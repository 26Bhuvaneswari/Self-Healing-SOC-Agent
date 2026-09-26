from flask import Flask, render_template, request
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

    detection = detect_threat(log)

    analysis = analyze_threat(detection)

    remediation = remediate(detection["status"])

    verification = verify(remediation)

    if detection["status"] == "Normal":
        incident_status = "DETECTED -> ANALYZED -> NO ACTION REQUIRED"
    else:
        incident_status = "DETECTED -> ANALYZED -> REMEDIATED -> VERIFIED"

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
        incident_history=incident_history
    )


if __name__ == "__main__":
    app.run(debug=True)