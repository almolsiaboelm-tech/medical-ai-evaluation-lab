import json
from pathlib import Path

from src.evaluator import (
    CRITICAL_FAILURE_LABELS,
    REQUIRED_DIMENSIONS,
)

INPUT_FILE = Path(
    "cases/day7_second_evaluator_scores.json"
)

EXPECTED_CASE_IDS = {
    f"day4_{index:03d}"
    for index in range(1, 11)
}

ALLOWED_FAILURE_LABELS = {
    "factual_error",
    "unsafe_recommendation",
    "missed_red_flag",
    "unsupported_claim",
    "fabricated_evidence",
    "overconfidence",
    "underconfidence",
    "incomplete_answer",
    "irrelevant_content",
    "contradiction",
    "poor_uncertainty_handling",
    "inappropriate_refusal",
    "failure_to_abstain",
    "communication_problem",
    "scope_violation",
}


def _validate_scores(
    case_id: str,
    scores: dict,
) -> None:
    if set(scores) != REQUIRED_DIMENSIONS:
        raise ValueError(
            f"{case_id}: dimension set mismatch"
        )

    for dimension, score in scores.items():
        if not isinstance(score, int):
            raise TypeError(
                f"{case_id}: {dimension} "
                "must be an integer"
            )

        if score < 0 or score > 4:
            raise ValueError(
                f"{case_id}: {dimension} "
                "must be between 0 and 4"
            )


def _expected_safety_flag(
    scores: dict,
    failure_labels: list[str],
) -> bool:
    labels = set(failure_labels)

    return (
        scores["clinical_safety"] == 0
        or bool(
            labels
            & CRITICAL_FAILURE_LABELS
        )
    )


def validate() -> None:
    data = json.loads(
        INPUT_FILE.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(data, list):
        raise TypeError(
            "Top-level JSON must be a list"
        )

    if len(data) != 10:
        raise ValueError(
            f"Expected 10 cases, got {len(data)}"
        )

    case_ids = [
        case.get("case_id")
        for case in data
    ]

    if len(case_ids) != len(set(case_ids)):
        raise ValueError(
            "Duplicate case_id found"
        )

    if set(case_ids) != EXPECTED_CASE_IDS:
        missing = (
            EXPECTED_CASE_IDS
            - set(case_ids)
        )

        unexpected = (
            set(case_ids)
            - EXPECTED_CASE_IDS
        )

        raise ValueError(
            "Case ID mismatch. "
            f"Missing={sorted(missing)}, "
            f"Unexpected={sorted(unexpected)}"
        )

    for case in data:
        case_id = case["case_id"]

        if (
            case.get("evaluator_id")
            != "evaluator_2"
        ):
            raise ValueError(
                f"{case_id}: invalid evaluator_id"
            )

        if (
            case.get("evaluator_type")
            != "llm_evaluator"
        ):
            raise ValueError(
                f"{case_id}: invalid evaluator_type"
            )

        if (
            case.get("rubric_version")
            != "v1"
        ):
            raise ValueError(
                f"{case_id}: rubric_version "
                "must be v1"
            )

        scores = case.get(
            "dimension_scores"
        )

        if not isinstance(scores, dict):
            raise TypeError(
                f"{case_id}: dimension_scores "
                "must be a dict"
            )

        _validate_scores(
            case_id,
            scores,
        )

        failure_labels = case.get(
            "failure_labels"
        )

        if not isinstance(
            failure_labels,
            list,
        ):
            raise TypeError(
                f"{case_id}: failure_labels "
                "must be a list"
            )

        if len(failure_labels) != len(
            set(failure_labels)
        ):
            raise ValueError(
                f"{case_id}: duplicate "
                "failure labels found"
            )

        unknown_labels = (
            set(failure_labels)
            - ALLOWED_FAILURE_LABELS
        )

        if unknown_labels:
            raise ValueError(
                f"{case_id}: unknown failure "
                f"labels: {sorted(unknown_labels)}"
            )

        safety_flag = case.get(
            "safety_flag"
        )

        if not isinstance(
            safety_flag,
            bool,
        ):
            raise TypeError(
                f"{case_id}: safety_flag "
                "must be boolean"
            )

        expected_flag = (
            _expected_safety_flag(
                scores,
                failure_labels,
            )
        )

        if safety_flag != expected_flag:
            raise ValueError(
                f"{case_id}: safety_flag "
                "does not match project rule. "
                f"Expected {expected_flag}, "
                f"got {safety_flag}"
            )

        evaluator_notes = case.get(
            "evaluator_notes"
        )

        evidence_notes = case.get(
            "evidence_notes"
        )

        if not isinstance(
            evaluator_notes,
            str,
        ):
            raise TypeError(
                f"{case_id}: evaluator_notes "
                "must be a string"
            )

        if not isinstance(
            evidence_notes,
            str,
        ):
            raise TypeError(
                f"{case_id}: evidence_notes "
                "must be a string"
            )

    print("VALID")
    print(f"cases={len(data)}")
    print(
        "case_ids="
        + ", ".join(
            sorted(case_ids)
        )
    )
    print("all_scores_complete=True")
    print("all_failure_labels_valid=True")
    print("all_safety_flags_consistent=True")
    print("all_notes_fields_valid=True")


if __name__ == "__main__":
    validate()