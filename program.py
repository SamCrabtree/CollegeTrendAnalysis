import pandas as pd
import requests
import json
import os
from pandas import json_normalize
from dotenv import load_dotenv
import ssl


load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context

# IMPORT DATA FROM COLLEGE SCORECARD ONLINE
api_url = "https://api.data.gov/ed/collegescorecard/v1/"
api_key = os.getenv("COLLEGE_SCORECARD")
dataset = "schools.json?"
fields = [
    #ID NUMBER
    "id",

    #SCHOOL INFORMATION
    "school.name",
    "school.city",
    "school.state",
    "school.school_url",
    "school.accreditor",
    "school.degrees_awarded.predominant_recoded",
    # Data Definitions
    #  0 - Not classified
    #  1 - Predominantly certificate-degree granting (varies)
    #  2 - Predominantly associate's-degree granting (2)
    #  3 - Predominantly bachelor's-degree granting (4)
    #  4 - Entirely graduate-degree granting (5+)
    "school.ownership",
    # Data Definitions
    #  1 - Public
    #  2 - Private Non-Profit
    #  3 - Private For Profit

    #SCHOOL BODY DETAILS
    "school.men_only",
    "school.women_only",
    "school.minority_serving.historically_black",
    "school.minority_serving.predominantly_black",
    "school.minority_serving.annh", # Alaska Native / Native Hawaiian Serving Institution
    "school.minority_serving.nant", # Native American Non-Tribal Serving Institution
    "school.minority_serving.tribal", # Native Tribal Serving Institution
    "school.minority_serving.aanipi", # Native American Pacific Islander Serving Institution
    "school.minority_serving.hispanic", # Hispanic Serving Institution
    "school.religious_affiliation",

    #ADMISSIONS NUMBERS
    "admissions.admission_rate_overall",

    # COST
    "cost.tuition.in_state",
    "cost.tuitionout-of_state",
    "cost.attendance_program_year",
    "cost.attendance_academic_year",
    "cost.tuition_program_year",
    "cost.booksupply",
    "cost.roomboard_oncampus",
    "cost.otherexpense.oncampus",
    "cost.roomboard_offcampus",
    "cost.otherexpense.offcampus",

    # DROPOUT RATES

]

api_request = api_url + dataset + \
              "&fields=" + ",".join(fields) + "&per_page=100&api_key=" + api_key



print(api_request)
r = requests.get(api_request).json()


df1 = pd.json_normalize(r['results'])

# #Import Data From Multiple CSV Files Found at https://www.tuitiontracker.org/
# colleges_df = pd.read_csv('https://www.tuitiontracker.org/data/download/institutions.csv', usecols = ['UnitID', 'Institution Name'])
# sticker_tuition_df = pd.read_csv('https://www.tuitiontracker.org/data/download/cost-attendance.csv', usecols = ['UnitID', 'Institution Name'])
# #Imports Data Regarding
# net_tuition_df = pd.read_csv('https://www.tuitiontracker.org/data/download/net-price.csv', usecols = ['UnitID', 'Institution Name'])
#
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

df3 = pd.merge(df1, df2, left_on='school.name', right_on='Institution Name').drop('Institution Name', axis=1)

print(df3)

# retention_rate_df = pd.read_csv('https://www.tuitiontracker.org/data/download/retention-rates.csv', usecols = ['UnitID','Institution Name'])
#
# #Combine all CSV files into one large DataSet by Concatenating NOTE: Since all files UnitID's Match Up Pandas auto does this.
# dataset_df = [colleges_df, sticker_tuition_df, net_tuition_df, grad_rate_df, retention_rate_df]
# results = pd.concat(dataset_df)
#
# print(results)





