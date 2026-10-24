
from pathlib import Path

from common import read_csv


def load_data(project_root: Path):
    data_dir = project_root / "dataset"

    return {
        "requests": read_csv(
            data_dir / "deletion_requests.csv"
        ),
        "sample_requests": (
            read_csv(data_dir / "sample_deletion_requests.csv")
            if (data_dir / "sample_deletion_requests.csv").exists()
            else None
        ),
        "identities": read_csv(
            data_dir / "user_identities.csv"
        ),
        "audit": read_csv(
            data_dir / "user_audit_log.csv"
        ),
        "activity": read_csv(
            data_dir / "system_activity.csv"
        ),
        "rules": read_csv(
            data_dir / "deletion_rules.csv"
        ),
        "evidence_manifest": read_csv(
            data_dir / "evidence_files.csv"
        ),
    }
