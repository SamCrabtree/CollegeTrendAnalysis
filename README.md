# College Trend Analyst

This program is designed to allow a user to view trends 
about Colleges for a specific year going back to 1995.
It provides visual presentations showing graduation rate vs
tuition cost, state college graduation rates, and tuition cost
by religious affiliation. 



## Project Goals

This project was made as part of a requirement for CodeLouisville's Data Analysis 2 program and meets the 
following project requirements: 

1. **Read TWO data sets in with an API (or use two different APIs that have data you can combine to answer new questions).**
As previously discussed with Mentors, one source is an API online using the CollegeScorecard API and the other
two sources (CSVs) come from TuitionTracker.org that still pending. 

2. **Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set.**
This project merges the dataset created from the CollegeScorecard API, and from TuitionTracker.com's CSV Files.

4. **Make 3 matplotlib or seaborn (or another plotting library) visualizations to display your data.**

We have three Seaborn Plots that print off as a result of this program. The first visualization show the comparison of
annual tuition cost to the institutions' graduation rate. The second visualization covers each states college graduation 
rate. The Third shows tuition cost by Religious Organization. 

5. **Utilize a virtual environment and include instructions in your README on how the user should set one up.**
Specifically this program was set up using Poetry, but a traditional VENV is able to be used with the included 
requirements.txt file. 

6. **Annotate your .py files with well-written comments and a clear README.md (only applicable if you’re not using a jupyter notebook).**
NOTE: This SHOULD be met by the file you are reading right now! 



## Setup


This program requires two major steps for setup. First, is the setup of a virtual environment. Second, you will 
need to get an API Key from CollegeScorecard.com. 


### Virtual Environment 

There are two ways you can go about creating a virtual environment. 

1. **Poetry**
Poetry uses primarily TOML files to help create a virtual environment and install all necessary files. 

2. **VENV**
The most common way to create a virtual environment and install all of the packages found in the Requirements.txt file


### API Key

In order to use this program, you will need to get an API key from CollegeScorecard.com. This is rather simple.
Go to https://collegescorecard.ed.gov/data/documentation/ and scroll to the bottom of the page. There you will
need to complete a security question. Then you should be able to apply for API approval rather quickly. 



