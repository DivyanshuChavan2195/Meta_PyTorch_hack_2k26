TASKS = {
    "easy_1": {
        "id": "easy_1",
        "difficulty": "easy",
        "claim_text": "NASA confirms asteroid impact next week.",
        "ground_truth": "false",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.20,
            "evidence_count": 1,
            "contradiction_score": 0.75,
            "verifier_confidence": 0.10
        },
        "verify_update": {
            "source_reliability": 0.25,
            "evidence_count": 3,
            "contradiction_score": 0.90,
            "verifier_confidence": 0.05
        }
    },

    "medium_1": {
        "id": "medium_1",
        "difficulty": "medium",
        "claim_text": "A 6.8 earthquake has hit Pune city center.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.45,
            "evidence_count": 1,
            "contradiction_score": 0.20,
            "verifier_confidence": 0.40
        },
        "verify_update": {
            "source_reliability": 0.70,
            "evidence_count": 4,
            "contradiction_score": 0.10,
            "verifier_confidence": 0.82
        }
    },

    "hard_1": {
        "id": "hard_1",
        "difficulty": "hard",
        "claim_text": "Hospital X is denying treatment to all patients after an outbreak.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.50,
            "evidence_count": 2,
            "contradiction_score": 0.45,
            "verifier_confidence": 0.48
        },
        "verify_update": {
            "source_reliability": 0.62,
            "evidence_count": 5,
            "contradiction_score": 0.35,
            "verifier_confidence": 0.58
        }
    }
}