import pandas as pd
import json
import requests
from pandas.io import gbq
import pandas_gbq
import io
import csv

'''
function 1: This is where you put your own code, as long as the output is a 
pandas dataframe you can write it out however you want.
'''

def get_api_data(event, context):
    # Define dataset url and the corresponding BigQuery Table name
    CSV_URL = 'https://opendata-ajuntament.barcelona.cat/data/dataset/4f3ffbda-d5be-4f2a-a836-26a77be6df1a/resource/f627ac0a-d05f-416d-9773-eeb464a3fc44/download'
    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')
        
    # Load dataset into pandas df
    df = pd.read_csv(io.StringIO(decoded_content), low_memory = False)

    # Sanity checks cleanup on the data
    ## 1. Drop NaN values from Value column
    df = df[df["Valor"].notna()]
    ## 2. Repopulate NaN values in text fields
    for index, row in df.iterrows():
        if pd.isna(row["Nom_Variable"]):
            df.at[index, "Nom_Variable"] = row["Nom_Indicador"]

    #We define a unique_id per row
    df['unique_id']= df.apply(lambda x: str(x["Data_Indicador"]) + "/" +  str(x["Nom_Indicador"]) + "/" + str(x["Nom_Variable"]) ,axis=1 )

    #bq_load function with the table_name
    bq_load('LaCiutatAlDia', df)  

'''
function 2: This function just converts your pandas dataframe into a bigquery table, 
you'll also need to designate the name and location of the table in the variable 
names below.
'''


def bq_load(key, value):
    # Define GCP project id, dataset name and get the table value from the function input.
    project_name = 'forcodesake'                     #We define the project id
    dataset_name = 'forcodesake.LaCiutatAlDia'       #We define the dataset name under the project id
    table_name = key                                 #We define the table name we want to create or replace 

    # Push the dataframe into BigQuery. If a table with the same name already exists, it will be replaced.
    value.to_gbq(destination_table='{}.{}'.format(dataset_name, table_name), project_id=project_name, if_exists='replace')
    return f'Success!'