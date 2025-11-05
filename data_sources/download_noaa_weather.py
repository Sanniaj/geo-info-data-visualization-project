"""
Downloads NASA FIRMS data for California regions.
Data source:
"""

#import libraries for data manipulation

import pandas as pd
import requests

#Let's read VIIRS csv sample data set into a DataFrame df

df =pd.read_csv('https://firms.modaps.eosdis.nasa.gov/content/notebooks/sample_viirs_snpp_071223.csv')

# show how many rows (records) and columns (values per record) we have

print ('FIRMS sample fire data contains %i rows and %i columns' % (df.shape[0], df.shape[1]))
df.shape