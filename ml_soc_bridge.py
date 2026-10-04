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

        action = "Simulated Isolation" if severity == "High" else "Simulated Block"

    else:
        risk_score = 0
        severity = "Low"
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