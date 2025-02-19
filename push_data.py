import os
import json
import sys
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from NetworkSecurity.exception.exception import NetworkSecurityException

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.environ['MONGO_DB_URL']
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            # Debugging: Check if file path is valid
            print(f"File path type: {type(file_path)}, value: {file_path}")

            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = self.mongo_client[self.database]  # Get database
            collection = db[self.collection]  # Get collection

            collection.insert_many(self.records)  # Insert records
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    File_Path = 'Network_Data/phisingData.csv'  # Ensure this is a string, not a tuple
    database = 'NetworkData'
    collection = 'PhishingData'  # Fixed typo ('PhisingData' → 'PhishingData')

    extract_data = NetworkDataExtract()

    # Convert CSV to JSON
    records = extract_data.csv_to_json_convertor(file_path=File_Path)

    # Insert into MongoDB
    count = extract_data.insert_data_mongodb(records, database, collection)
    print(f"Inserted {count} records into MongoDB.")
