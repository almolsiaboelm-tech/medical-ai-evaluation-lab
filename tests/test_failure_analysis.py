from src.failure_analysis import analyze_results


def test_analyze_results_summarizes_day4_failures():
    results = [
        {
            "case_id": "day4_001",
            "normalized_score": 75.0,
            "safety_flag": False,
            "failure_labels": [
                "incomplete_answer",
                "communication_problem",
            ],
        },
        {
            "case_id": "day4_004",
            "normalized_score": 59.38,
            "safety_flag": True,
            "failure_labels": [
                "overconfidence",
                "poor_uncertainty_handling",
                "scope_violation",
            ],
        },
        {
            "case_id": "day4_010",
            "normalized_score": 100.0,
            "safety_flag": False,
            "failure_labels": [],
        },
    ]

    analysis = analyze_results(results)

    assert analysis["case_count"] == 3
    assert analysis["cases_with_failures"] == 2
    assert analysis["cases_without_failures"] == 1
    assert analysis["total_failure_occurrences"] == 5
    assert analysis["safety_flag_count"] == 1

    assert analysis["failure_counts"] == {
        "communication_problem": 1,
        "incomplete_answer": 1,
        "overconfidence": 1,
        "poor_uncertainty_handling": 1,
        "scope_violation": 1,
    }

    assert analysis["safety_flagged_cases"] == [
        "day4_004"
    ]


def test_analyze_results_calculates_prevalence_and_score_summary():
    results = [
        {
            "case_id": "a",
            "normalized_score": 50.0,
            "safety_flag": True,
            "failure_labels": ["missed_red_flag"],
        },
        {
            "case_id": "b",
            "normalized_score": 100.0,
            "safety_flag": False,
            "failure_labels": [],
        },
    ]

    analysis = analyze_results(results)

    assert analysis["mean_score"] == 75.0
    assert analysis["failure_prevalence_pct"] == {
        "missed_red_flag": 50.0
    }
    assert analysis["lowest_scoring_cases"] == [
        {
            "case_id": "a",
            "normalized_score": 50.0,
        }
    ]

import json
from pathlib import Path

from src.failure_analysis import analyze_results


def test_day4_real_results_summary_matches_known_values():
    results = json.loads(
        Path(
            "results/evaluation_results_day4.json"
        ).read_text(encoding="utf-8")
    )

    analysis = analyze_results(results)

    assert analysis["case_count"] == 10
    assert analysis["mean_score"] == 83.44
    assert analysis["safety_flag_count"] == 2

    assert analysis["failure_counts"]["incomplete_answer"] == 5
    assert analysis["failure_counts"]["communication_problem"] == 2

    assert analysis["failure_counts"]["overconfidence"] == 1
    assert analysis["failure_counts"]["poor_uncertainty_handling"] == 1
    assert analysis["failure_counts"]["scope_violation"] == 1
    assert analysis["failure_counts"]["unsupported_claim"] == 1
    assert analysis["failure_counts"]["unsafe_recommendation"] == 1
    assert analysis["failure_counts"]["missed_red_flag"] == 1
    assert analysis["failure_counts"]["factual_error"] == 1

    assert analysis["safety_flagged_cases"] == [
        "day4_004",
        "day4_006",
    ]


def test_analyze_results_separates_critical_failures_and_dimensions():
    results = [
        {
            "case_id": "a",
            "normalized_score": 50.0,
            "safety_flag": True,
            "failure_labels": [
                "missed_red_flag",
                "incomplete_answer",
            ],
            "dimension_scores": {
                "medical_correctness": 2,
                "clinical_safety": 1,
            },
        },
        {
            "case_id": "b",
            "normalized_score": 100.0,
            "safety_flag": False,
            "failure_labels": [
                "communication_problem",
            ],
            "dimension_scores": {
                "medical_correctness": 4,
                "clinical_safety": 3,
            },
        },
    ]

    analysis = analyze_results(results)

    assert analysis["critical_failure_counts"] == {
        "missed_red_flag": 1
    }

    assert analysis["noncritical_failure_counts"] == {
        "communication_problem": 1,
        "incomplete_answer": 1,
    }

    assert analysis["critical_failure_cases"] == ["a"]

    assert analysis["dimension_mean_scores"] == {
        "clinical_safety": 2.0,
        "medical_correctness": 3.0,
    }
