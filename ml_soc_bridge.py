import pandas as pd
from ml_detector import detect_attack


def analyze_ml_sample(row):
    actual_target = int(row["Target"])

    features = row.drop(labels=["Target"]).to_dict()

    ml_result = detect_attack(features)

    prediction = ml_result["prediction"]
    confidence = ml_result["confidence"]

    if prediction == "Attack":
        risk_score = round(confidence)

        if risk_score >= 90:
            severity = "High"
        elif risk_score >= 70:
            severity = "Medium"
        else:
            severity = "Low"

    else:
        risk_score = round(100 - confidence)

        if risk_score >= 70:
            severity = "High"
        elif risk_score >= 30:
            severity = "Medium"
        else:
            severity = "Low"

    if prediction == "Attack" and severity == "High":
        action = "Simulated Isolation"
    elif prediction == "Attack":
        action = "Simulated Block"
    else:
        action = "No Action"

    actual = "Attack" if actual_target == 1 else "Benign"

    return {
        "actual": actual,
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": risk_score,
        "severity": severity,
        "action": action
    }