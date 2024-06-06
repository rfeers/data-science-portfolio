# Chicago Taxi Data Pipeline

This repository contains two main functions that handle the historical and recurrent data fetching, processing, and integration of Chicago taxi data into BigQuery using Google Cloud Functions. The raw data is modelized into five tables to smooth its usage

Overview
This project is designed to automate the data pipeline for Chicago taxi data, ensuring that historical data is fully fetched and stored, and new data is continuously updated daily.

## Overview
This project is designed to automate the data pipeline for Chicago taxi data, ensuring that historical data is fully fetched and stored, and new data is continuously updated daily.

## Data Modeling

The raw data is modelized into five tables to smooth its consumption. These tables are designed to optimize querying and analysis:

* **trips:** Contains detailed trip information such as pickup and dropoff locations, trip duration, and distance.
* **fares:**Includes fare-related data, including fare amount, tips, and payment methods.
* **drivers:** Stores information about the drivers, including IDs and metadata.
* **vehicles:** Holds data about the vehicles used for taxi services.
* **weather:** Integrates weather data relevant to the time and location of each trip to provide additional context.


## Functions
### Historical Data Fetching
**Function Name:** fetch_historical_data

* **Description:** This function fetches all historical Chicago taxi data up to the end of 2023. It utilizes Google Cloud Functions to extract data from the source, process it, and load it into BigQuery.
* **Execution:** This function is intended to run once to gather all historical data.
* Steps:
** __Extract:__ Connects to the data source and extracts historical taxi data.
** __Transform:__ Processes and cleans the data to ensure it is in the correct format for BigQuery.
** __Load:__ Loads the transformed data into the designated BigQuery table.

### Recurrent Data Update
**Function Name:** update_daily_data

* Description: This function updates the BigQuery table with the previous day's Chicago taxi data. It is designed to run recurrently, ensuring the dataset remains up-to-date.
* Execution: This function runs daily using Google Cloud Scheduler.
* __Steps:__
** __Extract:__ Fetches the previous day's taxi data.
** __Transform:__ Processes and cleans the data to ensure it is in the correct format for BigQuery.
** __Load:__ Appends the new data to the existing BigQuery table.

## Google Cloud Setup
* Google Cloud Functions
Both functions are implemented as Google Cloud Functions for scalable and serverless execution.

* BigQuery
BigQuery is used as the data warehouse where the taxi data is stored, processed, and queried.

* Cloud Scheduler
Cloud Scheduler triggers the update_daily_data function daily to ensure new data is fetched and integrated seamlessly.

