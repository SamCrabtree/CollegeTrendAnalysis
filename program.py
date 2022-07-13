import pandas as pd
import requests
import json
import os





# IMPORT DATA FROM COLLEGE SCORECARD ONLINE
api_url = "https://api.data.gov/ed/collegescorecard/v1/"
api_key = ""

school_dataset = "schools"
school_fields = [

    #SCHOOL INFORMATION
    "school.name",
    "school.city",
    "school.state",
    "school.degrees_awarded.predominant_recoded",

    # Data Definitions 0 - Not classified, 1 - Predominantly certificate-degree granting (varies),
    # 2 - Predominantly associate's-degree granting (2), 3 - Predominantly bachelor's-degree granting (4)
    # 4 - Entirely graduate-degree granting (5+)

    "school.ownership", # Data Definitions #  1 - Public, 2 - Private Non-Profit, 3 - Private For Profit

    #SCHOOL BODY DETAILS
    "school.religious_affiliation",
    "2020.admissions.test_requirements",
    "2020.admissions.sat_scores.average.overall",
    "2020.admissions.admission_rate.overall",
    "2020.cost.tuition.in_state",
    "2020.cost.tuition.out_of_state",
    "2020.cost.tuition.program_year",
]

# Builds out the API Query URL

def api_query():
    response_api = requests.get( api_url + school_dataset + ".json?" + \
                                 "&fields=id" + "&per_page=100" + "&api_key=" + api_key)
    data = response_api.text
    parse_json = json.loads(data)
    total = parse_json['metadata']['total']
    pages = round(total / 100) #Takes the total number of colleges and divides it by the results per page setting to
                               # generate the number of API pages.

    return pages

# Variable storage for the above function.
num_pages = api_query()


#API SEARCH FUNCTION

# Builds out the API Query URL
def api_pull(dataset, fields):
    data_pull = []
    i = 0
    for page in range(num_pages):
        api_pull_url = requests.get(api_url + dataset + ".json?" +  \
              "&page=" + str(i) + "&fields=" + ",".join(fields) + "&per_page=100" + "&api_key=" + api_key )
        print("Downloading College Scorecard API Results for " + dataset.title() + " Page " +str(i) +
              " of " + str(num_pages) + "...")
        i += 1

        response = api_pull_url.text
        response_json = json.loads(response)

        data_pull.extend(response_json['results'])

    return data_pull



print("Beginning Program...")
api_query()
schools = api_pull(school_dataset, school_fields)

#TAKES ALL API RESULTS AND CREATES PANDAS DATAFRAME
df1 = pd.DataFrame(schools)

# REORDER RESULTS COLUMNS
df1 = df1[["school.name", "school.city", "school.state", "school.degrees_awarded.predominant_recoded",
               "school.ownership", "school.religious_affiliation", "2020.admissions.test_requirements",
               "2020.admissions.sat_scores.average.overall", "2020.admissions.admission_rate.overall",
               "2020.cost.tuition.in_state", "2020.cost.tuition.out_of_state", "2020.cost.tuition.program_year", ]]

#RENAME API COLUMNS
df1.columns = ["Institution Name", "City", "State", "Primary Degree Offered", "Ownership", "Religious Affiliation",
               "School Test Requirements",
               "Test Averages", "Total Admissions Rate","In State Tuition Academic Year",
               "Out of State Tuition Academic Year", "Program Year Cost",
               ]

# Import Data From Multiple CSV Files Found at http://www.tuitiontracker.org/ NOTE: STILL WAITING FOR API ACCESS
# FOR THIS DATA SOURCE THIS CSV FILE CAN BE FOUND ON TUITION TRACKER.COM

df2 = pd.read_csv('http://www.tuitiontracker.org/data/download/cost-attendance.csv',
                  usecols=['Institution Name', 'Published in-state tuition and fees 2017-18 (IC2017_AY)',
                             ])

# Renames all of the Dataframes values above
df2.columns = ['Institution Name', 'In State Tuition 17-18',]

#Imports Data Regarding Graduation Rates
df3 = pd.read_csv('http://www.tuitiontracker.org/data/download/grad-rates.csv',
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

# Renames all of the Dataframes values above
df3.columns = ["Institution Name", "2016 4 YR Grad Rate", "2015 4 YR Grad Rate", "2014 4 YR Grad Rate",
               "2013 4 YR Grad Rate", "2012 4 YR Grad Rate", "2011 4 YR Grad Rate", "2016 2 YR Grad Rate",
               "2015 2 YR Grad Rate", "2014 2 YR Grad Rate", "2013 2 YR Grad Rate", "2012 2 YR Grad Rate",
               "2011 2 YR Grad Rate",
               ]

# Merge all of the Dataframes from TuitionTracker.com CSV into a singular DataFrame
df4 = pd.merge(df2, df3, on='Institution Name')

# Merge all data from College Scorecard API and TuitionTracker.coms CSV files.
df5 = pd.merge(df1, df4, on='Institution Name')





