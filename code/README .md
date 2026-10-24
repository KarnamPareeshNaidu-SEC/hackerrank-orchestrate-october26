# Deletion Audit Agent — runnable baseline

## Files
- `main.py`: command-line entry point
- `data_loader.py`: loads all CSV inputs
- `identity_resolver.py`: resolves current and historical identifiers
- `inspect_data.py`: searches operational activity
- `evidence_analyzer.py`: reads text-readable evidence listed in the manifest
- `decision_engine.py`: per-request decision entry point
- `remediation_planner.py`: policy and ordered step helpers
- `output_validator.py`: validates output schema and JSON

## Important limitation
This is a runnable scaffold, not a verified hidden-test solution. The screenshots do not contain the actual evidence contents or full audit schemas. The current `decision_engine.py` deliberately does not fabricate evidence-backed remediation steps, and currently returns `INCOMPLETE` for deletion requests until evidence-specific logic is implemented. Do not submit it as a final high-scoring solution without implementing the evidence state reconstruction and checking against `sample_output.csv`.

## Run
From the repository root:
```bash
python -m venv .venv
# Windows PowerShell:
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r code/requirements.txt
python code/main.py
```
It expects the provided `dataset/` directory beside `code/`, and writes `output.csv` in the repository root.
