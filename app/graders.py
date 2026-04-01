def grade_episode(task, final_action: str, steps_taken: int) -> float:
    truth = task["ground_truth"]

    # Strong correct outcomes
    if truth == "false" and final_action == "REJECT":
        return 1.0 if steps_taken <= 2 else 0.8

    if truth == "true" and final_action == "ACCEPT":
        return 1.0 if steps_taken <= 2 else 0.8

    if truth == "uncertain":
        if final_action == "VERIFY":
            return 0.7
        if final_action == "ESCALATE":
            return 1.0
        if final_action == "DEFER":
            return 0.6
        if final_action in ["ACCEPT", "REJECT"]:
            return 0.4

    return 0.0