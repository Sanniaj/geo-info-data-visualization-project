# Geo-Info Data Visualization Feature

This module provides geospatial data visualization for the Senior Design Project using **GeoPandas**, **Rasterio**, and **Matplotlib**.

---

## Setup

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   # or
   venv\Scripts\Activate.ps1      # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install notebook geopandas pandas rasterio shapely requests matplotlib
   ```

3. **(Optional) Save them for reuse:**
   ```bash
   pip freeze > requirements.txt
   ```

---

## Quick Test

Run this small script to verify your setup:

```python
import geopandas, rasterio, shapely, pandas, requests, matplotlib
print("Geo-Info visualization dependencies installed successfully!")
```

---

## 📄 Notes

- Tested on Python 3.10+.
- Virtual environment (`venv/`) should not be committed to Git.