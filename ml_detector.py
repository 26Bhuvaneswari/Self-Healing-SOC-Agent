import pandas as pd
import joblib
import numpy as np

MODEL_PATH = "soc_ml_model.pkl"

# Load trained ML model
model = joblib.load(MODEL_PATH)


def detect_attack(features):
    """
    Predict whether the network event is benign or an attack.
    """

    # Convert input to DataFrame
    data = pd.DataFrame([features])

    # Clean numeric values
    data = data.apply(pd.to_numeric, errors="coerce")
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.fillna(0)

    # Prediction
    prediction = model.predict(data)[0]

    # Confidence
    probabilities = model.predict_proba(data)[0]
    confidence = float(max(probabilities))

    if prediction == 1:
        result = "Attack"
    else:
        result = "Benign"

    return {
        "prediction": result,
        "confidence": round(confidence * 100, 2)
    }


if __name__ == "__main__":
    print("ML Detector loaded successfully.")
    print("Model:", MODEL_PATH)