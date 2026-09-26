def remediate(threat_status):
    """
    Performs safe simulated remediation.
    No real system changes are made.
    """

    if threat_status == "Malicious":
        return {
            "action": "Simulated Isolation",
            "result": "The suspicious endpoint was marked for isolation.",
            "reason": "High-severity malicious activity was detected.",
            "mode": "Simulation Only"
        }

    if threat_status == "Suspicious":
        return {
            "action": "Simulated Temporary Block",
            "result": "The suspicious source was marked for temporary blocking.",
            "reason": "Suspicious activity requires monitoring.",
            "mode": "Simulation Only"
        }

    return {
        "action": "No Action Required",
        "result": "The event was considered normal.",
        "reason": "No suspicious activity was detected.",
        "mode": "Simulation Only"
    }