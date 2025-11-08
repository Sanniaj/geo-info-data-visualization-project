"""
Download RAW NASA FIRMS detections for California across the entire year 2020.
- No cleaning, no dedupe, no merging — saves each 10-day chunk as returned by FIRMS.
- Output files: data/firms/firms_CA_<SOURCE>_<YYYY-MM-DD>.csv
"""

import os
import time
import pandas as pd
from datetime import date, timedelta
from config import NASA_FIRMS_API_KEY, NASA_FIRMS_URL, CA_BBOX_STR, FIRMS_DATA_DIR

# Choose a single 2020-available dataset. (NOAA-21 didn't exist in 2020.)
SOURCE = "MODIS_SP"
WINDOW_DAYS = 10            # FIRMS area API max window is 10 days

def window_starts(start_d: date, end_d: date, step: int):
    d = start_d
    while d <= end_d:
        yield d
        d += timedelta(days=step)

def download_chunk(start_dt: date, days: int):
    start_str = start_dt.strftime("%Y-%m-%d")
    url = (
        f"{NASA_FIRMS_URL}area/csv/"
        f"{NASA_FIRMS_API_KEY}/{SOURCE}/{CA_BBOX_STR}/{days}/{start_str}"
    )
    print(f"[{start_str} +{days}d] GET {url}")
    df = pd.read_csv(url)
    out_name = f"firms_CA_{SOURCE}_{start_str}.csv"
    out_path = os.path.join(FIRMS_DATA_DIR, out_name)
    df.to_csv(out_path, index=False)
    print(f"  Saved {len(df)} rows → {out_path}")

def main():
    if not NASA_FIRMS_API_KEY:
        raise SystemExit("Missing NASA_FIRMS_API_KEY. Set it in .env or config.py.")

    start = date(2020, 1, 1)
    end   = date(2020, 12, 31)

    for d in window_starts(start, end, WINDOW_DAYS):
        remaining = (end - d).days + 1
        days = min(WINDOW_DAYS, max(1, remaining))
        try:
            download_chunk(d, days)
        except Exception as e:
            print(f"  Error on {d} (+{days}d): {e}")
        # polite pause to avoid rate-limit spikes
        time.sleep(0.25)

if __name__ == "__main__":
    main()
