import json
from pathlib import Path

from src.agreement_analysis import analyze_agreement

EVALUATOR_1_FILE = Path(
    "results/evaluation_results_day4.json"
)

EVALUATOR_2_FILE = Path(
    "cases/day7_second_evaluator_scores.json"
)

OUTPUT_FILE = Path(
    "results/evaluator_agreement_day7.json"
)


def load_json(path: Path) -> list[dict]:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def main() -> None:
    evaluator_1 = load_json(
        EVALUATOR_1_FILE
    )

    evaluator_2 = load_json(
        EVALUATOR_2_FILE
    )

    results = analyze_agreement(
        evaluator_1,
        evaluator_2,
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("Day 7 — Evaluator Agreement")
    print("---------------------------")

    print(
        f"Cases: "
        f"{results['case_count']}"
    )

    print(
        "Overall score exact agreement: "
        f"{results['overall_score_exact_agreement_pct']}%"
    )

    print(
        "Overall mean absolute difference: "
        f"{results['overall_mean_absolute_difference']}"
    )

    print(
        "Safety flag agreement: "
        f"{results['safety_flag_agreement']['exact_agreement_pct']}%"
    )

    print(
        "Failure-label exact agreement: "
        f"{results['failure_label_agreement']['exact_agreement_pct']}%"
    )

    print(
        "Mean failure-label Jaccard similarity: "
        f"{results['failure_label_agreement']['mean_jaccard_similarity']}"
    )

    print(
        "Cases with any disagreement: "
        f"{results['disagreement_case_count']}"
    )

    print()

    print("Per-dimension agreement")
    print("-----------------------")

    for dimension, metrics in (
        results[
            "dimension_agreement"
        ].items()
    ):
        print(
            f"{dimension}: "
            f"exact="
            f"{metrics['exact_agreement_pct']}%, "
            f"MAE="
            f"{metrics['mean_absolute_difference']}"
        )

    print()

    print(
        f"Saved results to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()