import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DAY7_AGREEMENT_PATH = (
    PROJECT_ROOT
    / "results"
    / "evaluator_agreement_day7.json"
)

EVALUATOR_1_PATH = (
    PROJECT_ROOT
    / "results"
    / "evaluation_results_day4.json"
)

EVALUATOR_2_PATH = (
    PROJECT_ROOT
    / "cases"
    / "day7_second_evaluator_scores.json"
)

TRIAGE_PATH = (
    PROJECT_ROOT
    / "results"
    / "adjudication_triage_day8.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "cases"
    / "day8_adjudication_cases.json"
)


def load_json(path: Path) -> Any:
    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def normalize_evaluator_1(
    case: dict[str, Any],
) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "evaluator_id": "evaluator_1",
        "evaluator_type": "human_evaluator",
        "rubric_version": case["rubric_version"],
        "dimension_scores": case["dimension_scores"],
        "failure_labels": case["failure_labels"],
        "safety_flag": case["safety_flag"],
        "evaluator_notes": case["evaluator_notes"],
        "evidence_notes": case["evidence_notes"],
    }


def normalize_evaluator_2(
    case: dict[str, Any],
) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "evaluator_id": case["evaluator_id"],
        "evaluator_type": case["evaluator_type"],
        "rubric_version": case["rubric_version"],
        "dimension_scores": case["dimension_scores"],
        "failure_labels": case["failure_labels"],
        "safety_flag": case["safety_flag"],
        "evaluator_notes": case["evaluator_notes"],
        "evidence_notes": case["evidence_notes"],
    }


def main() -> None:
    agreement_results = load_json(
        DAY7_AGREEMENT_PATH
    )

    evaluator_1_raw = load_json(
        EVALUATOR_1_PATH
    )

    evaluator_2_raw = load_json(
        EVALUATOR_2_PATH
    )

    triage_results = load_json(
        TRIAGE_PATH
    )

    disagreement_ids = {
        case["case_id"]
        for case in agreement_results[
            "disagreement_cases"
        ]
    }

    evaluator_1_by_id = {
        case["case_id"]: normalize_evaluator_1(case)
        for case in evaluator_1_raw
    }

    evaluator_2_by_id = {
        case["case_id"]: normalize_evaluator_2(case)
        for case in evaluator_2_raw
    }

    triage_by_id = {
        case["case_id"]: case
        for case in triage_results["cases"]
    }

    missing_evaluator_1 = (
        disagreement_ids
        - set(evaluator_1_by_id)
    )

    missing_evaluator_2 = (
        disagreement_ids
        - set(evaluator_2_by_id)
    )

    missing_triage = (
        disagreement_ids
        - set(triage_by_id)
    )

    if missing_evaluator_1:
        raise ValueError(
            "Missing Evaluator 1 cases: "
            f"{sorted(missing_evaluator_1)}"
        )

    if missing_evaluator_2:
        raise ValueError(
            "Missing Evaluator 2 cases: "
            f"{sorted(missing_evaluator_2)}"
        )

    if missing_triage:
        raise ValueError(
            "Missing triage cases: "
            f"{sorted(missing_triage)}"
        )

    adjudication_cases = []

    for case_id in sorted(disagreement_ids):
        adjudication_cases.append(
            {
                "case_id": case_id,
                "triage": triage_by_id[case_id],
                "evaluator_1": (
                    evaluator_1_by_id[case_id]
                ),
                "evaluator_2": (
                    evaluator_2_by_id[case_id]
                ),
            }
        )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            adjudication_cases,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        "Day 8 adjudication cases built."
    )
    print(
        "Cases:",
        len(adjudication_cases),
    )
    print(
        "Saved to:",
        OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()