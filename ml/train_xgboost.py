import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


# Load dataset
df = pd.read_csv("../datasets/accident_risk_dataset.csv")

print("Dataset Shape:")
print(df.shape)

# Features
X = df.drop("accident_risk", axis=1)

# Target
y = df["accident_risk"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Model...")

# XGBoost Model
model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(round(accuracy * 100, 2), "%")

# Save model
joblib.dump(
    model,
    "models/accident_predictor_xgboost.pkl"
)

print("\nModel Saved Successfully")
print("models/accident_predictor_xgboost.pkl")