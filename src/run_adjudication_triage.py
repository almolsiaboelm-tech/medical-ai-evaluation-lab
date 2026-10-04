import json
from pathlib import Path

from src.adjudication_triage import (
    triage_disagreement_cases,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "evaluator_agreement_day7.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "adjudication_triage_day8.json"
)


def main() -> None:
    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        agreement_results = json.load(file)

    disagreement_cases = agreement_results[
        "disagreement_cases"
    ]

    triage_results = triage_disagreement_cases(
        disagreement_cases
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            triage_results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        "Day 8 adjudication triage complete."
    )
    print(
        "Disagreement cases:",
        triage_results[
            "disagreement_case_count"
        ],
    )
    print(
        "Adjudication required:",
        triage_results[
            "adjudication_required_count"
        ],
    )
    print(
        "Priority counts:",
        triage_results[
            "priority_counts"
        ],
    )
    print(
        "Reason counts:",
        triage_results[
            "reason_counts"
        ],
    )
    print(
        "Saved to:",
        OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()