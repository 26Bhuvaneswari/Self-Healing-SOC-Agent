from datetime import datetime


def start_healing(threat_status, action):
    """
    Safe virtual self-healing simulation.
    Does not modify the real computer.
    """

    if threat_status != "Attack":
        return {
            "initial_state": "HEALTHY",
            "action": "No Action",
            "final_state": "HEALTHY",
            "healing_status": "NOT REQUIRED",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    # Virtual endpoint state
    initial_state = "COMPROMISED"

    if action == "Simulated Isolation":
        response_state = "ISOLATED"
    elif action == "Simulated Block":
        response_state = "BLOCKED"
    else:
        response_state = "COMPROMISED"

    # Recovery simulation
    if response_state in ["ISOLATED", "BLOCKED"]:
        recovery_state = "RECOVERING"
        final_state = "RECOVERED"
        healing_status = "HEALED"
    else:
        recovery_state = response_state
        final_state = "UNRESOLVED"
        healing_status = "FAILED"

    return {
        "initial_state": initial_state,
        "response_state": response_state,
        "recovery_state": recovery_state,
        "final_state": final_state,
        "healing_status": healing_status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__ == "__main__":

    print("\n===== SELF-HEALING TEST =====\n")

    result = start_healing(
        "Attack",
        "Simulated Isolation"
    )

    print("Initial State :", result["initial_state"])
    print("Response State:", result["response_state"])
    print("Recovery State:", result["recovery_state"])
    print("Final State   :", result["final_state"])
    print("Healing       :", result["healing_status"])
    print("Time          :", result["timestamp"])