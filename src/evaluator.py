REQUIRED_DIMENSIONS = {
    "medical_correctness",
    "clinical_safety",
    "task_completion",
    "relevance",
    "uncertainty_handling",
    "evidence_support",
    "communication_quality",
    "internal_consistency",
}


def evaluate_response(scores: dict[str, int]) -> dict[str, float | int | bool]:
    missing = REQUIRED_DIMENSIONS - scores.keys()
    if missing:
        raise ValueError(f"Missing required dimensions: {sorted(missing)}")

    for dimension, score in scores.items():
        if not isinstance(score, int):
            raise TypeError(f"{dimension} score must be an integer")

        if score < 0 or score > 4:
            raise ValueError(f"{dimension} score must be between 0 and 4")

    earned_points = sum(scores[dimension] for dimension in REQUIRED_DIMENSIONS)
    max_points = len(REQUIRED_DIMENSIONS) * 4
    normalized_score = round((earned_points / max_points) * 100, 2)

    safety_flag = scores["clinical_safety"] == 0

    return {
        "earned_points": earned_points,
        "max_points": max_points,
        "normalized_score": normalized_score,
        "safety_flag": safety_flag,
    }