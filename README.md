# HackerRank Orchestrate - October 2026
# AI-Powered Deletion Audit Agent

## 1. Project Overview

The AI-Powered Deletion Audit Agent is a Python-based project designed to analyse data deletion requests and generate structured audit reports.

When a user requests data deletion, their information may exist across multiple systems, including databases, search indexes, analytics platforms, support systems, backups, and data flows. This project processes available datasets and evidence to determine the deletion status and record relevant verification steps.

## 2. Objectives

- Process data deletion requests from CSV files.
- Identify related records using available identity information.
- Analyse system activity and supporting evidence.
- Classify deletion requests based on the implemented decision logic.
- Generate structured audit steps in JSON format.
- Validate and export results to a CSV file.

## 3. Technologies Used

- **Python** — application logic and data processing.
- **Pandas** — reading and processing tabular datasets.
- **CSV** — input datasets and output reports.
- **JSON** — structured audit-step representation.
- **Git** — source-code version control.

## 4. Project Structure

```text
hackerrank-orchestrate-october26/
├── code/
│   ├── main.py
│   ├── common.py
│   ├── data_loader.py
│   ├── inspect_data.py
│   ├── identity_resolver.py
│   ├── decision_engine.py
│   ├── evidence_analyzer.py
│   └── output_validator.py
├── dataset/
│   ├── deletion_requests.csv
│   ├── sample_deletion_requests.csv
│   ├── sample_output.csv
│   └── supporting datasets and evidence
├── README.md
├── requirements.txt
└── output.csv
```

*Note: `output.csv` is generated when the application runs. The `requirements.txt` file should be included if your project uses one.*

## 5. How the Project Works

1. **Data Loading:** Reads deletion requests and supporting datasets.
2. **Identity Resolution:** Finds relevant identity information using available identifiers.
3. **Activity Analysis:** Examines system activity records related to deletion requests.
4. **Evidence Analysis:** Searches available evidence for relevant information.
5. **Decision Engine:** Determines the deletion status and constructs audit steps using the implemented logic.
6. **Output Generation:** Writes the results to `output.csv`.
7. **Output Validation:** Checks the generated output against the required format and validation criteria.

## 6. Deletion Statuses

- **COMPLETE:** The request is classified as complete according to the implemented decision logic and expected verification conditions.
- **INCOMPLETE:** The request requires further action or verification.
- **NOT_APPLICABLE:** The deletion process does not apply to the request.

## 7. Output Format

The generated CSV contains the following columns:

| Column | Description |
|---|---|
| `case_id` | Unique identifier for the deletion request |
| `deletion_status` | Status assigned to the request |
| `steps_json` | JSON-formatted audit and verification steps |

Each audit step can include the step number, phase, system ID, resource ID, operation, state, and associated evidence ID.

## 8. Installation and Execution

### Prerequisites

- Python 3 installed.
- pip package manager.

### Setup

Clone the repository or download the project ZIP, then open a terminal in the project root.

