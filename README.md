# Medical AI Evaluation Lab

An experimental portfolio framework for structured, reproducible evaluation of medical AI responses.

## Project Goal

The goal of this project is to build a practical medical AI evaluation workflow that goes beyond simple factual accuracy.

The current version evaluates dimensions such as:

- Medical and factual correctness
- Clinical safety
- Task completion
- Relevance
- Uncertainty handling
- Evidence support
- Communication quality
- Internal consistency

## Current Status

### Day 1
Created `Evaluation Scope v1`

### Day 2
Created `Evaluation Rubric v1`

### Day 3
Built the first working evaluation pipeline:

- Synthetic medical test cases
- Structured score validation
- Normalized scoring
- Critical safety flagging
- Automated evaluation runner
- JSON result export
- Three passing unit tests

## Project Structure

    medical-ai-evaluation-lab/
    ├── cases/
    │   └── synthetic_cases_v1.json
    ├── results/
    │   └── evaluation_results_v1.json
    ├── rubric/
    │   └── evaluation_rubric_v1.md
    ├── scope/
    │   └── evaluation_scope_v1.md
    ├── src/
    │   ├── evaluator.py
    │   └── run_evaluation.py
    ├── tests/
    │   └── test_evaluator.py
    ├── README.md
    └── requirements.txt

## Run the Evaluation

    python -m src.run_evaluation

## Run Tests

    python -m pytest -q

## Important Limitations

This project is an experimental evaluation framework.

It is not intended for:

- Direct clinical use
- Diagnosis
- Treatment decisions
- Patient management
- Regulatory validation
- Medical-device certification

The current version uses synthetic cases only.