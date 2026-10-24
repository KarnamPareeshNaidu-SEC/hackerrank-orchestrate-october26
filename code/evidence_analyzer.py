
from pathlib import Path

from common import norm, first


def load_evidence_text(project_root: Path, manifest):
    """
    Load text-readable evidence files listed in the evidence manifest.
    """
    chunks = []
    base = project_root / "dataset"

    if manifest is None or manifest.empty:
        return chunks

    for _, series in manifest.iterrows():
        row = series.to_dict()

        relative_path = first(row, "file_path", "path")
        evidence_id = first(row, "file_id", "evidence_id")

        if not relative_path:
            continue

        path = base / str(relative_path)

        allowed_extensions = {
            ".txt", ".log", ".json", ".csv",
            ".sql", ".md"
        }

        if (
            not path.exists()
            or path.suffix.lower() not in allowed_extensions
        ):
            continue

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            chunks.append({
                "evidence_id": evidence_id,
                "path": str(relative_path),
                "content": content,
            })

        except OSError as error:
            print(f"Warning: Could not read {path}: {error}")

    return chunks


def find_evidence(identifiers, evidence_chunks):
    """
    Find evidence documents containing any resolved identifier.
    """
    hits = []

    normalized_identifiers = {
        norm(identifier)
        for identifier in identifiers
        if norm(identifier)
    }

    for chunk in evidence_chunks:
        content = norm(chunk.get("content", ""))

        if any(
            identifier in content
            for identifier in normalized_identifiers
        ):
            hits.append(chunk)

    return hits
