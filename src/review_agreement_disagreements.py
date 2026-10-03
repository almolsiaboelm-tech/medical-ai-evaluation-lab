import json
from pathlib import Path

INPUT_FILE = Path(
    "results/evaluator_agreement_day7.json"
)


def main() -> None:
    data = json.loads(
        INPUT_FILE.read_text(
            encoding="utf-8"
        )
    )

    disagreements = data[
        "disagreement_cases"
    ]

    print(
        "Day 7 — Disagreement Review"
    )
    print(
        "==========================="
    )

    for case in disagreements:
        print()
        print(case["case_id"])
        print("-" * len(case["case_id"]))

        score_disagreements = case[
            "score_disagreements"
        ]

        if score_disagreements:
            print(
                "Score disagreements:"
            )

            for dimension, values in (
                score_disagreements.items()
            ):
                print(
                    f"  {dimension}: "
                    f"E1={values['evaluator_1']} "
                    f"E2={values['evaluator_2']} "
                    f"diff={values['absolute_difference']}"
                )

        safety = case["safety_flag"]

        if not safety["agreement"]:
            print(
                "SAFETY FLAG DISAGREEMENT:"
            )
            print(
                f"  E1={safety['evaluator_1']} "
                f"E2={safety['evaluator_2']}"
            )

        labels = case[
            "failure_labels"
        ]

        if not labels["exact_match"]:
            print(
                "Failure-label disagreement:"
            )
            print(
                "  E1="
                + ", ".join(
                    labels["evaluator_1"]
                )
            )
            print(
                "  E2="
                + ", ".join(
                    labels["evaluator_2"]
                )
            )
            print(
                "  Jaccard="
                f"{labels['jaccard_similarity']}"
            )


if __name__ == "__main__":
    main()