TASKS = {
    # EASY - FALSE CLAIMS (obvious)
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

    "easy_2": {
        "id": "easy_2",
        "difficulty": "easy",
        "claim_text": "World ends tomorrow according to astrology.",
        "ground_truth": "false",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.15,
            "evidence_count": 0,
            "contradiction_score": 0.85,
            "verifier_confidence": 0.08
        },
        "verify_update": {
            "source_reliability": 0.10,
            "evidence_count": 1,
            "contradiction_score": 0.95,
            "verifier_confidence": 0.02
        }
    },

    "easy_3": {
        "id": "easy_3",
        "difficulty": "easy",
        "claim_text": "Vaccines cause magnetism (debunked).",
        "ground_truth": "false",
        "risk_level": "medium",
        "initial_signals": {
            "source_reliability": 0.25,
            "evidence_count": 1,
            "contradiction_score": 0.80,
            "verifier_confidence": 0.12
        },
        "verify_update": {
            "source_reliability": 0.20,
            "evidence_count": 2,
            "contradiction_score": 0.88,
            "verifier_confidence": 0.08
        }
    },

    # EASY - TRUE CLAIMS (obvious)
    "easy_4": {
        "id": "easy_4",
        "difficulty": "easy",
        "claim_text": "Water boils at 100 degrees Celsius at sea level.",
        "ground_truth": "true",
        "risk_level": "low",
        "initial_signals": {
            "source_reliability": 0.95,
            "evidence_count": 5,
            "contradiction_score": 0.05,
            "verifier_confidence": 0.98
        },
        "verify_update": {
            "source_reliability": 0.98,
            "evidence_count": 8,
            "contradiction_score": 0.02,
            "verifier_confidence": 0.99
        }
    },

    "easy_5": {
        "id": "easy_5",
        "difficulty": "easy",
        "claim_text": "Paris is the capital of France.",
        "ground_truth": "true",
        "risk_level": "low",
        "initial_signals": {
            "source_reliability": 0.98,
            "evidence_count": 4,
            "contradiction_score": 0.01,
            "verifier_confidence": 0.99
        },
        "verify_update": {
            "source_reliability": 0.99,
            "evidence_count": 6,
            "contradiction_score": 0.00,
            "verifier_confidence": 0.99
        }
    },

    # MEDIUM - UNCERTAIN CLAIMS
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

    "medium_2": {
        "id": "medium_2",
        "difficulty": "medium",
        "claim_text": "Tech company X is being acquired by Tech company Y.",
        "ground_truth": "uncertain",
        "risk_level": "medium",
        "initial_signals": {
            "source_reliability": 0.50,
            "evidence_count": 2,
            "contradiction_score": 0.30,
            "verifier_confidence": 0.45
        },
        "verify_update": {
            "source_reliability": 0.72,
            "evidence_count": 5,
            "contradiction_score": 0.15,
            "verifier_confidence": 0.80
        }
    },

    "medium_3": {
        "id": "medium_3",
        "difficulty": "medium",
        "claim_text": "A new disease variant is spreading in Region Z.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.55,
            "evidence_count": 2,
            "contradiction_score": 0.35,
            "verifier_confidence": 0.50
        },
        "verify_update": {
            "source_reliability": 0.68,
            "evidence_count": 4,
            "contradiction_score": 0.25,
            "verifier_confidence": 0.75
        }
    },

    # HARD - UNCERTAIN / RISKY CLAIMS
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
    },

    "hard_2": {
        "id": "hard_2",
        "difficulty": "hard",
        "claim_text": "Political figure Z received undisclosed payments.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.48,
            "evidence_count": 3,
            "contradiction_score": 0.40,
            "verifier_confidence": 0.50
        },
        "verify_update": {
            "source_reliability": 0.60,
            "evidence_count": 6,
            "contradiction_score": 0.30,
            "verifier_confidence": 0.65
        }
    },

    "hard_3": {
        "id": "hard_3",
        "difficulty": "hard",
        "claim_text": "Environmental disaster reported in coastal region.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.52,
            "evidence_count": 2,
            "contradiction_score": 0.42,
            "verifier_confidence": 0.48
        },
        "verify_update": {
            "source_reliability": 0.68,
            "evidence_count": 5,
            "contradiction_score": 0.32,
            "verifier_confidence": 0.72
        }
    },

    "hard_4": {
        "id": "hard_4",
        "difficulty": "hard",
        "claim_text": "Research breakthrough claims cure for disease W.",
        "ground_truth": "uncertain",
        "risk_level": "high",
        "initial_signals": {
            "source_reliability": 0.55,
            "evidence_count": 3,
            "contradiction_score": 0.38,
            "verifier_confidence": 0.52
        },
        "verify_update": {
            "source_reliability": 0.70,
            "evidence_count": 6,
            "contradiction_score": 0.28,
            "verifier_confidence": 0.75
        }
    },

    # ADDITIONAL MEDIUM - FALSE CLAIMS
    "medium_4": {
        "id": "medium_4",
        "difficulty": "medium",
        "claim_text": "Celebrity X admitted to secret scandal.",
        "ground_truth": "false",
        "risk_level": "medium",
        "initial_signals": {
            "source_reliability": 0.35,
            "evidence_count": 1,
            "contradiction_score": 0.65,
            "verifier_confidence": 0.25
        },
        "verify_update": {
            "source_reliability": 0.30,
            "evidence_count": 2,
            "contradiction_score": 0.75,
            "verifier_confidence": 0.18
        }
    },

    # ADDITIONAL MEDIUM - TRUE CLAIMS
    "medium_5": {
        "id": "medium_5",
        "difficulty": "medium",
        "claim_text": "Scientific study shows X reduces risk of Y.",
        "ground_truth": "true",
        "risk_level": "low",
        "initial_signals": {
            "source_reliability": 0.80,
            "evidence_count": 4,
            "contradiction_score": 0.10,
            "verifier_confidence": 0.85
        },
        "verify_update": {
            "source_reliability": 0.92,
            "evidence_count": 7,
            "contradiction_score": 0.05,
            "verifier_confidence": 0.95
        }
    },
}