from collections import Counter, defaultdict
from typing import Any

from src.evaluator import CRITICAL_FAILURE_LABELS

REQUIRED_CASE_FIELDS = {
    "case_id",
    "task_type",
    "normalized_score",
    "safety_flag",
    "failure_labels",
    "dimension_scores",
}


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0

    return round(sum(values) / len(values), 2)


def _validate_case(
    case: dict[str, Any],
    index: int,
) -> None:
    missing = REQUIRED_CASE_FIELDS - case.keys()

    if missing:
        raise ValueError(
            f"Case at index {index} is missing fields: "
            f"{sorted(missing)}"
        )

    if not isinstance(case["case_id"], str):
        raise TypeError(
            f"case_id at index {index} must be a string"
        )

    if not isinstance(case["task_type"], str):
        raise TypeError(
            f"task_type at index {index} must be a string"
        )

    if not isinstance(
        case["normalized_score"],
        (int, float),
    ):
        raise TypeError(
            f"normalized_score at index {index} "
            "must be numeric"
        )

    if not isinstance(case["safety_flag"], bool):
        raise TypeError(
            f"safety_flag at index {index} "
            "must be boolean"
        )

    if not isinstance(case["failure_labels"], list):
        raise TypeError(
            f"failure_labels at index {index} "
            "must be a list"
        )

    if not isinstance(case["dimension_scores"], dict):
        raise TypeError(
            f"dimension_scores at index {index} "
            "must be a dictionary"
        )


def _dimension_means(
    cases: list[dict[str, Any]],
) -> dict[str, float]:
    dimension_names = sorted(
        {
            dimension
            for case in cases
            for dimension in case["dimension_scores"]
        }
    )

    means = {}

    for dimension in dimension_names:
        values = [
            float(case["dimension_scores"][dimension])
            for case in cases
            if dimension in case["dimension_scores"]
        ]

        means[dimension] = _mean(values)

    return means


def analyze_slices(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    if not results:
        return {
            "case_count": 0,
            "overall_mean_score": 0.0,
            "slice_count": 0,
            "slices": {},
        }

    for index, case in enumerate(results):
        _validate_case(case, index)

    overall_mean_score = _mean(
        [
            float(case["normalized_score"])
            for case in results
        ]
    )

    grouped = defaultdict(list)

    for case in results:
        grouped[case["task_type"]].append(case)

    slices = {}

    for task_type in sorted(grouped):
        cases = grouped[task_type]
        case_count = len(cases)

        failure_counts = Counter(
            label
            for case in cases
            for label in case["failure_labels"]
        )

        total_failures = sum(
            failure_counts.values()
        )

        cases_with_failures = sum(
            bool(case["failure_labels"])
            for case in cases
        )

        safety_flag_count = sum(
            case["safety_flag"]
            for case in cases
        )

        critical_failure_counts = {
            label: count
            for label, count in sorted(
                failure_counts.items()
            )
            if label in CRITICAL_FAILURE_LABELS
        }

        critical_failure_cases = [
            case["case_id"]
            for case in cases
            if set(case["failure_labels"])
            & CRITICAL_FAILURE_LABELS
        ]

        mean_score = _mean(
            [
                float(case["normalized_score"])
                for case in cases
            ]
        )

        slices[task_type] = {
            "case_count": case_count,
            "case_ids": [
                case["case_id"]
                for case in cases
            ],
            "mean_score": mean_score,
            "delta_vs_overall_score": round(
                mean_score - overall_mean_score,
                2,
            ),
            "cases_with_failures": cases_with_failures,
            "failure_case_rate_pct": round(
                cases_with_failures
                / case_count
                * 100,
                2,
            ),
            "total_failure_occurrences": total_failures,
            "failures_per_case": round(
                total_failures / case_count,
                2,
            ),
            "safety_flag_count": safety_flag_count,
            "safety_flag_rate_pct": round(
                safety_flag_count
                / case_count
                * 100,
                2,
            ),
            "critical_failure_occurrences": sum(
                critical_failure_counts.values()
            ),
            "critical_failure_counts": (
                critical_failure_counts
            ),
            "critical_failure_cases": (
                critical_failure_cases
            ),
            "failure_counts": dict(
                sorted(failure_counts.items())
            ),
            "dimension_mean_scores": (
                _dimension_means(cases)
            ),
            "small_slice_warning": case_count < 3,
        }

    return {
        "case_count": len(results),
        "overall_mean_score": overall_mean_score,
        "slice_count": len(slices),
        "slices": slices,
    }