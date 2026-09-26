def detect_threat(log):
    """
    Simple rule-based SOC threat detector.
    """

    event = log.lower()

    # Malicious activity
    if "malware" in event or "ransomware" in event:
        return {
            "status": "Malicious",
            "reason": "Malware or ransomware activity was detected."
        }

    if "unauthorized access" in event:
        return {
            "status": "Malicious",
            "reason": "Unauthorized access activity was detected."
        }

    # Suspicious activity
    if "failed login" in event or "multiple login failures" in event:
        return {
            "status": "Suspicious",
            "reason": "Multiple failed login attempts were detected."
        }

    if "port scan" in event or "port scanning" in event:
        return {
            "status": "Suspicious",
            "reason": "Possible port scanning activity was detected."
        }

    # Normal activity
    return {
        "status": "Normal",
        "reason": "No suspicious activity was detected."
    }