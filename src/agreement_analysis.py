from collections import defaultdict
from typing import Any

from src.evaluator import REQUIRED_DIMENSIONS


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0

    return round(
        sum(values) / len(values),
        4,
    )


def _label_jaccard(
    labels_a: list[str],
    labels_b: list[str],
) -> float:
    set_a = set(labels_a)
    set_b = set(labels_b)

    if not set_a and not set_b:
        return 1.0

    union = set_a | set_b

    if not union:
        return 1.0

    return round(
        len(set_a & set_b) / len(union),
        4,
    )


def analyze_agreement(
    evaluator_1: list[dict[str, Any]],
    evaluator_2: list[dict[str, Any]],
) -> dict[str, Any]:
    eval1_by_id = {
        case["case_id"]: case
        for case in evaluator_1
    }

    eval2_by_id = {
        case["case_id"]: case
        for case in evaluator_2
    }

    if set(eval1_by_id) != set(eval2_by_id):
        raise ValueError(
            "Evaluator case IDs do not match"
        )

    case_ids = sorted(eval1_by_id)

    dimension_exact_matches = defaultdict(int)
    dimension_absolute_differences = defaultdict(list)

    safety_exact_matches = 0

    label_exact_matches = 0
    label_jaccard_scores: list[float] = []

    disagreement_cases = []

    for case_id in case_ids:
        case_1 = eval1_by_id[case_id]
        case_2 = eval2_by_id[case_id]

        score_disagreements = {}

        for dimension in REQUIRED_DIMENSIONS:
            score_1 = case_1["dimension_scores"][dimension]
            score_2 = case_2["dimension_scores"][dimension]

            difference = abs(
                score_1 - score_2
            )

            dimension_absolute_differences[
                dimension
            ].append(difference)

            if score_1 == score_2:
                dimension_exact_matches[
                    dimension
                ] += 1
            else:
                score_disagreements[
                    dimension
                ] = {
                    "evaluator_1": score_1,
                    "evaluator_2": score_2,
                    "absolute_difference": difference,
                }

        safety_1 = case_1["safety_flag"]
        safety_2 = case_2["safety_flag"]

        if safety_1 == safety_2:
            safety_exact_matches += 1

        labels_1 = case_1["failure_labels"]
        labels_2 = case_2["failure_labels"]

        if set(labels_1) == set(labels_2):
            label_exact_matches += 1

        label_jaccard = _label_jaccard(
            labels_1,
            labels_2,
        )

        label_jaccard_scores.append(
            label_jaccard
        )

        if (
            score_disagreements
            or safety_1 != safety_2
            or set(labels_1) != set(labels_2)
        ):
            disagreement_cases.append(
                {
                    "case_id": case_id,
                    "score_disagreements": (
                        score_disagreements
                    ),
                    "safety_flag": {
                        "evaluator_1": safety_1,
                        "evaluator_2": safety_2,
                        "agreement": (
                            safety_1 == safety_2
                        ),
                    },
                    "failure_labels": {
                        "evaluator_1": sorted(
                            labels_1
                        ),
                        "evaluator_2": sorted(
                            labels_2
                        ),
                        "exact_match": (
                            set(labels_1)
                            == set(labels_2)
                        ),
                        "jaccard_similarity": (
                            label_jaccard
                        ),
                    },
                }
            )

    case_count = len(case_ids)

    dimension_results = {}

    all_absolute_differences = []

    for dimension in sorted(
        REQUIRED_DIMENSIONS
    ):
        differences = (
            dimension_absolute_differences[
                dimension
            ]
        )

        all_absolute_differences.extend(
            differences
        )

        exact_matches = (
            dimension_exact_matches[
                dimension
            ]
        )

        dimension_results[
            dimension
        ] = {
            "exact_match_count": (
                exact_matches
            ),
            "exact_agreement_pct": round(
                (
                    exact_matches
                    / case_count
                )
                * 100,
                2,
            ),
            "mean_absolute_difference": (
                _mean(differences)
            ),
        }

    overall_score_exact_matches = sum(
        dimension_exact_matches.values()
    )

    total_score_comparisons = (
        case_count
        * len(REQUIRED_DIMENSIONS)
    )

    return {
        "case_count": case_count,
        "dimension_agreement": (
            dimension_results
        ),
        "overall_score_exact_agreement_pct": round(
            (
                overall_score_exact_matches
                / total_score_comparisons
            )
            * 100,
            2,
        ),
        "overall_mean_absolute_difference": (
            _mean(
                all_absolute_differences
            )
        ),
        "safety_flag_agreement": {
            "exact_match_count": (
                safety_exact_matches
            ),
            "exact_agreement_pct": round(
                (
                    safety_exact_matches
                    / case_count
                )
                * 100,
                2,
            ),
        },
        "failure_label_agreement": {
            "exact_match_count": (
                label_exact_matches
            ),
            "exact_agreement_pct": round(
                (
                    label_exact_matches
                    / case_count
                )
                * 100,
                2,
            ),
            "mean_jaccard_similarity": (
                _mean(
                    label_jaccard_scores
                )
            ),
        },
        "disagreement_case_count": len(
            disagreement_cases
        ),
        "disagreement_cases": (
            disagreement_cases
        ),
    }