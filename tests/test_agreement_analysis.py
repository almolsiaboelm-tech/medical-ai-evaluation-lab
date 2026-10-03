from src.agreement_analysis import (
    _label_jaccard,
    analyze_agreement,
)


def _case(
    case_id: str,
    scores: dict[str, int],
    safety_flag: bool,
    failure_labels: list[str],
) -> dict:
    return {
        "case_id": case_id,
        "dimension_scores": scores,
        "safety_flag": safety_flag,
        "failure_labels": failure_labels,
    }


BASE_SCORES = {
    "medical_correctness": 4,
    "clinical_safety": 4,
    "task_completion": 4,
    "relevance": 4,
    "uncertainty_handling": 4,
    "evidence_support": 4,
    "communication_quality": 4,
    "internal_consistency": 4,
}


def test_label_jaccard_exact_match():
    score = _label_jaccard(
        ["a", "b"],
        ["a", "b"],
    )

    assert score == 1.0


def test_label_jaccard_partial_overlap():
    score = _label_jaccard(
        ["a", "b"],
        ["b", "c"],
    )

    assert score == 0.3333


def test_label_jaccard_both_empty():
    score = _label_jaccard(
        [],
        [],
    )

    assert score == 1.0


def test_perfect_agreement():
    evaluator_1 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [],
        )
    ]

    evaluator_2 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [],
        )
    ]

    result = analyze_agreement(
        evaluator_1,
        evaluator_2,
    )

    assert (
        result[
            "overall_score_exact_agreement_pct"
        ]
        == 100.0
    )

    assert (
        result[
            "overall_mean_absolute_difference"
        ]
        == 0.0
    )

    assert (
        result[
            "safety_flag_agreement"
        ]["exact_agreement_pct"]
        == 100.0
    )

    assert (
        result[
            "failure_label_agreement"
        ]["exact_agreement_pct"]
        == 100.0
    )

    assert (
        result["disagreement_case_count"]
        == 0
    )


def test_one_dimension_disagreement():
    scores_1 = BASE_SCORES.copy()
    scores_2 = BASE_SCORES.copy()

    scores_2["clinical_safety"] = 3

    evaluator_1 = [
        _case(
            "case_001",
            scores_1,
            False,
            [],
        )
    ]

    evaluator_2 = [
        _case(
            "case_001",
            scores_2,
            False,
            [],
        )
    ]

    result = analyze_agreement(
        evaluator_1,
        evaluator_2,
    )

    assert (
        result[
            "overall_score_exact_agreement_pct"
        ]
        == 87.5
    )

    assert (
        result[
            "overall_mean_absolute_difference"
        ]
        == 0.125
    )

    assert (
        result[
            "dimension_agreement"
        ]["clinical_safety"][
            "exact_agreement_pct"
        ]
        == 0.0
    )

    assert (
        result[
            "dimension_agreement"
        ]["clinical_safety"][
            "mean_absolute_difference"
        ]
        == 1.0
    )

    assert (
        result["disagreement_case_count"]
        == 1
    )


def test_safety_flag_disagreement():
    evaluator_1 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [],
        )
    ]

    evaluator_2 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            True,
            [],
        )
    ]

    result = analyze_agreement(
        evaluator_1,
        evaluator_2,
    )

    assert (
        result[
            "safety_flag_agreement"
        ]["exact_agreement_pct"]
        == 0.0
    )

    assert (
        result["disagreement_case_count"]
        == 1
    )


def test_failure_label_partial_agreement():
    evaluator_1 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [
                "missed_red_flag",
                "unsafe_recommendation",
            ],
        )
    ]

    evaluator_2 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [
                "missed_red_flag",
            ],
        )
    ]

    result = analyze_agreement(
        evaluator_1,
        evaluator_2,
    )

    assert (
        result[
            "failure_label_agreement"
        ]["exact_agreement_pct"]
        == 0.0
    )

    assert (
        result[
            "failure_label_agreement"
        ]["mean_jaccard_similarity"]
        == 0.5
    )


def test_case_id_mismatch_raises():
    evaluator_1 = [
        _case(
            "case_001",
            BASE_SCORES.copy(),
            False,
            [],
        )
    ]

    evaluator_2 = [
        _case(
            "case_999",
            BASE_SCORES.copy(),
            False,
            [],
        )
    ]

    try:
        analyze_agreement(
            evaluator_1,
            evaluator_2,
        )
    except ValueError as exc:
        assert (
            "Evaluator case IDs do not match"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )