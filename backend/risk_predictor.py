import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "ml",
    "models",
    "accident_predictor_xgboost.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_accident_risk(
    hour,
    day_of_week,
    traffic_density,
    rainfall,
    visibility,
    speed_avg,
    junction_score
):
    data = pd.DataFrame([{
        "hour": hour,
        "day_of_week": day_of_week,
        "traffic_density": traffic_density,
        "rainfall": rainfall,
        "visibility": visibility,
        "speed_avg": speed_avg,
        "junction_score": junction_score
    }])

    prediction = model.predict(data)[0]

    return int(prediction)