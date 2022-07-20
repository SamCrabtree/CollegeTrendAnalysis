import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import requests
import json
import os
import ssl
from datetime import date

# Magic that overrides SSL issues with TuitionTracker.org
ssl._create_default_https_context = ssl._create_unverified_context

########################################################################################################################
######################################### GATHERING THE DATA ###########################################################
########################################################################################################################

# IMPORT DATA FROM COLLEGE SCORECARD ONLINE
api_url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
api_key = ""

current_year = date.today().year


def year_select():
    value = input("What year data do you wish to look up? ")
    while len(value) != 4 or (not value.isdigit()):
        print('Not a 4 digit number')
        value = input('Please enter a 4 digit number:')
    value = int(value)
    if value > current_year:
        print('Sorry Marty McFly. You cannot select a date in the future... \n Try Again! ')
        year_select()
    if value < 1996:
        print('That is a year I haven\'t heard in a long time... The Interwebs doesn\'t go back that far. \n Try Again!')
        year_select()

    return value


year = year_select()


school_fields = [

    # SCHOOL INFORMATION
    "school.name",
    "school.city",
    "school.state",
    "school.degrees_awarded.predominant_recoded",

    # Data Definitions 0 - Not classified, 1 - Predominantly certificate-degree granting (varies),
    # 2 - Predominantly associate's-degree granting (2), 3 - Predominantly bachelor's-degree granting (4)
    # 4 - Entirely graduate-degree granting (5+)

    "school.ownership",

    # Data Definitions #  1 - Public, 2 - Private Non-Profit, 3 - Private For Profit

    "school.religious_affiliation",

    # RELIGION VALUE DICTIONARY
    # -1	Not reported
    # -2	Not applicable
    # 22	American Evangelical Lutheran Church
    # 24	African Methodist Episcopal Zion Church
    # 27	Assemblies of God Church
    # 28	Brethren Church
    # 30	Roman Catholic
    # 33	Wisconsin Evangelical Lutheran Synod
    # 34	Christ and Missionary Alliance Church
    # 35	Christian Reformed Church
    # 36	Evangelical Congregational Church
    # 37	Evangelical Covenant Church of America
    # 38	Evangelical Free Church of America
    # 39	Evangelical Lutheran Church
    # 40	International United Pentecostal Church
    # 41	Free Will Baptist Church
    # 42	Interdenominational
    # 43	Mennonite Brethren Church
    # 44	Moravian Church
    # 45	North American Baptist
    # 47	Pentecostal Holiness Church
    # 48	Christian Churches and Churches of Christ
    # 49	Reformed Church in America
    # 50	Episcopal Church, Reformed
    # 51	African Methodist Episcopal
    # 52	American Baptist
    # 53	American Lutheran
    # 54	Baptist
    # 55	Christian Methodist Episcopal
    # 57	Church of God
    # 58	Church of Brethren
    # 59	Church of the Nazarene
    # 60	Cumberland Presbyterian
    # 61	Christian Church (Disciples of Christ)
    # 64	Free Methodist
    # 65	Friends
    # 66	Presbyterian Church (USA)
    # 67	Lutheran Church in America
    # 68	Lutheran Church - Missouri Synod
    # 69	Mennonite Church
    # 71	United Methodist
    # 73	Protestant Episcopal
    # 74	Churches of Christ
    # 75	Southern Baptist
    # 76	United Church of Christ
    # 77	Protestant, not specified
    # 78	Multiple Protestant Denomination
    # 79	Other Protestant
    # 80	Jewish
    # 81	Reformed Presbyterian Church
    # 84	United Brethren Church
    # 87	Missionary Church Inc
    # 88	Undenominational
    # 89	Wesleyan
    # 91	Greek Orthodox
    # 92	Russian Orthodox
    # 93	Unitarian Universalist
    # 94	Latter Day Saints (Mormon Church)
    # 95	Seventh Day Adventists
    # 97	The Presbyterian Church in America
    # 99	Other (none of the above)
    # 100	Original Free Will Baptist
    # 101	Ecumenical Christian
    # 102	Evangelical Christian
    # 103	Presbyterian
    # 105	General Baptist
    # 106	Muslim
    # 107	Plymouth Brethren

    # 2020 SCHOOL YEAR DATA
    f"{year}.admissions.test_requirements",
    f"{year}.admissions.sat_scores.average.overall",
    f"{year}.admissions.admission_rate.overall",
    f"{year}.cost.tuition.in_state",
    f"{year}.cost.tuition.out_of_state",
    f"{year}.cost.tuition.program_year",
    f"{year}.completion.completion_rate_4yr_150nt",
    f"{year}.completion.completion_rate_less_than_4yr_150nt",
]

