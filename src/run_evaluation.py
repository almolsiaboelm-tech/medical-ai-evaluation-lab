import json
from pathlib import Path

from src.evaluator import evaluate_response


CASES_FILE = Path("cases/synthetic_cases_v1.json")
RESULTS_FILE = Path("results/evaluation_results_v1.json")


def main() -> None:
    cases = json.loads(
        CASES_FILE.read_text(encoding="utf-8")
    )

    results = []

    for case in cases:
        evaluation = evaluate_response(
            scores=case["scores"],
            failure_labels=case.get("failure_labels", []),
        )

        result = {
            "case_id": case["id"],
            "task_type": case["task_type"],
            "dimension_scores": case["scores"],
            "normalized_score": evaluation["normalized_score"],
            "earned_points": evaluation["earned_points"],
            "max_points": evaluation["max_points"],
            "safety_flag": evaluation["safety_flag"],
            "failure_labels": case.get("failure_labels", []),
            "evaluator_notes": case.get("evaluator_notes", ""),
            "evidence_notes": case.get("evidence_notes", ""),
            "rubric_version": case.get("rubric_version", "v1"),
        }

        results.append(result)

        print(f'Case: {case["id"]}')
        print(
            f'Score: '
            f'{evaluation["normalized_score"]}%'
        )
        print(
            f'Safety flag: '
            f'{evaluation["safety_flag"]}'
        )
        print(
            f'Failure labels: '
            f'{case.get("failure_labels", [])}'
        )
        print("-" * 40)

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_FILE.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Saved results to: {RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()