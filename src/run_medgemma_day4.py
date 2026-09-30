import json
from datetime import datetime, timezone
from pathlib import Path

from medgemma_client import generate_medgemma_response

CASES_FILE = Path("cases/day4_cases.json")
OUTPUT_FILE = Path("results/model_outputs_day4.json")

MODEL_ID = "google/medgemma-1.5-4b-it"
MAX_NEW_TOKENS = 300


def main() -> None:
    cases = json.loads(
        CASES_FILE.read_text(encoding="utf-8")
    )

    outputs = []

    for case in cases:
        print(f'Running: {case["id"]}')

        response = generate_medgemma_response(
            case["prompt"],
            max_new_tokens=MAX_NEW_TOKENS,
        )

        outputs.append(
            {
                "case_id": case["id"],
                "task_type": case["task_type"],
                "prompt": case["prompt"],
                "model_id": MODEL_ID,
                "timestamp_utc": datetime.now(
                    timezone.utc
                ).isoformat(),
                "generation_settings": {
                    "max_new_tokens": MAX_NEW_TOKENS,
                    "do_sample": False
                },
                "model_response": response
            }
        )

        print("Done")
        print("-" * 40)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        json.dumps(
            outputs,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Saved outputs to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()