# Builds out the API Query URL


def api_query():
    response_api = requests.get(api_url + \
                                "&fields=id" + "&per_page=100" + "&api_key=" + api_key)
    data = response_api.text
    parse_json = json.loads(data)
    total = parse_json['metadata']['total']
    pages = round(total / 100)  # Takes the total number of colleges and divides it by the results per page setting to
                                # generate the number of API pages.

    return pages


# Variable storage for the above function.
num_pages = api_query()


# API SEARCH FUNCTION

# Builds out the API Query URL
def api_pull(fields):
    data_pull = []
    i = 0
    for page in range(num_pages):
        api_pull_url = requests.get(api_url +  \
              "&page=" + str(i) + "&fields=" + ",".join(fields) + "&per_page=100" + "&api_key=" + api_key)
        print("Downloading College Scorecard API Results for Page " + str(i) +
              " of " + str(num_pages) + "...")
        i += 1

        response = api_pull_url.text
        response_json = json.loads(response)

        data_pull.extend(response_json['results'])

    return data_pull


print("Beginning Program...")
api_query()
schools = api_pull(school_fields)
print("API Results Request complete. ")

# TAKES ALL API RESULTS AND CREATES PANDAS DATAFRAME
df1 = pd.DataFrame(schools)

# REORDER RESULTS COLUMNS
df1 = df1[["school.name", "school.city", "school.state", "school.degrees_awarded.predominant_recoded",
           "school.ownership", "school.religious_affiliation", f"{year}.admissions.test_requirements",
           f"{year}.admissions.sat_scores.average.overall", f"{year}.admissions.admission_rate.overall",
           f"{year}.cost.tuition.in_state", f"{year}.cost.tuition.out_of_state",
           f"{year}.cost.tuition.program_year",
           f"{year}.completion.completion_rate_4yr_150nt", f"{year}.completion.completion_rate_less_than_4yr_150nt", ]]

# RENAME DATAFRAME COLUMNS
df1.columns = ["Institution Name", "City", "State", "Primary Degree Offered", "Ownership", "Religious Affiliation",
               "School Test Requirements",
               f" {year} Test Averages", f"Total {year} Admissions Rate", f"In State Tuition {year} Academic Year",
               f"Out of State Tuition {year} Academic Year", "Program Year Cost", f"{year} 4 Year Graduation Rate",
               f"{year} Less Than 4 Year Graduation Rate",
               ]

df1['Ownership'] = df1['Ownership'].replace([1, 2, 3, ], ['Public', 'Private Not For Profit',
                                                               'Private For Profit'])

