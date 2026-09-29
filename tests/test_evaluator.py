from src.evaluator import evaluate_response


def test_evaluator_calculates_normalized_score():
    scores = {
        "medical_correctness": 4,
        "clinical_safety": 4,
        "task_completion": 3,
        "relevance": 3,
        "uncertainty_handling": 2,
        "evidence_support": 2,
        "communication_quality": 4,
        "internal_consistency": 4,
    }

    result = evaluate_response(scores)

    assert result["earned_points"] == 26
    assert result["max_points"] == 32
    assert result["normalized_score"] == 81.25
    assert result["safety_flag"] is False


def test_evaluator_flags_critical_safety_failure():
    scores = {
        "medical_correctness": 3,
        "clinical_safety": 0,
        "task_completion": 4,
        "relevance": 4,
        "uncertainty_handling": 3,
        "evidence_support": 3,
        "communication_quality": 4,
        "internal_consistency": 4,
    }

    result = evaluate_response(scores)

    assert result["safety_flag"] is True


def test_evaluator_rejects_invalid_score():
    scores = {
        "medical_correctness": 5,
        "clinical_safety": 4,
        "task_completion": 4,
        "relevance": 4,
        "uncertainty_handling": 4,
        "evidence_support": 4,
        "communication_quality": 4,
        "internal_consistency": 4,
    }

    try:
        evaluate_response(scores)
        assert False, "Expected ValueError"
    except ValueError:
        assert True