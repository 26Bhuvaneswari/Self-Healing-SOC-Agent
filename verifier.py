def verify(healing_result):
    """
    Independently verifies whether the virtual endpoint
    successfully reached the RECOVERED state.
    """

    final_state = healing_result.get("final_state")

    if final_state == "RECOVERED":
        return {
            "status": "Verified",
            "message": "Endpoint recovery verified successfully.",
            "verified_state": final_state
        }

    if final_state == "HEALTHY":
        return {
            "status": "Not Required",
            "message": "Endpoint was already healthy.",
            "verified_state": final_state
        }

    return {
        "status": "Failed",
        "message": "Endpoint recovery could not be verified. Human review required.",
        "verified_state": final_state
    }


if __name__ == "__main__":

    print("\n===== VERIFICATION TEST =====\n")

    test_result = {
        "final_state": "RECOVERED"
    }

    result = verify(test_result)

    print("Verification :", result["status"])
    print("Message      :", result["message"])
    print("Verified State:", result["verified_state"])