from flask import Flask, render_template, request
from ml_detector import detect_attack
import pandas as pd
from ml_soc_bridge import analyze_ml_sample
from healing import start_healing
from detector import detect_threat
from analyzer import analyze_threat
from remediation import remediate
from verifier import verify
import json
from datetime import datetime

app = Flask(__name__)


def load_logs():
    with open("sample_logs.json", "r") as file:
        return json.load(file)


def load_history():
    with open("incident_history.json", "r") as file:
        return json.load(file)


def save_incident(incident):
    history = load_history()

    for item in history:
        if (
            item["event"] == incident["event"]
            and item["source"] == incident["source"]
        ):
            return

    history.append(incident)

    with open("incident_history.json", "w") as file:
        json.dump(history, file, indent=4)


@app.route("/", methods=["GET"])
def home():

    logs = load_logs()

    selected_id = request.args.get("id", "2")

    try:
        selected_id = int(selected_id)
    except ValueError:
        selected_id = 2

    selected_log = next(
        (item for item in logs if item["id"] == selected_id),
        logs[1]
    )

    log = selected_log["event"]

    # Existing SOC analysis
    detection = detect_threat(log)

    analysis = analyze_threat(detection)

    remediation = remediate(detection["status"])

    verification = verify(remediation)

    if detection["status"] == "Normal":
        incident_status = "DETECTED -> ANALYZED -> NO ACTION REQUIRED"
    else:
        incident_status = "DETECTED -> ANALYZED -> REMEDIATED -> VERIFIED"

    # Existing dashboard counts
    normal_count = 0
    suspicious_count = 0
    malicious_count = 0

    for item in logs:

        result = detect_threat(item["event"])

        if result["status"] == "Normal":
            normal_count += 1

        elif result["status"] == "Suspicious":
            suspicious_count += 1

        elif result["status"] == "Malicious":
            malicious_count += 1

    # Save current incident
    incident = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": log,
        "source": selected_log["source"],
        "threat": detection["status"],
        "severity": analysis["severity"],
        "action": remediation["action"],
        "verification": verification["status"]
    }

    save_incident(incident)

    incident_history = load_history()

    # =========================================================
    # ML SELF-HEALING ANALYSIS
    # =========================================================

    ml_data = pd.read_csv(
        r"MachineLearningCVE/ml_test_samples.csv"
    )

    ml_results = []

    for i in range(len(ml_data)):

        row = ml_data.iloc[i]

        # ML detection + risk analysis
        soc_result = analyze_ml_sample(row)

        # Safe self-healing simulation
        healing_result = start_healing(
            soc_result["prediction"],
            soc_result["action"]
        )

        # Independent verification
        ml_verification = verify(healing_result)

        ml_results.append({
            "sample": i + 1,
            "prediction": soc_result["prediction"],
            "confidence": soc_result["confidence"],
            "risk_score": soc_result["risk_score"],
            "severity": soc_result["severity"],
            "action": soc_result["action"],
            "final_state": healing_result["final_state"],
            "healing_status": healing_result["healing_status"],
            "verification_status": ml_verification["status"]
        })

    # =========================================================
    # SEND DATA TO DASHBOARD
    # =========================================================

    return render_template(
        "index.html",
        logs=logs,
        log=log,
        detection=detection,
        analysis=analysis,
        remediation=remediation,
        verification=verification,
        incident_status=incident_status,
        normal_count=normal_count,
        suspicious_count=suspicious_count,
        malicious_count=malicious_count,
        selected_id=selected_log["id"],
        incident_history=incident_history,
        ml_results=ml_results
    )


@app.route("/ml-test", methods=["GET"])
def ml_test():

    data = pd.read_csv(
        r"MachineLearningCVE/ml_test_samples.csv"
    )

    results = []

    for i in range(len(data)):

        row = data.iloc[i]

        # ML detection + risk analysis
        soc_result = analyze_ml_sample(row)

        # Self-healing simulation
        healing_result = start_healing(
            soc_result["prediction"],
            soc_result["action"]
        )

        # Independent verification
        verification_result = verify(healing_result)

        results.append({
            "sample": i + 1,

            "actual": soc_result["actual"],
            "prediction": soc_result["prediction"],
            "confidence": soc_result["confidence"],

            "risk_score": soc_result["risk_score"],
            "severity": soc_result["severity"],
            "action": soc_result["action"],

            "initial_state": healing_result["initial_state"],
            "response_state": healing_result.get("response_state"),
            "recovery_state": healing_result.get("recovery_state"),
            "final_state": healing_result["final_state"],
            "healing_status": healing_result["healing_status"],

            "verification_status": verification_result["status"],
            "verification_message": verification_result["message"],
            "verified_state": verification_result["verified_state"]
        })

    return {
        "message": "ML Self-Healing SOC Agent Test",
        "samples": results
    }


if __name__ == "__main__":
    app.run(debug=True)