import json
from pathlib import Path

from src.error_slicing import analyze_slices

INPUT_FILE = Path(
    "results/evaluation_results_day4.json"
)

OUTPUT_FILE = Path(
    "results/error_slicing_day6.json"
)


def _print_slice(
    name,
    data,
):
    print("\n" + "=" * 60)
    print(f"Slice: {name}")
    print(f"Cases: {data['case_count']}")
    print(
        "Case IDs: "
        + ", ".join(data["case_ids"])
    )

    print(
        f"Mean score: "
        f"{data['mean_score']}%"
    )

    print(
        f"Delta vs overall: "
        f"{data['delta_vs_overall_score']:+.2f}"
    )

    print(
        f"Failure-case rate: "
        f"{data['failure_case_rate_pct']}%"
    )

    print(
        f"Failures per case: "
        f"{data['failures_per_case']}"
    )

    print(
        f"Safety-flag rate: "
        f"{data['safety_flag_rate_pct']}%"
    )

    print(
        f"Critical failure occurrences: "
        f"{data['critical_failure_occurrences']}"
    )

    print("Failure counts:")

    if data["failure_counts"]:
        for label, count in (
            data["failure_counts"].items()
        ):
            print(f"- {label}: {count}")
    else:
        print("- none")

    print("Critical failures:")

    if data["critical_failure_counts"]:
        for label, count in (
            data[
                "critical_failure_counts"
            ].items()
        ):
            print(f"- {label}: {count}")
    else:
        print("- none")

    print("Dimension means:")

    for dimension, score in (
        data[
            "dimension_mean_scores"
        ].items()
    ):
        print(
            f"- {dimension}: {score}/4"
        )

    if data["small_slice_warning"]:
        print(
            "WARNING: small slice "
            "(fewer than 3 cases); "
            "interpret cautiously."
        )


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    results = json.loads(
        INPUT_FILE.read_text(
            encoding="utf-8"
        )
    )

    analysis = analyze_slices(results)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        json.dumps(
            analysis,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Saved analysis to: {OUTPUT_FILE}"
    )

    print(
        f"Total cases: "
        f"{analysis['case_count']}"
    )

    print(
        f"Overall mean score: "
        f"{analysis['overall_mean_score']}%"
    )

    print(
        f"Slice count: "
        f"{analysis['slice_count']}"
    )

    for name, data in (
        analysis["slices"].items()
    ):
        _print_slice(name, data)


if __name__ == "__main__":
    main()