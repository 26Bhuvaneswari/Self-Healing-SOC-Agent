def analyze_threat(detection_result):
    status = detection_result["status"]

    if status == "Malicious":
        return {
            "severity": "High",
            "explanation": detection_result["reason"],
            "action": "Immediate safe containment is recommended."
        }

    if status == "Suspicious":
        return {
            "severity": "Medium",
            "explanation": detection_result["reason"],
            "action": "Monitor the event and simulate containment."
        }

    return {
        "severity": "Low",
        "explanation": detection_result["reason"],
        "action": "No remediation required."
    }