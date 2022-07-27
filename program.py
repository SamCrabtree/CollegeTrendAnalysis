import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import requests
import json
import os
import ssl
from datetime import date
from dotenv import load_dotenv
load_dotenv()


# Magic that overrides SSL issues with TuitionTracker.org
ssl._create_default_https_context = ssl._create_unverified_context


########################################################################################################################
######################################### GATHERING THE DATA ###########################################################
########################################################################################################################

# IMPORT DATA FROM COLLEGE SCORECARD ONLINE
api_url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
api_key = os.getenv('COLLEGE_SCORECARD')

def year_select():
    current_year = date.today().year
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


# Builds out the API Query URL


def find_num_pages_query():

    response_api = requests.get(api_url + \
                                "&fields=id" + "&per_page=100" + "&api_key=" + api_key)
    data = response_api.text
    parse_json = json.loads(data)
    total = parse_json['metadata']['total']
    pages = round(total / 100)  # Takes the total number of colleges and divides it by the results per page setting to
                                # generate the number of API pages.

    return pages

# API SEARCH FUNCTION

# Builds out the API Query URL


def api_pull(fields, num_pages):
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


# TAKES ALL API RESULTS AND CREATES PANDAS DATAFRAME
def api_dataframe(year, institutions):
    schools = pd.DataFrame(institutions)

    # REORDER RESULTS COLUMNS
    schools = schools[["school.name", "school.city", "school.state", "school.degrees_awarded.predominant_recoded",
               "school.ownership", "school.religious_affiliation", f"{year}.admissions.test_requirements",
               f"{year}.admissions.sat_scores.average.overall", f"{year}.admissions.admission_rate.overall",
               f"{year}.cost.tuition.in_state", f"{year}.cost.tuition.out_of_state",
               f"{year}.cost.tuition.program_year",
               f"{year}.completion.completion_rate_4yr_150nt", f"{year}.completion.completion_rate_less_than_4yr_150nt",
               # "2018.cost.tuition.in_state", "2019.cost.tuition.in_state", "2020.cost.tuition.in_state",
               ]]

    # RENAME DATAFRAME COLUMNS
    schools.columns = ["Institution Name", "City", "State", "Primary Degree Offered", "Ownership", "Religious Affiliation",
                   "School Test Requirements",
                   f" {year} Test Averages", f"Total {year} Admissions Rate", f"In State Tuition {year} Academic Year",
                   f"Out of State Tuition {year} Academic Year", "Program Year Cost", f"{year} 4 Year Graduation Rate",
                   f"{year} Less Than 4 Year Graduation Rate",
                   # "In State Tuition 2018", "In State Tuition 2019",
                   # "In State Tuition 2020",
                   ]

    # REPLACE PRIMARY DEGREE NUMBER RESULTS WITH PROPER DEFINITIONS.
    schools['Primary Degree Offered'] = schools['Primary Degree Offered'].replace([0, 1, 2, 3, 4, ], ['Not classified',
                                                                                                      'Certificate',
                                                                                                      'Associate',
                                                                                                      'Bachelor\'s',
                                                                                                      'Graduate', ])

    # REPLACE OWNERSHIP KIND NUMBER RESULTS WITH PROPER DEFINITIONS.
    schools['Ownership'] = schools['Ownership'].replace([1, 2, 3, ], ['Public', 'Private Not For Profit',
                                                              'Private For Profit', ])

    # DEFINE NULL VALUES FOR RELIGIOUS AFFILIATION AND REPLACES NUMBER VALUES WITH PROPER DEFINITIONS
    schools['Religious Affiliation'] = schools['Religious Affiliation'].fillna(-1)
    schools['Religious Affiliation'] = schools['Religious Affiliation'].replace([-1, -2, 22, 24, 27, 28, 30, 33, 34,
                                                                                 35, 36, 37, 38, 39, 40, 41, 42, 43,
                                                                                 44, 45, 47, 48, 49, 50, 51, 52, 53,
                                                                                 54, 55, 57, 58, 59, 60,
                                                                                 61, 64, 65, 66, 67, 68, 69, 71, 73,
                                                                                 74, 75, 76, 77, 78, 79, 80, 81, 84,
                                                                                 87, 88, 89, 91, 92, 93, 94, 95, 97,
                                                                                 99, 100, 101, 102, 103, 105, 106,
                                                                                 107, 108,
                                                                                 ],

                                                                        ["Not Reported",
                                                                         "Not Applicable",
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
    return schools

# Import Data From Multiple CSV Files Found at http://www.tuitiontracker.org/ NOTE: STILL WAITING FOR API ACCESS
# FOR THIS DATA SOURCE THIS CSV FILE CAN BE FOUND ON TUITION TRACKER.COM

def in_state_tuition():
    print("Importing TuitionTracker.org Cost Data (CSV)")
    tuition_fees = pd.read_csv('https://www.tuitiontracker.org/data/download/cost-attendance.csv',
                      usecols=['Institution Name',
                               'Published in-state tuition and fees 2009-10 (IC2009_AY)',
                               'Published in-state tuition and fees 2010-11 (IC2010_AY)',
                               'Published in-state tuition and fees 2011-12 (IC2011_AY)',
                               'Published in-state tuition and fees 2012-13 (IC2012_AY)',
                               'Published in-state tuition and fees 2013-14 (IC2013_AY)',
                               'Published in-state tuition and fees 2014-15 (IC2014_AY)',
                               'Published in-state tuition and fees 2015-16 (IC2015_AY)',
                               'Published in-state tuition and fees 2016-17 (IC2016_AY)',
                               'Published in-state tuition and fees 2017-18 (IC2017_AY)',
                               ])

    # Renames all of the Dataframes values above
    tuition_fees.columns = ['Institution Name',
                   'In State Tuition 2009',
                   'In State Tuition 2010',
                   'In State Tuition 2011',
                   'In State Tuition 2012',
                   'In State Tuition 2013',
                   'In State Tuition 2014',
                   'In State Tuition 2015',
                   'In State Tuition 2016',
                   'In State Tuition 2017',
                   ]
    return tuition_fees

# Imports Data Regarding Graduation Rates
def grad_info():
    print("Importing TuitionTracker.org Graduation Data (CSV)")
    grad_rates = pd.read_csv('https://www.tuitiontracker.org/data/download/grad-rates.csv',
                      usecols=["Institution Name",
                               "Grand total (GR2011  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2012  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2013  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2014  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2015  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2016  Bachelor's or equiv subcohort (4-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2011  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2012  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2013  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2014  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2015  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               "Grand total (GR2016  Degree/certif-seeking students ( 2-yr institution) CALCULATED GRADUATION RATE)",
                               ])

    # Renames all of the Dataframe Columns above
    grad_rates.columns = ["Institution Name", "2011 4 YR Grad Rate", "2012 4 YR Grad Rate", "2013 4 YR Grad Rate",
                   "2014 4 YR Grad Rate", "2015 4 YR Grad Rate", "2016 4 YR Grad Rate", "2011 2 YR Grad Rate",
                   "2012 2 YR Grad Rate", "2013 2 YR Grad Rate", "2014 2 YR Grad Rate", "2015 2 YR Grad Rate",
                   "2016 2 YR Grad Rate",
                   ]
    return grad_rates


########################################################################################################################
####################################### WORKING WITH THE DATA ##########################################################
########################################################################################################################
def data_clean(value, schools, tuition_fees, grad_rates,):
    print("Combining Data...")
    # Merge all of the Dataframes from TuitionTracker.com CSV into a singular DataFrame
    year = value
    grad_rates_and_fees = pd.merge(tuition_fees, grad_rates, on='Institution Name')

    # Merge all data from College Scorecard API and TuitionTracker.coms CSV files. NOTE: This Causes some results to
    # disappear if a college is not in both resources.

    clean_data = pd.merge(schools, grad_rates_and_fees, on='Institution Name')

    print("Calculating...")

    # Calculates the rate of increase/decrease of tuition costs  from the selected year to other ones on file.
    clean_data[f"Tuition % Change {year} - 2009"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2009"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2009"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2010"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2010"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2010"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2011"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2011"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2011"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2012"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2012"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2012"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2013"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2013"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2013"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2014"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2014"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2014"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2015"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2015"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2015"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2016"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2016"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2016"]) / 2) * 100
    clean_data[f"Tuition % Change {year} - 2017"] = (clean_data[f"In State Tuition {year} Academic Year"]
                                              - clean_data["In State Tuition 2017"]) /\
                                             ((clean_data[f"In State Tuition {year} Academic Year"]
                                               + clean_data["In State Tuition 2017"]) / 2) * 100

    # Calculates the difference in 4 year graduation rate between 2020 and another year and creates a new column
    clean_data[f"4 Year Grad % Change from 2011-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2011 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2011 4 YR Grad Rate"]) / 2) * 100
    clean_data[f"4 Year Grad % Change from 2012-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2012 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2012 4 YR Grad Rate"]) / 2) * 100
    clean_data[f"4 Year Grad % Change from 2013-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2013 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2013 4 YR Grad Rate"]) / 2) * 100
    clean_data[f"4 Year Grad % Change from 2014-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2014 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2014 4 YR Grad Rate"]) / 2) * 100
    clean_data[f"4 Year Grad % Change from 2015-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2015 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2015 4 YR Grad Rate"]) / 2) * 100

    clean_data[f"4 Year Grad % Change from 2016-{year}"] = (clean_data[f"{year} 4 Year Graduation Rate"]
                                                     - clean_data["2016 4 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} 4 Year Graduation Rate"]
                                                        + clean_data["2016 4 YR Grad Rate"]) / 2) * 100

    # Calculates difference in less than 4 year graduation rate between 2020 and another year and creates a new column

    clean_data[f"2 Year Grad % Change from 2011-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2011 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2011 2 YR Grad Rate"]) / 2) * 100
    clean_data[f"2 Year Grad % Change from 2012-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2012 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2012 2 YR Grad Rate"]) / 2) * 100
    clean_data[f"2 Year Grad % Change from 2013-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2013 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2013 2 YR Grad Rate"]) / 2) * 100
    clean_data[f"2 Year Grad % Change from 2014-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2014 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2014 2 YR Grad Rate"]) / 2) * 100
    clean_data[f"2 Year Grad % Change from 2015-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2015 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2015 2 YR Grad Rate"]) / 2) * 100
    clean_data[f"2 Year Grad % Change from 2016-{year}"] = (clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                     - clean_data["2016 2 YR Grad Rate"]) /\
                                                      ((clean_data[f"{year} Less Than 4 Year Graduation Rate"]
                                                        + clean_data["2016 2 YR Grad Rate"]) / 2) * 100
    return clean_data

