import json
from pathlib import Path

from src.failure_analysis import analyze_results

INPUT_FILE = Path("results/evaluation_results_day4.json")
OUTPUT_FILE = Path("results/failure_analysis_day5.json")


def main() -> None:
    results = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    analysis = analyze_results(results)

    OUTPUT_FILE.write_text(
        json.dumps(
            analysis,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Saved analysis to: {OUTPUT_FILE}")
    print(f"Cases: {analysis['case_count']}")
    print(f"Mean score: {analysis['mean_score']}%")
    print(
        f"Safety flags: "
        f"{analysis['safety_flag_count']}"
    )
    print(
        f"Failure occurrences: "
        f"{analysis['total_failure_occurrences']}"
    )

    print("\nFailure counts:")
    for label, count in analysis["failure_counts"].items():
        print(f"- {label}: {count}")

    print("\nCritical failure counts:")
    for label, count in analysis[
        "critical_failure_counts"
    ].items():
        print(f"- {label}: {count}")

    print("\nDimension mean scores:")
    for dimension, score in analysis[
        "dimension_mean_scores"
    ].items():
        print(f"- {dimension}: {score}/4")


if __name__ == "__main__":
    main()