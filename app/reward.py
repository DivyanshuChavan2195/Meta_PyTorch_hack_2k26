def compute_reward(task, observation, action: str, action_cost: float = 0.0):
    truth = task["ground_truth"]
    risk = observation.risk_level

    # Default
    reward = -0.05
    reason = "Minor step cost."

    if action == "VERIFY":
        if observation.verifier_confidence < 0.7:
            reward = 0.4
            reason = "Good choice: verification under uncertainty."
        else:
            reward = -0.1
            reason = "Unnecessary verification."

    elif action == "DEFER":
        if observation.evidence_count < 2:
            reward = 0.2
            reason = "Reasonable to defer with limited evidence."
        else:
            reward = -0.2
            reason = "Too much deferring."

    elif action == "ESCALATE":
        if risk == "high" and 0.3 <= observation.verifier_confidence <= 0.7:
            reward = 0.6
            reason = "Escalation appropriate for high-risk ambiguity."
        else:
            reward = -0.3
            reason = "Unnecessary escalation."

    elif action == "ACCEPT":
        if truth == "true":
            reward = 1.0
            reason = "Correctly accepted a true claim."
        elif truth == "uncertain" and observation.verifier_confidence > 0.75:
            reward = 0.8
            reason = "Accepted after strong supporting evidence."
        else:
            reward = -2.0
            reason = "Dangerous acceptance."

    elif action == "REJECT":
        if truth == "false":
            reward = 1.0
            reason = "Correctly rejected a false claim."
        elif truth == "uncertain" and observation.contradiction_score > 0.7:
            reward = 0.7
            reason = "Reasonable rejection under contradiction."
        else:
            reward = -1.5
            reason = "Rejected potentially true information."

    # Apply cost penalty (0.1 * action_cost)
    cost_penalty = 0.1 * action_cost
    final_reward = reward - cost_penalty

    return final_reward, reason