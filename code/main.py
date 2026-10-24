
import json
import time
from pathlib import Path

import pandas as pd

from data_loader import load_data
from evidence_analyzer import load_evidence_text
from identity_resolver import build_graph
from decision_engine import audit_case
from output_validator import validate_output


def main():
    start_time = time.time()

    # Find the project root directory.
    root = Path(__file__).resolve().parent.parent

    print("Loading datasets...")
    data = load_data(root)

    # Check that deletion requests are available.
    requests = data.get("requests")
    if data.get("sample_requests") is not None:
        requests = data["sample_requests"]

    if requests is None:
        raise KeyError(
            "Deletion requests were not loaded. "
            "Check dataset/deletion_requests.csv."
        )

    print(f"Loaded {len(requests)} deletion requests.")

    # Build the identity graph only once.
    print("Building identity graph...")

    data["identity_graph"] = build_graph(
        data["identities"],
        data["audit"],
    )

    # Load evidence using the correct manifest key.
    print("Loading evidence...")

    evidence_manifest = data["evidence_manifest"]

    evidence_chunks = load_evidence_text(
        root,
        evidence_manifest,
    )

    print(f"Loaded {len(evidence_chunks)} evidence files.")

    # Process each deletion request.
    output_rows = []
    total = len(requests)

    print("Processing deletion requests...")

    for index, (_, request) in enumerate(
        requests.iterrows(),
        start=1,
    ):
        status, steps = audit_case(
            request,
            data,
            evidence_chunks,
        )

        output_rows.append({
            "case_id": request.get("case_id", ""),
            "deletion_status": status,
            "steps_json": json.dumps(
                steps,
                ensure_ascii=False,
            ),
        })

        if index % 25 == 0 or index == total:
            print(f"Processed {index}/{total} requests.")

    # Create the required output CSV.
    output_path = root / "output.csv"

    output_df = pd.DataFrame(
        output_rows,
        columns=[
            "case_id",
            "deletion_status",
            "steps_json",
        ],
    )

    output_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    print(f"Output saved to: {output_path}")

    # Validate the output file.
    print("Validating output...")

    validate_output(output_path)

    elapsed = time.time() - start_time

    print(f"Completed in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    main()
