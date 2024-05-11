import configparser
import io
from datetime import datetime, timedelta
from hashlib import sha1

import pandas as pd
import requests
from elasticsearch import Elasticsearch
from tqdm import tqdm

# Define dataset url and the corresponding ES index
CSV_URL = "https://opendata-ajuntament.barcelona.cat/data/dataset/4f3ffbda-d5be-4f2a-a836-26a77be6df1a/resource/f627ac0a-d05f-416d-9773-eeb464a3fc44/download"
es_index = "la-ciutat-al-dia-num"

# Load dataset into pandas df
with requests.get(CSV_URL, stream=True) as r:
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.content.decode("utf-8")), low_memory=False)

# Consolidate last's week data. Comment out the following two lines to upload the entire dataset.
time_delta = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
df = df[df["Data_Indicador"] > time_delta]

# Sanity checks cleanup on the data
# 1. Drop NaN values from Value column
df = df[df["Valor"].notna()]
# 2. Repopulate NaN values in text fields
for index, row in df.iterrows():
    if pd.isna(row["Nom_Variable"]):
        df.at[index, "Nom_Variable"] = row["Nom_Indicador"]

# Authenticate to ES
config = configparser.ConfigParser()
config.read("es-token.ini")
es = Elasticsearch(
    cloud_id=config["ELASTIC"]["cloud_id"],
    basic_auth=(config["ELASTIC"]["user"], config["ELASTIC"]["password"]),
)
es.info()

print(f"Uploading {len(df)} rows to Elasticsearch...")

try:
    # Fill payload with df information and push to ES
    for _, row in tqdm(df.iterrows(), total=len(df)):
        payload = row.to_dict()
        unique_id = sha1(
            f"{payload['Data_Indicador']}/{payload['Nom_Indicador']}/{payload['Nom_Variable']}".encode(
                "utf-8"
            )
        ).hexdigest()
        es.index(index=es_index, document=payload, id=unique_id)

    # Refresh index
    es.indices.refresh(index=es_index)
    print(f"Upload completed successfully!")

except elasticsearch.ElasticsearchException as e:
    print(f"An error occurred: {e}")
