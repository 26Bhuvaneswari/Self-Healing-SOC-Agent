import pandas as pd
from ml_detector import detect_attack


def analyze_ml_sample(row):
    """
    Convert one CICIDS2017 row into an SOC-friendly result.
    """

    actual_target = int(row["Target"])

    features = row.drop(labels=["Target"]).to_dict()

    ml_result = detect_attack(features)

    prediction = ml_result["prediction"]
    confidence = ml_result["confidence"]

    # Risk calculation
    if prediction == "Attack":
        if confidence >= 90:
            severity = "High"
            risk_score = 90
        elif confidence >= 70:
            severity = "Medium"
            risk_score = 70
        else:
            severity = "Low"
            risk_score = 50
    else:
        severity = "Low"
        risk_score = 10

    # Agent decision
    if prediction == "Attack" and severity == "High":
        action = "Simulated Isolation"
    elif prediction == "Attack":
        action = "Simulated Block"
    else:
        action = "No Action"

    # Ground truth only for testing
    actual = "Attack" if actual_target == 1 else "Benign"

    return {
        "actual": actual,
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": risk_score,
        "severity": severity,
        "action": action
    }


if __name__ == "__main__":

    data_path = r"MachineLearningCVE\ml_test_samples.csv"

    df = pd.read_csv(data_path)

    print("\n===== ML SOC BRIDGE TEST =====\n")

    for i in range(5):
        result = analyze_ml_sample(df.iloc[i])

        print(f"Sample {i + 1}")
        print("Actual     :", result["actual"])
        print("Prediction :", result["prediction"])
        print("Confidence :", result["confidence"], "%")
        print("Risk Score :", result["risk_score"])
        print("Severity   :", result["severity"])
        print("Action     :", result["action"])
        print("-" * 40)