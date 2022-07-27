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

5. **Utilize a virtual environment and include instructions in your README on how the user should set one up.**.
Specifically this program was set up using Poetry, but a traditional VENV is able to be used with the included 
requirements.txt file. 

6. **Annotate your .py files with well-written comments and a clear README.md (only applicable if you’re not using a jupyter notebook).**
NOTE: This SHOULD be met by the file you are reading right now! 



## Setup


This program requires two major steps for setup. First, is the setup of a virtual environment. Second, you will 
need to get an API Key from CollegeScorecard.com. 


### Virtual Environment 

There are two ways you can go about creating a virtual environment.

### Via Poetry
1. Clone the Repository to your local device.
2. Install Poetry to your device. (For more information about poetry check out https://python-poetry.org/ )
3. Open the folder in terminal or gitbash and type 
`Poetry Shell`
4. Next, install the required programs from the pyproject.toml file by typing 
`Poetry Install`
` 

### Via Requirements.txt
1. Clone the Repository to your local device. 
2. Navigate to the project folder with terminal or gitbash and create a virtual envioronment. 
- Windows
`python -m venv venv`
- Mac/Linux
`python3 -m venv venv`
3. Activate your virtual environment 
- Windows 
`venv\Scripts\activate.bat`
- Mac/Linux
`source venv/bin/activate`
4. Install the requirements.txt file using the following comand 
`pip install -r requirements.txt`


### API Key and addition

In order to use this program, you will need to get an API key from CollegeScorecard.com. This is rather simple.
Go to https://collegescorecard.ed.gov/data/documentation/ and scroll to the bottom of the page. There you will
need to complete a security question. Then you should be able to apply for API approval rather quickly. 

Once you have completed this process, and are issued an API key, you will need to add the API key to the a .env file. 
In the repo, you will find a file called **.env.example** paste the api key with no spaces or quotations to the right of
the "=" sign and rename the file to .env.

## Running The Program

1. Once you have activate your virtual environment above
- For Windows: 
`python program.py`

- For Mac/Linux:
`python3 program.py`

2. You will be prompted to enter the year you wish to review. 

3. Once you finish, you will be presented with three figures. 

