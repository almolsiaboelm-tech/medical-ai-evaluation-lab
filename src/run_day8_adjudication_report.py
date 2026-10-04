import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.evaluator import REQUIRED_DIMENSIONS


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CASES_PATH = (
    PROJECT_ROOT
    / "cases"
    / "day8_adjudication_cases.json"
)

ADJUDICATED_PATH = (
    PROJECT_ROOT
    / "cases"
    / "day8_adjudicated_scores.json"
)

TRIAGE_PATH = (
    PROJECT_ROOT
    / "results"
    / "adjudication_triage_day8.json"
)

SUMMARY_OUTPUT_PATH = (
    PROJECT_ROOT
    / "results"
    / "adjudication_summary_day8.json"
)

REPORT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "day8_adjudication_report.md"
)


def load_json(path: Path) -> Any:
    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def mean(values: list[float]) -> float:
    if not values:
        return 0.0

    return round(
        sum(values) / len(values),
        4,
    )


def main() -> None:
    adjudication_inputs = load_json(
        INPUT_CASES_PATH
    )

    adjudicated = load_json(
        ADJUDICATED_PATH
    )

    triage = load_json(
        TRIAGE_PATH
    )

    inputs_by_id = {
        case["case_id"]: case
        for case in adjudication_inputs
    }

    adjudicated_by_id = {
        case["case_id"]: case
        for case in adjudicated
    }

    dimension_resolution = {
        dimension: {
            "matched_evaluator_1": 0,
            "matched_evaluator_2": 0,
            "matched_both": 0,
            "matched_neither": 0,
        }
        for dimension in REQUIRED_DIMENSIONS
    }

    evaluator_1_dimension_values = {
        dimension: []
        for dimension in REQUIRED_DIMENSIONS
    }

    evaluator_2_dimension_values = {
        dimension: []
        for dimension in REQUIRED_DIMENSIONS
    }

    final_dimension_values = {
        dimension: []
        for dimension in REQUIRED_DIMENSIONS
    }

    cases_changed_from_evaluator_1 = 0
    cases_changed_from_evaluator_2 = 0

    final_labels_match_evaluator_1 = 0
    final_labels_match_evaluator_2 = 0
    final_labels_match_both = 0
    final_labels_match_neither = 0

    safety_match_both = 0
    safety_match_evaluator_1_only = 0
    safety_match_evaluator_2_only = 0
    safety_match_neither = 0

    final_safety_flag_count = 0

    adjudication_details = []

    for case_id in sorted(adjudicated_by_id):
        source = inputs_by_id[case_id]
        final = adjudicated_by_id[case_id]

        evaluator_1 = source["evaluator_1"]
        evaluator_2 = source["evaluator_2"]

        final_scores = final[
            "final_dimension_scores"
        ]

        e1_scores = evaluator_1[
            "dimension_scores"
        ]

        e2_scores = evaluator_2[
            "dimension_scores"
        ]

        changed_from_e1 = False
        changed_from_e2 = False

        resolved_dimensions = []

        for dimension in REQUIRED_DIMENSIONS:
            score_1 = e1_scores[dimension]
            score_2 = e2_scores[dimension]
            final_score = final_scores[dimension]

            evaluator_1_dimension_values[
                dimension
            ].append(score_1)

            evaluator_2_dimension_values[
                dimension
            ].append(score_2)

            final_dimension_values[
                dimension
            ].append(final_score)

            if final_score != score_1:
                changed_from_e1 = True

            if final_score != score_2:
                changed_from_e2 = True

            if score_1 == score_2 == final_score:
                dimension_resolution[
                    dimension
                ]["matched_both"] += 1

            elif (
                final_score == score_1
                and final_score != score_2
            ):
                dimension_resolution[
                    dimension
                ]["matched_evaluator_1"] += 1

            elif (
                final_score == score_2
                and final_score != score_1
            ):
                dimension_resolution[
                    dimension
                ]["matched_evaluator_2"] += 1

            else:
                dimension_resolution[
                    dimension
                ]["matched_neither"] += 1

            if score_1 != score_2:
                resolved_dimensions.append(
                    {
                        "dimension": dimension,
                        "evaluator_1": score_1,
                        "evaluator_2": score_2,
                        "final": final_score,
                    }
                )

        if changed_from_e1:
            cases_changed_from_evaluator_1 += 1

        if changed_from_e2:
            cases_changed_from_evaluator_2 += 1

        labels_1 = set(
            evaluator_1["failure_labels"]
        )

        labels_2 = set(
            evaluator_2["failure_labels"]
        )

        final_labels = set(
            final["final_failure_labels"]
        )

        if (
            final_labels == labels_1
            and final_labels == labels_2
        ):
            final_labels_match_both += 1

        elif final_labels == labels_1:
            final_labels_match_evaluator_1 += 1

        elif final_labels == labels_2:
            final_labels_match_evaluator_2 += 1

        else:
            final_labels_match_neither += 1

        safety_1 = evaluator_1[
            "safety_flag"
        ]

        safety_2 = evaluator_2[
            "safety_flag"
        ]

        final_safety = final[
            "final_safety_flag"
        ]

        if final_safety:
            final_safety_flag_count += 1

        if (
            final_safety == safety_1
            and final_safety == safety_2
        ):
            safety_match_both += 1

        elif final_safety == safety_1:
            safety_match_evaluator_1_only += 1

        elif final_safety == safety_2:
            safety_match_evaluator_2_only += 1

        else:
            safety_match_neither += 1

        adjudication_details.append(
            {
                "case_id": case_id,
                "priority": final[
                    "adjudication_priority"
                ],
                "reasons": final[
                    "adjudication_reasons"
                ],
                "resolved_dimensions": (
                    resolved_dimensions
                ),
                "final_failure_labels": sorted(
                    final_labels
                ),
                "final_safety_flag": (
                    final_safety
                ),
            }
        )

    evaluator_1_means = {
        dimension: mean(
            evaluator_1_dimension_values[
                dimension
            ]
        )
        for dimension in REQUIRED_DIMENSIONS
    }

    evaluator_2_means = {
        dimension: mean(
            evaluator_2_dimension_values[
                dimension
            ]
        )
        for dimension in REQUIRED_DIMENSIONS
    }

    final_dimension_means = {
        dimension: mean(
            final_dimension_values[
                dimension
            ]
        )
        for dimension in REQUIRED_DIMENSIONS
    }

    priority_counts = Counter(
        case["adjudication_priority"]
        for case in adjudicated
    )

    final_failure_counts = Counter()

    for case in adjudicated:
        final_failure_counts.update(
            case["final_failure_labels"]
        )

    summary = {
        "adjudicated_case_count": len(
            adjudicated
        ),
        "open_disagreement_cases_before": len(
            adjudicated
        ),
        "open_disagreement_cases_after": 0,
        "priority_counts": {
            priority: priority_counts.get(
                priority,
                0,
            )
            for priority in (
                "critical",
                "high",
                "medium",
                "low",
            )
        },
        "triage_reason_counts": triage[
            "reason_counts"
        ],
        "cases_changed_from_evaluator_1": (
            cases_changed_from_evaluator_1
        ),
        "cases_changed_from_evaluator_2": (
            cases_changed_from_evaluator_2
        ),
        "dimension_resolution": (
            dimension_resolution
        ),
        "dimension_means": {
            "evaluator_1": evaluator_1_means,
            "evaluator_2": evaluator_2_means,
            "adjudicated": final_dimension_means,
        },
        "failure_label_resolution": {
            "matched_both": (
                final_labels_match_both
            ),
            "matched_evaluator_1_only": (
                final_labels_match_evaluator_1
            ),
            "matched_evaluator_2_only": (
                final_labels_match_evaluator_2
            ),
            "matched_neither": (
                final_labels_match_neither
            ),
        },
        "final_failure_label_counts": dict(
            sorted(
                final_failure_counts.items()
            )
        ),
        "safety_resolution": {
            "final_safety_flagged_cases": (
                final_safety_flag_count
            ),
            "matched_both": (
                safety_match_both
            ),
            "matched_evaluator_1_only": (
                safety_match_evaluator_1_only
            ),
            "matched_evaluator_2_only": (
                safety_match_evaluator_2_only
            ),
            "matched_neither": (
                safety_match_neither
            ),
        },
        "cases": adjudication_details,
    }

    with SUMMARY_OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    report_lines = [
        "# Day 8 — Adjudication Report",
        "",
        "## Purpose",
        "",
        (
            "Day 8 converts the evaluator "
            "disagreements identified on Day 7 "
            "into a documented adjudication workflow."
        ),
        "",
        (
            "The resulting judgments are an "
            "**adjudicated reference evaluation**, "
            "not a clinical gold standard."
        ),
        "",
        "## Adjudication Volume",
        "",
        (
            "Disagreement cases reviewed: "
            f"{summary['adjudicated_case_count']}"
        ),
        "",
        (
            "Open disagreement cases before "
            "adjudication: "
            f"{summary['open_disagreement_cases_before']}"
        ),
        "",
        (
            "Open disagreement cases after "
            "adjudication: "
            f"{summary['open_disagreement_cases_after']}"
        ),
        "",
        (
            "This does not represent improved inter-rater "
            "agreement. The disagreements were resolved "
            "through an explicit adjudication step."
        ),
        "",
        "## Triage Priority",
        "",
    ]

    for priority in (
        "critical",
        "high",
        "medium",
        "low",
    ):
        report_lines.append(
            f"- {priority}: "
            f"{summary['priority_counts'][priority]}"
        )

    report_lines.extend(
        [
            "",
            "## Triage Reasons",
            "",
        ]
    )

    for reason, count in sorted(
        summary[
            "triage_reason_counts"
        ].items()
    ):
        report_lines.append(
            f"- {reason}: {count}"
        )

    report_lines.extend(
        [
            "",
            "## Adjudicated Dimension Means",
            "",
            (
                "| Dimension | Evaluator 1 | "
                "Evaluator 2 | Adjudicated |"
            ),
            "|---|---:|---:|---:|",
        ]
    )

    for dimension in REQUIRED_DIMENSIONS:
        report_lines.append(
            "| "
            f"{dimension} | "
            f"{evaluator_1_means[dimension]:.2f} | "
            f"{evaluator_2_means[dimension]:.2f} | "
            f"{final_dimension_means[dimension]:.2f} |"
        )

    report_lines.extend(
        [
            "",
            "## Failure-Label Resolution",
            "",
            (
                "- Final label set matched both "
                "evaluators: "
                f"{final_labels_match_both}"
            ),
            (
                "- Matched Evaluator 1 only: "
                f"{final_labels_match_evaluator_1}"
            ),
            (
                "- Matched Evaluator 2 only: "
                f"{final_labels_match_evaluator_2}"
            ),
            (
                "- Matched neither exactly: "
                f"{final_labels_match_neither}"
            ),
            "",
            "## Final Failure Labels",
            "",
        ]
    )

    for label, count in sorted(
        final_failure_counts.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    ):
        report_lines.append(
            f"- {label}: {count}"
        )

    report_lines.extend(
        [
            "",
            "## Safety Resolution",
            "",
            (
                "- Final safety-flagged cases: "
                f"{final_safety_flag_count}"
            ),
            (
                "- Final safety flag matched both "
                f"evaluators: {safety_match_both}"
            ),
            "",
            (
                "No Day 7 case contained a disagreement "
                "on the binary safety flag. Day 8 "
                "therefore focused primarily on severity "
                "calibration and failure-label boundaries."
            ),
            "",
            "## Methodological Interpretation",
            "",
            (
                "Adjudication should not be interpreted "
                "as evidence that the rubric became more "
                "reliable after review."
            ),
            "",
            (
                "Instead, Day 8 demonstrates a process "
                "for making disagreements explicit, "
                "prioritizing safety-related differences, "
                "reviewing the original evidence, and "
                "preserving a traceable final judgment."
            ),
            "",
            (
                "The historical Evaluator 1 and Evaluator 2 "
                "records remain unchanged."
            ),
            "",
            "## Limitations",
            "",
            "- 10 synthetic cases in the original evaluation set",
            "- 8 cases required adjudication",
            "- one human evaluator",
            "- one LLM evaluator",
            "- one LLM adjudication process",
            "- one medical language model",
            (
                "- Rubric v1 and Taxonomy v1 remain "
                "experimental"
            ),
            "- no clinical validation",
            (
                "- no claim of generalizable "
                "inter-rater reliability"
            ),
        ]
    )

    REPORT_OUTPUT_PATH.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(
        "Day 8 adjudication report complete."
    )
    print(
        "Adjudicated cases:",
        summary["adjudicated_case_count"],
    )
    print(
        "Changed from Evaluator 1:",
        summary[
            "cases_changed_from_evaluator_1"
        ],
    )
    print(
        "Changed from Evaluator 2:",
        summary[
            "cases_changed_from_evaluator_2"
        ],
    )
    print(
        "Final safety-flagged cases:",
        summary[
            "safety_resolution"
        ]["final_safety_flagged_cases"],
    )
    print(
        "Summary:",
        SUMMARY_OUTPUT_PATH,
    )
    print(
        "Report:",
        REPORT_OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()