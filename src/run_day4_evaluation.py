import json
from pathlib import Path

from src.evaluator import evaluate_response

SCORED_CASES_FILE = Path("cases/day4_scored_cases.json")
MODEL_OUTPUTS_FILE = Path("results/model_outputs_day4.json")
RESULTS_FILE = Path("results/evaluation_results_day4.json")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    scored_cases = load_json(SCORED_CASES_FILE)
    model_outputs = load_json(MODEL_OUTPUTS_FILE)

    outputs_by_id = {
        item["case_id"]: item
        for item in model_outputs
    }

    results = []

    for case in scored_cases:
        case_id = case["id"]

        if case_id not in outputs_by_id:
            raise ValueError(
                f"Missing model output for case: {case_id}"
            )

        model_output = outputs_by_id[case_id]

        evaluation = evaluate_response(
            scores=case["scores"],
            failure_labels=case.get(
                "failure_labels",
                [],
            ),
        )

        result = {
            "case_id": case_id,
            "task_type": case["task_type"],
            "model_id": model_output["model_id"],
            "timestamp_utc": model_output[
                "timestamp_utc"
            ],
            "generation_settings": model_output[
                "generation_settings"
            ],
            "prompt": model_output["prompt"],
            "model_response": model_output[
                "model_response"
            ],
            "dimension_scores": case["scores"],
            "earned_points": evaluation[
                "earned_points"
            ],
            "max_points": evaluation[
                "max_points"
            ],
            "normalized_score": evaluation[
                "normalized_score"
            ],
            "safety_flag": evaluation[
                "safety_flag"
            ],
            "failure_labels": case.get(
                "failure_labels",
                [],
            ),
            "evaluator_notes": case.get(
                "evaluator_notes",
                "",
            ),
            "evidence_notes": case.get(
                "evidence_notes",
                "",
            ),
            "rubric_version": case.get(
                "rubric_version",
                "v1",
            ),
        }

        results.append(result)

        print(f"Case: {case_id}")
        print(
            f"Score: "
            f"{evaluation['normalized_score']}%"
        )
        print(
            f"Safety flag: "
            f"{evaluation['safety_flag']}"
        )
        print(
            f"Failure labels: "
            f"{case.get('failure_labels', [])}"
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
        f"Saved Day 4 evaluation to: "
        f"{RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()