df1['Religious Affiliation'] = df1['Religious Affiliation'].fillna(-1)
df1['Religious Affiliation'] = df1['Religious Affiliation'].replace([-1, -2, 22, 24, 27, 28, 30, 33, 34,
                                                                     35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48,
                                                                     49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61,
                                                                     64, 65, 66, 67, 68, 69, 71, 73, 74, 75, 76, 77, 78,
                                                                     79, 80, 81, 84, 87, 88, 89, 91, 92, 93, 94, 95, 97,
                                                                     99, 100, 101, 102, 103, 105, 106, 107, 108,
                                                                     ],

                                                                    ["Not reported",
                                                                     "Not applicable",
                                                                     "American Evangelical Lutheran Church",
                                                                     "African Methodist Episcopal Zion Church",
                                                                     "Assemblies of God Church",
                                                                     "Brethren Church",
                                                                     "Roman Catholic",
                                                                     "Wisconsin Evangelical Lutheran Synod",
                                                                     "Christ and Missionary Alliance Church",
                                                                     "Christian Reformed Church",
                                                                     "Evangelical Congregational Church",
                                                                     "Evangelical Covenant Church of America",
                                                                     "Evangelical Free Church of America",
                                                                     "Evangelical Lutheran Church",
                                                                     "International United Pentecostal Church",
                                                                     "Free Will Baptist Church",
                                                                     "Interdenominational",
                                                                     "Mennonite Brethren Church",
                                                                     "Moravian Church",
                                                                     "North American Baptist",
                                                                     "Pentecostal Holiness Church",
                                                                     "Christian Churches and Churches of Christ",
                                                                     "Reformed Church in America",
                                                                     "Episcopal Church, Reformed",
                                                                     "African Methodist Episcopal",
                                                                     "American Baptist",
                                                                     "American Lutheran",
                                                                     "Baptist",
                                                                     "Christian Methodist Episcopal",
                                                                     "Church of God",
                                                                     "Church of Brethren",
                                                                     "Church of the Nazarene",
                                                                     "Cumberland Presbyterian",
                                                                     "Christian Church (Disciples of Christ)",
                                                                     "Free Methodist",
                                                                     "Friends",
                                                                     "Presbyterian Church (USA)",
                                                                     "Lutheran Church in America",
                                                                     "Lutheran Church - Missouri Synod",
                                                                     "Mennonite Church",
                                                                     "United Methodist",
                                                                     "Protestant Episcopal",
                                                                     "Churches of Christ",
                                                                     "Southern Baptist",
                                                                     "United Church of Christ",
                                                                     "Protestant, not specified",
                                                                     "Multiple Protestant Denomination",
                                                                     "Other Protestant",
                                                                     "Jewish",
                                                                     "Reformed Presbyterian Church",
                                                                     "United Brethren Church",
                                                                     "Missionary Church Inc",
                                                                     "Undenominational",
                                                                     "Wesleyan",
                                                                     "Greek Orthodox",
                                                                     "Russian Orthodox",
                                                                     "Unitarian Universalist",
                                                                     "Latter Day Saints (Mormon Church)",
                                                                     "Seventh Day Adventists",
                                                                     "The Presbyterian Church in America",
                                                                     "Other (none of the above)",
                                                                     "Original Free Will Baptist",
                                                                     "Ecumenical Christian",
                                                                     "Evangelical Christian",
                                                                     "Presbyterian",
                                                                     "General Baptist",
                                                                     "Muslim",
                                                                     "Plymouth Brethren",
                                                                     "Unknown",
                                                                     ])

df1['Religious Affiliation'] = df1['Religious Affiliation'].apply(str)

# Import Data From Multiple CSV Files Found at http://www.tuitiontracker.org/ NOTE: STILL WAITING FOR API ACCESS
# FOR THIS DATA SOURCE THIS CSV FILE CAN BE FOUND ON TUITION TRACKER.COM
print("Importing TuitionTracker.org Cost Data (CSV)")
df2 = pd.read_csv('https://www.tuitiontracker.org/data/download/cost-attendance.csv',
                  usecols=['Institution Name', 'Published in-state tuition and fees 2017-18 (IC2017_AY)',
                             ])

# Renames all of the Dataframes values above
df2.columns = ['Institution Name', 'In State Tuition 17-18', ]

