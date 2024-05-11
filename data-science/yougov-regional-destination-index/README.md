## DATA MODELING

# Data Modeling for Tourism Survey Analysis
## Overview
This repository hosts a Python script for local execution, which is dedicated to: 
- Processing and analysis of extensive survey data focusing on regional tourist destinations (YouGov Regional Destination Index). 
The authoritative version of the script is maintained on Google Cloud Platform (GCP) cloud services. 

## Main function
The primary goal of this repository is to **demonstrate the transformation of a complex input dataset — a SPSS file with over 2,230 columns — into three comprehensible, interrelated tables.**
The purpose of this data modeling is: 
- To capture individual survey responses
- Identify global trends by country.
- Assess the branding of various destinations as tourist spots.

## Output
The script outputs three CSV files:
- `main_ddbb_<Quarter>.csv`: This file records essential details for each participant of the survey. It's organized so that each row represents a distinct individual.
- `GTP_ddbb_<Quarter>.csv`: This file focuses on the global travel profiles of the individuals, featuring 205 unique variables to capture diverse aspects of travel preferences. It is structured with each row detailing the profile of one individual.
- `answers_ddbb_regions_<Quarter>.csv`: This file compiles responses from individuals regarding their opinions on 20 different regions. It is arranged such that each row contains a single individual's responses related to one specific region.
  
## Entity-Relationship Diagram (ERD)
The ERD demonstrates the structure of the database, illustrating the relationships between the main survey data (main_ddbb), the regional answers (answers_ddbb_regions), and the global travel profiles (GTP_ddbb). 
The caseid acts as a foreign key linking the regional answers and global profiles to the main survey data.

<img width="801" alt="ERD" src="https://github.com/rfeers/data-science-portfolio/assets/83583953/87309d9a-0dc7-4423-8bd2-6b056fe120fc">

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


  
Replace <Quarter> with the actual quarter's identifier when looking for the files.
