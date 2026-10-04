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
            "mode": "Simulation Only",
            "initial_state": "COMPROMISED",
            "response_state": "ISOLATED",
            "recovery_state": "RECOVERING",
            "final_state": "RECOVERED"
        }

    if threat_status == "Suspicious":
        return {
            "action": "Simulated Temporary Block",
            "result": "The suspicious source was marked for temporary blocking.",
            "reason": "Suspicious activity requires monitoring.",
            "mode": "Simulation Only",
            "initial_state": "COMPROMISED",
            "response_state": "BLOCKED",
            "recovery_state": "RECOVERING",
            "final_state": "RECOVERED"
        }

    return {
        "action": "No Action Required",
        "result": "The event was considered normal.",
        "reason": "No suspicious activity was detected.",
        "mode": "Simulation Only",
        "initial_state": "HEALTHY",
        "response_state": "HEALTHY",
        "recovery_state": "HEALTHY",
        "final_state": "HEALTHY"
    }