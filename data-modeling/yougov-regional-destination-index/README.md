## DATA MODELING

# Data Modeling for Tourism Survey Analysis
## Overview
This repository hosts a Python script for local execution, which is dedicated to the processing and analysis of extensive survey data focusing on regional tourist destinations. 
The authoritative version of the script is maintained on Google Cloud Platform (GCP) cloud services. 

## Main function
The primary goal of this repository is to demonstrate the transformation of a complex input dataset — a substantial SPSS file with over 2,230 columns — into three comprehensible, interrelated tables.
The purpose of this data modeling is to capture individual survey responses, identify global trends by country, and assess the branding of various destinations as tourist spots. 
The ERD attached to this documentation visualizes the relationships between different datasets within the project.

## Entity-Relationship Diagram (ERD)
The ERD demonstrates the structure of the database, illustrating the relationships between the main survey data (main_ddbb), the regional answers (answers_ddbb_regions), and the global travel profiles (GTP_ddbb). 
The caseid acts as a foreign key linking the regional answers and global profiles to the main survey data.

<img width="801" alt="ERD" src="https://github.com/rfeers/data-science-portfolio/assets/83583953/5bea8cb3-b1c3-4f2d-a628-accf68d3036c">


## Scripts
`get_data()`
This function retrieves survey data stored in SPSS format from a specified directory. It constructs a dictionary where each key-value pair corresponds to a country and its associated data.

`generating_final_tables()`
This function processes the retrieved data to structure it according to predefined schemas. It generates three final DataFrames: main_ddbb_final, GTP_ddbb_final, and answers_ddbb_regions, each corresponding to a different aspect of the survey.

`save_tables()`
After processing, this function saves the final tables into CSV format in an output directory for further analysis or storage.

## Usage
The data is confidential, so it is not attached in the former repository. 
The code is hosted in our GCP-environment. 

# Requirements
- Python 3.x
- Pandas library
- NumPy library
- os module
Please make sure to install the required dependencies before running the script.

## Output
The script outputs three CSV files:
- main_ddbb_<Quarter>.csv: Contains the main survey data.
- GTP_ddbb_<Quarter>.csv: Contains the global travel profile data.
- answers_ddbb_regions_<Quarter>.csv: Contains the regional answers data.
  
Replace <Quarter> with the actual quarter's identifier when looking for the files.
