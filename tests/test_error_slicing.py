import json
from pathlib import Path

from src.error_slicing import analyze_slices

RESULTS_FILE = Path(
    "results/evaluation_results_day4.json"
)


def _load_results():
    return json.loads(
        RESULTS_FILE.read_text(
            encoding="utf-8"
        )
    )


def test_day4_results_are_grouped_into_expected_slices():
    analysis = analyze_slices(
        _load_results()
    )

    assert analysis["case_count"] == 10
    assert analysis["slice_count"] == 4
    assert analysis["overall_mean_score"] == 83.44

    assert (
        analysis["slices"]["safety"]["case_ids"]
        == [
            "day4_002",
            "day4_003",
            "day4_006",
            "day4_009",
        ]
    )

    assert (
        analysis["slices"]["patient_education"][
            "case_ids"
        ]
        == [
            "day4_001",
            "day4_005",
            "day4_008",
        ]
    )

    assert (
        analysis["slices"]["uncertainty"]["case_ids"]
        == [
            "day4_004",
            "day4_007",
        ]
    )

    assert (
        analysis["slices"]["scope_control"]["case_ids"]
        == [
            "day4_010",
        ]
    )


def test_patient_education_slice_metrics():
    analysis = analyze_slices(
        _load_results()
    )

    data = analysis["slices"][
        "patient_education"
    ]

    assert data["case_count"] == 3
    assert data["mean_score"] == 73.96
    assert data["delta_vs_overall_score"] == -9.48

    assert data["failure_case_rate_pct"] == 100.0
    assert data["total_failure_occurrences"] == 7
    assert data["failures_per_case"] == 2.33

    assert data["safety_flag_count"] == 0
    assert data["safety_flag_rate_pct"] == 0.0

    assert data["critical_failure_occurrences"] == 0

    assert data["failure_counts"] == {
        "communication_problem": 2,
        "factual_error": 1,
        "incomplete_answer": 3,
        "unsupported_claim": 1,
    }


def test_safety_slice_exposes_risk_despite_high_score():
    analysis = analyze_slices(
        _load_results()
    )

    data = analysis["slices"]["safety"]

    assert data["case_count"] == 4
    assert data["mean_score"] == 89.84
    assert data["delta_vs_overall_score"] == 6.40

    assert data["failure_case_rate_pct"] == 50.0
    assert data["failures_per_case"] == 0.75

    assert data["safety_flag_count"] == 1
    assert data["safety_flag_rate_pct"] == 25.0

    assert data["critical_failure_occurrences"] == 2

    assert data["critical_failure_counts"] == {
        "missed_red_flag": 1,
        "unsafe_recommendation": 1,
    }

    assert data["critical_failure_cases"] == [
        "day4_006"
    ]


def test_uncertainty_slice_metrics_and_warning():
    analysis = analyze_slices(
        _load_results()
    )

    data = analysis["slices"]["uncertainty"]

    assert data["case_count"] == 2
    assert data["mean_score"] == 76.56
    assert data["delta_vs_overall_score"] == -6.88

    assert data["failure_case_rate_pct"] == 100.0
    assert data["failures_per_case"] == 2.0

    assert data["safety_flag_count"] == 1
    assert data["safety_flag_rate_pct"] == 50.0

    assert data["critical_failure_occurrences"] == 1

    assert data["critical_failure_counts"] == {
        "scope_violation": 1
    }

    assert data["dimension_mean_scores"][
        "clinical_safety"
    ] == 2.5

    assert data["dimension_mean_scores"][
        "uncertainty_handling"
    ] == 2.5

    assert data["small_slice_warning"] is True


def test_scope_control_is_marked_as_small_slice():
    analysis = analyze_slices(
        _load_results()
    )

    data = analysis["slices"]["scope_control"]

    assert data["case_count"] == 1
    assert data["mean_score"] == 100.0

    assert data["small_slice_warning"] is True

    assert data["failure_case_rate_pct"] == 0.0
    assert data["safety_flag_rate_pct"] == 0.0
    assert data["critical_failure_occurrences"] == 0