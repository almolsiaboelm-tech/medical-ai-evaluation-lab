from src.adjudication_triage import (
    triage_disagreement_case,
    triage_disagreement_cases,
)


def _base_case() -> dict:
    return {
        "case_id": "case_001",
        "score_disagreements": {},
        "safety_flag": {
            "evaluator_1": False,
            "evaluator_2": False,
            "agreement": True,
        },
        "failure_labels": {
            "evaluator_1": [],
            "evaluator_2": [],
            "exact_match": True,
            "jaccard_similarity": 1.0,
        },
    }


def test_safety_flag_disagreement_is_critical():
    case = _base_case()

    case["safety_flag"] = {
        "evaluator_1": False,
        "evaluator_2": True,
        "agreement": False,
    }

    result = triage_disagreement_case(case)

    assert result["requires_adjudication"] is True
    assert result["priority"] == "critical"
    assert (
        "safety_flag_disagreement"
        in result["adjudication_reasons"]
    )


def test_clinical_safety_score_disagreement_is_high():
    case = _base_case()

    case["score_disagreements"] = {
        "clinical_safety": {
            "evaluator_1": 3,
            "evaluator_2": 2,
            "absolute_difference": 1,
        }
    }

    result = triage_disagreement_case(case)

    assert result["requires_adjudication"] is True
    assert result["priority"] == "high"
    assert (
        "safety_score_disagreement"
        in result["adjudication_reasons"]
    )


def test_major_score_disagreement_is_high():
    case = _base_case()

    case["score_disagreements"] = {
        "relevance": {
            "evaluator_1": 4,
            "evaluator_2": 2,
            "absolute_difference": 2,
        }
    }

    result = triage_disagreement_case(case)

    assert result["requires_adjudication"] is True
    assert result["priority"] == "high"
    assert (
        "major_score_disagreement"
        in result["adjudication_reasons"]
    )


def test_failure_label_disagreement_is_medium():
    case = _base_case()

    case["failure_labels"] = {
        "evaluator_1": [
            "incomplete_answer",
        ],
        "evaluator_2": [
            "incomplete_answer",
            "communication_problem",
        ],
        "exact_match": False,
        "jaccard_similarity": 0.5,
    }

    result = triage_disagreement_case(case)

    assert result["requires_adjudication"] is True
    assert result["priority"] == "medium"
    assert (
        "failure_label_disagreement"
        in result["adjudication_reasons"]
    )


def test_minor_score_disagreement_is_low():
    case = _base_case()

    case["score_disagreements"] = {
        "relevance": {
            "evaluator_1": 4,
            "evaluator_2": 3,
            "absolute_difference": 1,
        }
    }

    result = triage_disagreement_case(case)

    assert result["requires_adjudication"] is True
    assert result["priority"] == "low"
    assert (
        "minor_score_disagreement"
        in result["adjudication_reasons"]
    )


def test_multiple_reasons_keep_highest_priority():
    case = _base_case()

    case["score_disagreements"] = {
        "clinical_safety": {
            "evaluator_1": 3,
            "evaluator_2": 2,
            "absolute_difference": 1,
        }
    }

    case["failure_labels"] = {
        "evaluator_1": [],
        "evaluator_2": [
            "incomplete_answer",
        ],
        "exact_match": False,
        "jaccard_similarity": 0.0,
    }

    result = triage_disagreement_case(case)

    assert result["priority"] == "high"
    assert (
        "safety_score_disagreement"
        in result["adjudication_reasons"]
    )
    assert (
        "failure_label_disagreement"
        in result["adjudication_reasons"]
    )


def test_summary_counts_cases_priorities_and_reasons():
    case_1 = _base_case()
    case_1["case_id"] = "case_001"
    case_1["score_disagreements"] = {
        "relevance": {
            "evaluator_1": 4,
            "evaluator_2": 3,
            "absolute_difference": 1,
        }
    }

    case_2 = _base_case()
    case_2["case_id"] = "case_002"
    case_2["score_disagreements"] = {
        "clinical_safety": {
            "evaluator_1": 3,
            "evaluator_2": 2,
            "absolute_difference": 1,
        }
    }

    result = triage_disagreement_cases(
        [case_1, case_2]
    )

    assert result["disagreement_case_count"] == 2
    assert result["adjudication_required_count"] == 2
    assert result["priority_counts"]["low"] == 1
    assert result["priority_counts"]["high"] == 1
    assert (
        result["reason_counts"][
            "minor_score_disagreement"
        ]
        == 1
    )
    assert (
        result["reason_counts"][
            "safety_score_disagreement"
        ]
        == 1
    )