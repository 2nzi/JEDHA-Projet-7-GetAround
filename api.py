import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import List, Union
from fastapi import FastAPI
import joblib


description = """
Welcome to the GetAround Car Value Prediction API. This app provides an endpoint to predict car values based on various features! Try it out 🕹️

## Machine Learning

This section includes a Machine Learning endpoint that predicts car values based on various features. Here is the endpoint:

* `/predict`: **POST** request that accepts a list of car features and returns a predicted car value.

Check out the documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Machine Learning",
        "description": "Endpoint for predicting car values based on provided features."
    }
]

app = FastAPI(
    title="🚗 GetAround Car Value Prediction API",
    description=description,
    version="0.1",
    contact={
        "name": "Antoine VERDON",
        "email": "antoineverdon.pro@gmail.com",  # Replace with actual email
    },
    openapi_tags=tags_metadata
)


class PredictionFeatures(BaseModel):
    CarData: List[Union[str, int, bool]] = ["Renault", 193231, 85, "diesel", "black", "estate", False, True, False, False, False, False, True]

@app.get("/", tags=["Introduction Endpoints"])
async def index():
    return "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the API at `/docs`"

@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    columns = [
        'model_key', 'mileage', 'engine_power', 'fuel', 'paint_color',
        'car_type', 'private_parking_available', 'has_gps',
        'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
        'has_speed_regulator', 'winter_tires'
    ]
    
    car_data_dict = {col: [val] for col, val in zip(columns, predictionFeatures.CarData)}
    car_data = pd.DataFrame(car_data_dict)
    loaded_model = joblib.load('best_model_XGBoost.pkl')
    prediction = loaded_model.predict(car_data)
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
