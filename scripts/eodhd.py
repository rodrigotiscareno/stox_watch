import requests
import json
import csv

import pandas as pd
from utility import get_tickers
from parse_csv import load_csv_to_sql

def fetch_sentiments():
    lowercase_ticker_list = [ticker.lower() for ticker in get_tickers(100)]
    result_string = ','.join(lowercase_ticker_list)
    # result_string = "TSLA"

    endpoint = f'https://eodhd.com/api/sentiments?s={result_string}&api_token=66746b7e20e902.29520100&fmt=json'

    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        print(data)
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}, {response.text}")
        

sentiments = fetch_sentiments()
# sentiments = {
#    "TSLA.US":[
#       {
#          "date":"2024-06-25",
#          "count":15,
#          "normalized":0.3612
#       },
#       {
#          "date":"2024-06-24",
#          "count":16,
#          "normalized":0.4279
#       },
#    ],
#    "APPL.US":[
#       {
#          "date":"2024-06-25",
#          "count":15,
#          "normalized":0.3612
#       },
#       {
#          "date":"2024-06-24",
#          "count":16,
#          "normalized":0.4279
#       },
#    ]
# }



data_to_write = json.loads(json.dumps(sentiments))

# Define the CSV file name
csv_file = "sentiments.csv"

# Write the data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["company", "date", "count", "normalized"])
    # Write the rows for each company
    for company, records in data_to_write.items():
        for entry in records:
            writer.writerow([company, entry["date"], entry["count"], entry["normalized"]])

print(f"Data has been written to {csv_file}")

# Convert each element to lowercase



