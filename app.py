import os
import sys

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi import FastAPI, File, UploadFile ,Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
import pymongo

from NetworkSecurity.utils.main_utils.utils import load_pickle
from fastapi.templating import Jinja2Templates
from NetworkSecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME


MONGO_DB_URL = os.environ['MONGO_DB_URL']

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)


database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful !!")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

templates = Jinja2Templates(directory="./template")

@app.post("/predict")
async def predict(request: Request ,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        print(df)

        preprocessor = load_pickle('final_model/preprocessor.pkl')
        final_model=load_pickle('final_model/model.pkl')

        network_model = NetworkModel(preprocessor=preprocessor,model=final_model)
        y_pred = network_model.predict(df)
        
        df['prediction'] = y_pred
        print(df.iloc[0])

        df.to_csv('prediction/output.csv',index=False)

        table_html = df.to_html(classes='table table-striped')
        print(y_pred)

        return 'Completer'
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)


