from __future__ import annotations
import json, re
from pathlib import Path
import pandas as pd

def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")

def norm(value) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()

def safe_json(value):
    try:
        return json.loads(value)
    except Exception:
        return None

def first(row, *names, default=""):
    lookup = {str(k).casefold(): v for k, v in row.items()}
    for name in names:
        if name.casefold() in lookup and str(lookup[name.casefold()]).strip():
            return str(lookup[name.casefold()]).strip()
    return default

def evidence_step(step_no, phase, system_id, resource_id, operation, state, evidence_id=""):
    return {
        "step_no": int(step_no), "phase": phase, "system_id": system_id or "unknown_system",
        "resource_id": resource_id or "unknown_resource", "operation": operation,
        "state": state, "evidence_id": evidence_id or ""
    }
