"""
Download NOAA weather data for California across 2020 for wildfire prediction.
Key variables: temperature, precipitation, wind speed, humidity
Output files: data/noaa/noaa_weather_CA_<YYYY-MM-DD>.csv
"""

import os
import time
import requests
import pandas as pd
from datetime import date, timedelta
from config import NOAA_API_KEY, NOAA_API_URL, NOAA_DATA_DIR

# NOAA CDO Dataset and location
DATASET_ID = "GHCND"  # Global Historical Climatology Network - Daily
LOCATION_ID = "FIPS:06"  # California FIPS code
WINDOW_DAYS = 365  # NOAA CDO allows up to 1 year per request

# Weather data types relevant for wildfire prediction
DATATYPES = [
    "TMAX",  # Maximum temperature
    "TMIN",  # Minimum temperature
    "PRCP",  # Precipitation
    "AWND",  # Average wind speed
    "WSF2",  # Fastest 2-minute wind speed
    "WSF5",  # Fastest 5-second wind speed
]

def download_chunk(start_dt: date, end_dt: date, offset=0):
    """
    Download weather data for a date range.
    NOAA CDO API has a 1000-result limit, so may need multiple calls with offset.
    """
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    url = f"{NOAA_API_URL}data"
    headers = {"token": NOAA_API_KEY}
    params = {
        "datasetid": DATASET_ID,
        "locationid": LOCATION_ID,
        "startdate": start_str,
        "enddate": end_str,
        "datatypeid": ",".join(DATATYPES),
        "limit": 1000,  # Max results per request
        "offset": offset,
        "units": "metric"
    }

    print(f"[{start_str} to {end_str}] GET {url} (offset={offset})")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        df = pd.DataFrame(data["results"])
        return df, data["metadata"]["resultset"]["count"]
    else:
        print(f"  No results")
        return None, 0

def download_full_period(start_dt: date, end_dt: date):
    """
    Download all data for a period, handling pagination if > 1000 results.
    """
    all_data = []
    offset = 1  # NOAA CDO uses 1-based offset

    while True:
        df, total_count = download_chunk(start_dt, end_dt, offset)

        if df is None:
            break

        all_data.append(df)
        print(f"  Retrieved {len(df)} rows (total available: {total_count})")

        # Check if we need more pages
        if offset + len(df) - 1 >= total_count:
            break

        offset += 1000
        time.sleep(0.2)  # Rate limit pause between pagination requests

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        start_str = start_dt.strftime("%Y-%m-%d")
        out_name = f"noaa_weather_CA_{start_str}.csv"
        out_path = os.path.join(NOAA_DATA_DIR, out_name)
        combined_df.to_csv(out_path, index=False)
        print(f"  Saved {len(combined_df)} total rows → {out_path}")

def main():
    if not NOAA_API_KEY:
        raise SystemExit("Missing NOAA_API_KEY. Set it in .env or config.py.")

    # Download full year 2020
    start = date(2020, 1, 1)
    end = date(2020, 12, 31)

    try:
        download_full_period(start, end)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\nDownload complete!")

if __name__ == "__main__":
    main()