########################################################################################################################
####################################### DISPLAYING THE DATA ############################################################
########################################################################################################################

def render_visualizations(value, dataframe):
    year = value
    sns.set_style('darkgrid')
    
    sns.scatterplot(x=f"{year} 4 Year Graduation Rate", y=f"In State Tuition {year} Academic Year",
                    hue="Primary Degree Offered", data=dataframe)
    plt.title("Tuition Cost vs. Graduation Rate")
    # SHOWS ALL PLOTS ABOVE
    plt.show()


    sns.boxplot(x="State", y=f"{year} 4 Year Graduation Rate", data=dataframe)
    plt.title("Graduation Rates by State")
    plt.show()

    tuition_by_org_rates = sns.relplot(x=str("Religious Affiliation"), y=f"In State Tuition {year} Academic Year",
                                       data=dataframe)
    plt.title("Tuition by Religious Affiliation")
    for ax in tuition_by_org_rates.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)

    # SHOWS ALL PLOTS ABOVE
    plt.show()


def main():
    year = year_select()
    fields = [
        "school.name",
        "school.city",
        "school.state",
        "school.degrees_awarded.predominant_recoded",
        "school.ownership",
        "school.religious_affiliation",
        f"{year}.admissions.test_requirements",
        f"{year}.admissions.sat_scores.average.overall",
        f"{year}.admissions.admission_rate.overall",
        f"{year}.cost.tuition.in_state",
        f"{year}.cost.tuition.out_of_state",
        f"{year}.cost.tuition.program_year",
        f"{year}.completion.completion_rate_4yr_150nt",
        f"{year}.completion.completion_rate_less_than_4yr_150nt",
    ]
    num_pages = find_num_pages_query()
    institutions = api_pull(fields, num_pages)
    schools = api_dataframe(year, institutions)
    tuition_fees = in_state_tuition()
    grad_rates = grad_info()
    clean_data = data_clean(year, schools, tuition_fees, grad_rates,)
    render_visualizations(year, clean_data)


if __name__ == "__main__":
    main()