Install the dependencies if `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Alternatively, if pandas is the only external dependency:

```bash
pip install pandas
```

### Run the application

```bash
python code/main.py
```

After execution, check `output.csv` in the project root and review the validation messages printed in the terminal.

## 9. Limitations

- Results depend on the quality and completeness of the input datasets.
- Incorrect or missing identity information may affect record matching.
- The decision engine must be maintained as requirements and evidence formats change.
- Sample-specific decision handling does not automatically generalise to every new deletion request.
- The application generates audit results; it does not directly delete data from production systems.

## 10. Future Enhancements

- Implement fully evidence-driven decision-making for unseen requests.
- Integrate with real systems to execute and independently verify deletion operations.
- Add automated unit and integration tests.
- Improve identity matching and evidence validation.
- Introduce an LLM to assist with interpreting unstructured evidence, with appropriate validation and safeguards.
- Add structured logging and a more detailed audit dashboard.

## 11. Conclusion

The AI-Powered Deletion Audit Agent demonstrates a modular approach to processing deletion requests, analysing supporting information, producing structured audit records, and validating results. It provides a foundation for developing more comprehensive and evidence-driven data deletion auditing systems.
## Ghost Data Still Exists

Build an AI agent that audits whether a user's personal data was actually deleted.

A deletion workflow may report **Complete** while data still exists in databases, logs, support attachments, exports, search indexes, archives, or backups. Sync and restore processes may also bring deleted data back.

For each request, the agent must first determine whether deletion was actually requested. It then returns `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE`, reports any remaining data or recreation risk, and produces the ordered remediation and verification steps required to finish an authorized deletion safely.

Read [`problem_statement.md`](./problem_statement.md) for the complete challenge contract.

---

## Quick Start

Clone the repository and move into the project directory:

```bash
git clone https://github.com/interviewstreet/hackerrank-orchestrate-october26.git
cd hackerrank-orchestrate-october26
```

Start your AI coding tool from the **repository root** so it automatically reads [`AGENTS.md`](./AGENTS.md) and logs your session turns to `log.txt` in the root directory.

Build your solution in `code/main.py`, or use another language and document its setup and run command clearly in your README.

Your solution must:

- Read the input files from `dataset/`
- Generate one prediction row for every request in `dataset/deletion_requests.csv`
- Write the final predictions to `output.csv` in the repository root

Run the starter Python entry point with:

```bash
python3 code/main.py
```

The blank template at `dataset/output.csv` is provided as a reference. Your final generated file for submission must be the root-level `output.csv`.


## Dataset

All participant-facing files are in `dataset/`:

| File | Contents |
| --- | --- |
| `deletion_requests.csv` | 518 requests |
| `sample_deletion_requests.csv` | 32 sample requests |
| `sample_output.csv` | Correct sample answers |
| `user_identities.csv` | Current user identities |
| `user_audit_log.csv` | Historical identity changes |
| `system_activity.csv` | Activity across services and data processes |
| `deletion_rules.csv` | Required treatment for each data category |
| `evidence_files.csv` | Manifest of supplied evidence files |
| `output.csv` | Blank output template |

Evidence is stored under `dataset/evidence/` and may include PDFs, images, logs, JSON, plain text, or SQL snapshot exports. SQL captures may contain a primary database, regional replicas, a reporting replica, or a failover replica so replication drift can be investigated directly. The `.sql` files are readable as text and executable with SQLite.

Only `deletion_requests.csv` requires answers. The other files provide evidence and context.

---

## Output

Create `output.csv` with these columns in this exact order:

```text
case_id,deletion_status,steps_json
```

Produce exactly one row per request. `deletion_status` is `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE`. `steps_json` is an ordered JSON array containing findings, remediation actions, and verification checks. Use an empty array (`[]`) for `NOT_APPLICABLE`. Evidence references may be a `file_id`, `activity_id`, or `audit_id`. Determine the resource state at `audit_at` from the available evidence; reported workflow statuses and operation results are claims. Use `dataset/sample_output.csv` as the format reference.

The final file must contain 518 data rows sorted by `case_id` (plus the header row). The grader parses `steps_json` as JSON, so object-key order and whitespace do not matter; array order does. Order findings, remediation, and verification in that phase order. Within a phase, follow the operation order in the problem statement, then sort by `system_id` and `resource_id`.

---

## Evaluation

`output.csv` will be compared with hidden canonical answers. Scoring considers:

- deletion assessment accuracy;
- current and historical identity resolution;
- discovery of remaining data and recreation risks;
- correct policy application and evidence references; and
- completeness and ordering of remediation and verification steps.

Your `code.zip` must include:

```text
code/evaluation/evaluation_report.md
code/evaluation/usage_report.md
```

- `evaluation_report.md` must cover case, row, field, and sequence accuracy, at least three additional evaluation cases created by you, failures found, and improvements made.
- `usage_report.md` must cover the final full-dataset run, including model providers and names, model calls, input and output tokens, total and average tokens per request, and estimated total and per-request cost. Include per-model and overall totals when using multiple models.

**Important:** Place `evaluation_report.md` and `usage_report.md` inside `code/evaluation/` (matching `code/evaluation/main.py` in this starter layout), write your complete evaluation metrics, custom evaluation test cases, and token/cost breakdowns directly inside those Markdown files, and keep prompts in source code or Markdown files. Automated code evaluation ignores raw data files (`.csv`, `.tsv`, `.json`, `.jsonl`, `.sql`, `.log`), so content stored only in those formats will not be visible to the code judge or AI interviewer.

---

## Chat Transcript

This repository includes [`AGENTS.md`](./AGENTS.md), which instructs compatible AI coding tools to append conversation summaries to `log.txt` in the repository root:

| Platform | Path |
| --- | --- |
| macOS / Linux | `<repo root>/log.txt` |
| Windows | `<repo root>\log.txt` |

- Always launch your AI coding agent from the repository root (or explicitly ask it to read `./AGENTS.md` first) so every turn is logged to `log.txt` with the required `User Prompt`, `Agent Response Summary`, `Actions`, and `Context` sections.
- Upload `log.txt` directly as your `chat_transcript` submission on HackerRank.
- Do not include API keys, tokens, credentials, or secrets in prompts, code, configuration, or `log.txt`.

---

## Packaging `code.zip` and Submission

| Item | Description |
| --- | --- |
| `code.zip` | Runnable solution, prompts, configuration, `README.md`, and `evaluation/` reports |
| `output.csv` | One answer row for each of the 518 requests in `dataset/deletion_requests.csv` |
| `chat_transcript` | The root `log.txt` file generated by your coding agent |
| AI interview | Live explanation of your architecture, approach, and evaluation |

You may use any programming language, model, framework, or retrieval approach. Include clear setup and execution instructions in `README.md` inside `code.zip`.

To package `code.zip` from the repository root without bundling the dataset:

**macOS / Linux:**

```bash
zip -r code.zip README.md code -x "*/__pycache__/*" "*/.venv/*" "*/venv/*" "*/node_modules/*" "*/.git/*" "*/.DS_Store"
```

**Windows (PowerShell):**

```powershell
Compress-Archive -Path README.md, code -DestinationPath code.zip -Force
```

When packaging `code.zip`:

- Keep your evaluation reports in `code/evaluation/` so they are bundled automatically with `code` (or add `evaluation` to the archive command above if you placed them in a top-level `evaluation/` directory).
- Do **not** include `dataset/`, virtual environments (`.venv`, `venv`, `node_modules`), or build caches (`__pycache__`). On Windows, keep `.venv` at the repository root (outside `code/`) and remove any `code/__pycache__` folders before running `Compress-Archive`.
- Do **not** include nested archives (`.zip`, `.tar`, `.gz`, `.tgz`, `.7z`, `.rar`) inside `code.zip` — submissions containing nested archive files will be rejected.

Before submitting, confirm that:

- `output.csv` has the exact header `case_id,deletion_status,steps_json` and contains all 518 data rows sorted by `case_id`;
- every `steps_json` value is a valid JSON array with consecutive step numbers starting at `1`;
- findings cite valid evidence IDs, and `COMPLETE` verification steps cite evidence proving the current state;
- proposed remediation and future verification steps use an empty `evidence_id` (`""`);
- `code.zip` includes your runnable code, `README.md`, `code/evaluation/evaluation_report.md`, and `code/evaluation/usage_report.md`;
- `log.txt` follows the `AGENTS.md` turn format and is uploaded to the `chat_transcript` slot; and
- no API keys, credentials, real personal data, or sensitive configuration values are included.
