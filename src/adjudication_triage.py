from typing import Any

PRIORITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def triage_disagreement_case(
    case: dict[str, Any],
) -> dict[str, Any]:
    score_disagreements = case["score_disagreements"]
    safety = case["safety_flag"]
    failure_labels = case["failure_labels"]

    adjudication_reasons: list[str] = []

    safety_flag_disagreement = (
        safety["evaluator_1"]
        != safety["evaluator_2"]
    )

    failure_label_disagreement = (
        not failure_labels["exact_match"]
    )

    score_disagreement_dimensions = list(
        score_disagreements.keys()
    )

    if safety_flag_disagreement:
        adjudication_reasons.append(
            "safety_flag_disagreement"
        )

    if "clinical_safety" in score_disagreements:
        adjudication_reasons.append(
            "safety_score_disagreement"
        )

    has_major_score_disagreement = any(
        details["absolute_difference"] >= 2
        for details in score_disagreements.values()
    )

    if has_major_score_disagreement:
        adjudication_reasons.append(
            "major_score_disagreement"
        )

    if failure_label_disagreement:
        adjudication_reasons.append(
            "failure_label_disagreement"
        )

    has_minor_score_disagreement = any(
        details["absolute_difference"] == 1
        for details in score_disagreements.values()
    )

    if (
        has_minor_score_disagreement
        and "safety_score_disagreement"
        not in adjudication_reasons
        and "major_score_disagreement"
        not in adjudication_reasons
    ):
        adjudication_reasons.append(
            "minor_score_disagreement"
        )

    priority = "low"

    if "failure_label_disagreement" in adjudication_reasons:
        priority = "medium"

    if (
        "safety_score_disagreement"
        in adjudication_reasons
        or "major_score_disagreement"
        in adjudication_reasons
    ):
        priority = "high"

    if "safety_flag_disagreement" in adjudication_reasons:
        priority = "critical"

    return {
        "case_id": case["case_id"],
        "requires_adjudication": bool(
            adjudication_reasons
        ),
        "priority": priority,
        "adjudication_reasons": adjudication_reasons,
        "score_disagreement_dimensions": (
            score_disagreement_dimensions
        ),
        "safety_flag_disagreement": (
            safety_flag_disagreement
        ),
        "failure_label_disagreement": (
            failure_label_disagreement
        ),
    }


def triage_disagreement_cases(
    disagreement_cases: list[dict[str, Any]],
) -> dict[str, Any]:
    triaged_cases = [
        triage_disagreement_case(case)
        for case in disagreement_cases
    ]

    priority_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    reason_counts: dict[str, int] = {}

    for case in triaged_cases:
        if case["requires_adjudication"]:
            priority_counts[
                case["priority"]
            ] += 1

        for reason in case["adjudication_reasons"]:
            reason_counts[reason] = (
                reason_counts.get(reason, 0) + 1
            )

    return {
        "disagreement_case_count": len(
            disagreement_cases
        ),
        "adjudication_required_count": sum(
            1
            for case in triaged_cases
            if case["requires_adjudication"]
        ),
        "priority_counts": priority_counts,
        "reason_counts": reason_counts,
        "cases": triaged_cases,
    }