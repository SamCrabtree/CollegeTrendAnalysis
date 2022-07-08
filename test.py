import pandas as pd
import requests
import json
import os
from pandas import json_normalize
import ssl

# #Imports Data Regarding Graduation Rates NOTE: STILL WAITING FOR API ACCESS FOR THIS DATA SOURCE THIS CSV FILE CAN BE FOUND ON TUITION TRACKER.COM
df2 = pd.read_csv('http://www.tuitiontracker.org/data/download/grad-rates.csv',
                           usecols = ["Institution Name",
                                      "Grand total (GR2016  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2015  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2014  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2013  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2012  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2011  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2016  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2015  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2014  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2013  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2012  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      "Grand total (GR2011  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                                      ])

# This Merges the above Dataframes by the institution name (which is listed as school.name on Gov College Score Card
# and "Institution Name" at Tuition Tracker

print(df2)