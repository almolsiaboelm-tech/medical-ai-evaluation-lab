import json
from pathlib import Path

from src.evaluator import evaluate_response

CASES_FILE = Path("cases/synthetic_cases_v1.json")
RESULTS_FILE = Path("results/evaluation_results_v1.json")


def main() -> None:
    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    results = []

    for case in cases:
        evaluation = evaluate_response(case["scores"])

        results.append(
            {
                "case_id": case["id"],
                "task_type": case["task_type"],
                "normalized_score": evaluation["normalized_score"],
                "earned_points": evaluation["earned_points"],
                "max_points": evaluation["max_points"],
                "safety_flag": evaluation["safety_flag"],
            }
        )

        print(f'Case: {case["id"]}')
        print(f'Score: {evaluation["normalized_score"]}%')
        print(f'Safety flag: {evaluation["safety_flag"]}')
        print("-" * 40)

    RESULTS_FILE.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(f"Saved results to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()