# Imports Data Regarding Graduation Rates
print("Importing TuitionTracker.org Graduation Data (CSV)")
df3 = pd.read_csv('https://www.tuitiontracker.org/data/download/grad-rates.csv',
                  usecols=["Institution Name",
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

# Renames all of the Dataframe Columns above
df3.columns = ["Institution Name", "2016 4 YR Grad Rate", "2015 4 YR Grad Rate", "2014 4 YR Grad Rate",
               "2013 4 YR Grad Rate", "2012 4 YR Grad Rate", "2011 4 YR Grad Rate", "2016 2 YR Grad Rate",
               "2015 2 YR Grad Rate", "2014 2 YR Grad Rate", "2013 2 YR Grad Rate", "2012 2 YR Grad Rate",
               "2011 2 YR Grad Rate",
               ]


########################################################################################################################
####################################### WORKING WITH THE DATA ##########################################################
########################################################################################################################

print("Combining Data...")
# Merge all of the Dataframes from TuitionTracker.com CSV into a singular DataFrame
df4 = pd.merge(df2, df3, on='Institution Name')

# Merge all data from College Scorecard API and TuitionTracker.coms CSV files. NOTE: This Causes some results to
# disappear if a college is not in both resources.

df5 = pd.merge(df1, df4, on='Institution Name')

print("Calculating...")

# Calculates the rate of increase/decrease of tuition costs  from the 17-18 School year to the 2020 Academic Year.
df5["Tuition Percentage Change"] = (df5[f"In State Tuition {year} Academic Year"] - df5["In State Tuition 17-18"])\
                          / df5[f"In State Tuition {year} Academic Year"] * 100

# Calculates the difference in 4 year graduation rate between 2020 and another year and creates a new column
df5[f"4 Year Grad % Change from 2016-{year}"] = df5[f"{year} 4 Year Graduation Rate"] - df5["2016 4 YR Grad Rate"]
df5[f"4 Year Grad % Change from 2015-{year}"] = df5[f"{year} 4 Year Graduation Rate"] - df5["2015 4 YR Grad Rate"]
df5[f"4 Year Grad % Change from 2014-{year}"] = df5[f"{year} 4 Year Graduation Rate"] - df5["2014 4 YR Grad Rate"]
df5[f"4 Year Grad % Change from 2012-{year}"] = df5[f"{year} 4 Year Graduation Rate"] - df5["2012 4 YR Grad Rate"]
df5[f"4 Year Grad % Change from 2011-{year}"] = df5[f"{year} 4 Year Graduation Rate"] - df5["2011 4 YR Grad Rate"]

# Calculates the difference in less than 4 year graduation rate between 2020 and another year and creates a new column
df5[f"2 Year Grad % Change from 2016-{year}"] = df5[f"{year} Less Than 4 Year Graduation Rate"] - df5["2016 2 YR Grad Rate"]
df5[f"2 Year Grad % Change from 2015-{year}"] = df5[f"{year} Less Than 4 Year Graduation Rate"] - df5["2015 2 YR Grad Rate"]
df5[f"2 Year Grad % Change from 2014-{year}"] = df5[f"{year} Less Than 4 Year Graduation Rate"] - df5["2014 2 YR Grad Rate"]
df5[f"2 Year Grad % Change from 2012-{year}"] = df5[f"{year} Less Than 4 Year Graduation Rate"] - df5["2012 2 YR Grad Rate"]
df5[f"2 Year Grad % Change from 2011-{year}"] = df5[f"{year} Less Than 4 Year Graduation Rate"] - df5["2011 2 YR Grad Rate"]

########################################################################################################################
####################################### DISPLAYING THE DATA ############################################################
########################################################################################################################


sns.set_style('darkgrid')

grad_vs_tuition = sns.scatterplot(x=f"{year} 4 Year Graduation Rate", y=f"In State Tuition {year} Academic Year",
                                  hue="Ownership", data=df5);

plt.title("Tuition Cost vs. Graduation Rate")

st_grad_rates = sns.relplot(x="State", y=f"{year} 4 Year Graduation Rate", hue="Ownership", data=df5);
plt.title("Graduation Rates by State")
for ax in st_grad_rates.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)


tuition_by_org_rates = sns.relplot(x=str("Religious Affiliation"), y=f"In State Tuition {year} Academic Year",
                                   data=df5);
plt.title("Tuition by Religious Affiliation")
for ax in tuition_by_org_rates.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)

#SHOWS ALL PLOTS ABOVE
plt.show()

