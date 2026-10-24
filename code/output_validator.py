
import json
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "case_id",
    "deletion_status",
    "steps_json",
]

VALID_STATUSES = {
    "COMPLETE",
    "INCOMPLETE",
    "NOT_APPLICABLE",
}


def validate_output(output_path):
    """
    Check the generated output.csv for required columns,
    valid statuses, and valid JSON in steps_json.
    """
    output_path = Path(output_path)

    if not output_path.exists():
        raise FileNotFoundError(
            f"Output file not found: {output_path}"
        )

    df = pd.read_csv(output_path, dtype=str).fillna("")

    # Validate required columns.
    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Validate deletion statuses.
    invalid_statuses = sorted(
        set(df["deletion_status"]) - VALID_STATUSES
    )

    if invalid_statuses:
        raise ValueError(
            f"Invalid deletion statuses: {invalid_statuses}"
        )

    # Validate steps_json for every row.
    for index, value in enumerate(df["steps_json"], start=2):
        try:
            steps = json.loads(value)
        except (json.JSONDecodeError, TypeError) as error:
            raise ValueError(
                f"Invalid JSON in steps_json at CSV row {index}: "
                f"{error}"
            ) from error

        if not isinstance(steps, list):
            raise ValueError(
                f"steps_json must contain a JSON list at CSV row {index}"
            )

        for step in steps:
            if not isinstance(step, dict):
                raise ValueError(
                    f"Each step must be a JSON object at CSV row {index}"
                )

    print(f"Output validation passed: {len(df)} rows.")
    return True
