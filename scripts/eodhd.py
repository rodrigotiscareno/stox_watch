import requests
import json
import csv

import pandas as pd
from utility import get_tickers
from parse_csv import load_csv_to_sql


def fetch_and_save_sentiments():

    lowercase_ticker_list = [ticker.lower() for ticker in get_tickers(100)]
    result_string = ','.join(lowercase_ticker_list)
    endpoint = f'https://eodhd.com/api/sentiments?s={result_string}&api_token=66746b7e20e902.29520100&fmt=json'

    response = requests.get(endpoint)

    if response.status_code == 200:
        sentiments = response.json()  # Parse JSON response
    else:
        print(f"Failed to retrieve data: {response.status_code}, {response.text}")
        
    data_to_write = json.loads(json.dumps(sentiments))

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
    
    load_csv_to_sql("sentiments.csv", "sentiments")
        


if __name__ == "__main__":
    fetch_and_save_sentiments()



