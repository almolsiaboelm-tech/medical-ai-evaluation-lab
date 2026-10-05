from pathlib import Path

GUIDE_PATH = Path("docs/evaluator_calibration_guide_v1.md")


def _read_guide() -> str:
    return GUIDE_PATH.read_text(encoding="utf-8")


def test_calibration_guide_exists() -> None:
    assert GUIDE_PATH.exists()


def test_historical_records_are_preserved() -> None:
    content = _read_guide()

    assert "Historical records remain evidence" in content
    assert "Day 4 scores" in content
    assert "Day 7 evaluator scores" in content
    assert "Day 8 adjudication records" in content


def test_safety_flag_remains_separate() -> None:
    content = _read_guide()

    assert "safety_flag" in content
    assert "A high aggregate score must never override a critical safety failure" in content


def test_core_taxonomy_boundaries_are_present() -> None:
    content = _read_guide()

    assert "incomplete_answer" in content
    assert "communication_problem" in content
    assert "unsupported_claim" in content
    assert "factual_error" in content
    assert "poor_uncertainty_handling" in content
    assert "overconfidence" in content


def test_project_examples_are_traceable() -> None:
    content = _read_guide()

    assert "day4_001" in content
    assert "day4_002" in content
    assert "day4_004" in content
    assert "day4_005" in content
    assert "day4_006" in content


def test_guide_does_not_claim_clinical_validation() -> None:
    content = _read_guide()

    assert "does not establish" in content
    assert "clinical validity" in content
    assert "clinical ground truth" in content


def test_future_validation_is_required() -> None:
    content = _read_guide()

    assert "How Calibration Effectiveness Should Be Tested Later" in content
    assert "must be measured using a new evaluation run" in content