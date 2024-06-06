import base64
import functions_framework
import requests
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from datetime import datetime

# Ensure the BigQuery client is initialized
client = bigquery.Client(project="coral-environs-414713")

def get_last_trip_start_timestamp(client, dataset_id: str = "chicago_taxis_data", table_name="rides_table"):
    query = f"""
        SELECT MAX(trip_start_timestamp) AS last_trip_start
        FROM `{client.project}.{dataset_id}.{table_name}`
    """
    query_job = client.query(query)
    results = query_job.result()  # Waits for the query to finish

    for row in results:
        return row.last_trip_start

    return None  # In case there are no rows

## API CALL FUNCTION
def get_data(start_date_time, limit: int = 1000, offset: int = 0):
    start_date_time_str = start_date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    url = "https://data.cityofchicago.org/resource/ajtu-isnz.json?$limit={0}&$offset={1}&$where=trip_start_timestamp>'{2}'".format(limit, offset, start_date_time_str)

    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)  # Simplified request call
        response.raise_for_status()  # This will raise an exception for 4XX and 5XX status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": True}  # Using a consistent error signaling in the response

def data_modeling(df: pd.DataFrame):
    # Datetimes are objects, need to be parsed as datetime. 
    df["trip_start_timestamp"] = pd.to_datetime(df["trip_start_timestamp"])
    df["trip_end_timestamp"] = pd.to_datetime(df["trip_end_timestamp"])

    ## DATA MODELING
    # PICKUP LOCATION
    pickup_location_dim = df[['pickup_community_area','pickup_centroid_latitude', 'pickup_centroid_longitude']].drop_duplicates().reset_index(drop=True)
    pickup_location_dim['pickup_location_id'] = pickup_location_dim.drop_duplicates().index
    pickup_location_dim

    # DROPOF LOCATION
    dropoff_location_dim = df[['dropoff_community_area','dropoff_centroid_latitude', 'dropoff_centroid_longitude']].drop_duplicates().reset_index(drop=True)
    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.drop_duplicates().index
    dropoff_location_dim

    # COMPANY NAME
    company_type_dim = df[['company']].drop_duplicates().reset_index(drop=True)
    company_type_dim['company_id'] = company_type_dim.index
    company_type_dim

    # PAYMENT TYPE
    payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
    payment_type_dim['payment_id'] = payment_type_dim.index
    payment_type_dim

    # RIDES TABLE
    rides_table = df[["trip_id", "taxi_id", "trip_start_timestamp", "trip_end_timestamp", "trip_seconds", "trip_miles", 
                    "fare", "tips", "tolls", "extras", "trip_total", "payment_type", "company", 
                    "pickup_community_area","pickup_centroid_latitude", "pickup_centroid_longitude",
                    "dropoff_community_area","dropoff_centroid_latitude", "dropoff_centroid_longitude",
                    ]]

    rides_table = pd.merge(rides_table, pickup_location_dim, 
                    left_on=['pickup_community_area', 'pickup_centroid_latitude', 'pickup_centroid_longitude'],
                    right_on=['pickup_community_area', 'pickup_centroid_latitude', 'pickup_centroid_longitude'],
                    how='left')

    rides_table = pd.merge(rides_table, dropoff_location_dim, 
                    left_on=['dropoff_community_area', 'dropoff_centroid_latitude', 'dropoff_centroid_longitude'],
                    right_on=['dropoff_community_area', 'dropoff_centroid_latitude', 'dropoff_centroid_longitude'],
                    how='left')

    rides_table = pd.merge(rides_table, payment_type_dim, 
                    left_on=['payment_type'],
                    right_on=['payment_type'],
                    how='left')

    rides_table = pd.merge(rides_table, company_type_dim, 
                    left_on=['company'],
                    right_on=['company'],
                    how='left')

    rides_table = rides_table.drop(columns=["pickup_community_area", "pickup_centroid_latitude", "pickup_centroid_longitude", "dropoff_community_area", "dropoff_centroid_latitude", "dropoff_centroid_longitude"])
    
    return {"pickup_location_dim":pickup_location_dim, "dropoff_location_dim": dropoff_location_dim,  "company_type_dim":company_type_dim, "payment_type_dim": payment_type_dim, "rides_table": rides_table}

# Function to load dataframe to BigQuery
def load_df_to_bigquery(client, dictionary: dict, dataset_id: str = "chicago_taxis_data"):
    print("BQ TIME!")
    for table_name, df in dictionary.items():
        print(f"Processing table {table_name}")
        table_full_path = f"{client.project}.{dataset_id}.{table_name}"
        
        # Check if the table exists
        try:
            client.get_table(table_full_path)  # Make an API request.
            print(f"Table {table_name} exists, appending data.")
            job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND,)
            # Load the dataframe to BigQuery
            job = client.load_table_from_dataframe(df, table_full_path, job_config=job_config)
            job.result()  # Wait for the job to complete

        except NotFound:
            print(f"Table {table_name} does not exist, creating and loading data.")
            # Create the new data
            job = client.load_table_from_dataframe(df, table_full_path)
            job.result()  # Wait for the job to complete

        print(f"Table {table_name} loaded successfully.")


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    ## RETREIVING DATA
    data = []
    limit = 100000
    offset = 0
    start_date_time = get_last_trip_start_timestamp(client)
    while True: 
        data_batch = get_data(start_date_time, limit=limit, offset=offset)
        if "error" in data_batch:
            print("API call failed or finished.")
            break

        if not data_batch:  # Checking for empty response
            print("No more data to fetch.")
            break

        data.extend(data_batch)
        offset += limit

    if not data:
        return("No data retrieved.")
    else:
        try:
            output = data_modeling(pd.json_normalize(data))
            load_df_to_bigquery(client, output)
            return("Data modeling succeeded!")
        except Exception as e:
            return(f"Data modeling failed: {e}")
