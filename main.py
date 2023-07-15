from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os

DIRPATH = os.path.dirname(__file__)
ASSETSDIRPATH = os.path.join(DIRPATH, "assets")
ML_COMPONENTS = os.path.join(ASSETSDIRPATH, "dog_model.pkl")

app = FastAPI(
    title = 'Shelter Animals Outcome Prediction',
    version = '1.0',
    description = 'The possible outcome for animals in shelter depending on some parameters.'
)

class Item(BaseModel):
    age_in_days: float
    month: int
    day: int
    hour: int
    minute: int
    name: str
    year: int

# Load your model
with open(ML_COMPONENTS, "rb") as file:
    loaded_obj = pickle.load(file)

pipeline = loaded_obj["pipeline"]
model = loaded_obj["model"]

@app.get('/')
def read_root():
    return {"Hello": "Welcome to the Shelter Animals Outcome Prediction API. Please POST to /predict to use the API."}


# Apply preprocessing and prediction
@app.post('/predict')
def predict(item: Item):
    data = item.dict()
    data_preprocessed = pipeline.transform([list(data.values())])  # apply your preprocessing pipeline
    prediction = model.predict(data_preprocessed)  # model prediction
    return {'prediction': prediction}
