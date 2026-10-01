from collections import Counter

from src.evaluator import CRITICAL_FAILURE_LABELS


def analyze_results(results):
    case_count = len(results)

    failure_counts = Counter(
        label
        for case in results
        for label in case.get("failure_labels", [])
    )

    cases_with_failures = sum(
        bool(case.get("failure_labels"))
        for case in results
    )

    safety_flagged_cases = [
        case["case_id"]
        for case in results
        if case.get("safety_flag", False)
    ]

    mean_score = round(
        sum(case["normalized_score"] for case in results)
        / case_count,
        2,
    )

    failure_prevalence_pct = {
        label: round((count / case_count) * 100, 2)
        for label, count in sorted(failure_counts.items())
    }

    minimum_score = min(
        case["normalized_score"]
        for case in results
    )

    lowest_scoring_cases = [
        {
            "case_id": case["case_id"],
            "normalized_score": case["normalized_score"],
        }
        for case in results
        if case["normalized_score"] == minimum_score
    ]

    critical_failure_counts = {
        label: count
        for label, count in sorted(failure_counts.items())
        if label in CRITICAL_FAILURE_LABELS
    }

    noncritical_failure_counts = {
        label: count
        for label, count in sorted(failure_counts.items())
        if label not in CRITICAL_FAILURE_LABELS
    }

    critical_failure_cases = [
        case["case_id"]
        for case in results
        if set(case.get("failure_labels", []))
        & CRITICAL_FAILURE_LABELS
    ]

    dimension_names = sorted(
        {
            dimension
            for case in results
            for dimension in case.get(
                "dimension_scores",
                {},
            )
        }
    )

    dimension_mean_scores = {}

    for dimension in dimension_names:
        values = [
            case["dimension_scores"][dimension]
            for case in results
            if dimension
            in case.get("dimension_scores", {})
        ]

        dimension_mean_scores[dimension] = round(
            sum(values) / len(values),
            2,
        )

    return {
        "case_count": case_count,
        "cases_with_failures": cases_with_failures,
        "cases_without_failures": (
            case_count - cases_with_failures
        ),
        "total_failure_occurrences": sum(
            failure_counts.values()
        ),
        "safety_flag_count": len(
            safety_flagged_cases
        ),
        "failure_counts": dict(
            sorted(failure_counts.items())
        ),
        "safety_flagged_cases": safety_flagged_cases,
        "mean_score": mean_score,
        "failure_prevalence_pct": (
            failure_prevalence_pct
        ),
        "lowest_scoring_cases": lowest_scoring_cases,
        "critical_failure_counts": (
            critical_failure_counts
        ),
        "noncritical_failure_counts": (
            noncritical_failure_counts
        ),
        "critical_failure_cases": (
            critical_failure_cases
        ),
        "dimension_mean_scores": (
            dimension_mean_scores
        ),
    }
