from common import first, norm, evidence_step

# Rule categories visible in the supplied deletion_rules.csv screenshot.
DEFAULT_TREATMENT = {
    "USER_PROFILE": "DELETE", "SECONDARY_IDENTIFIER": "DELETE",
    "SEARCH_INDEX_ENTRY": "DELETE", "CACHE_ENTRY": "DELETE",
    "SUPPORT_MESSAGE": "REDACT", "SUPPORT_ATTACHMENT": "DELETE",
    "ANALYTICS_PROFILE": "ANONYMIZE", "PRODUCT_TELEMETRY": "ANONYMIZE",
    "USER_EXPORT": "DELETE", "MARKETING_PROFILE": "DELETE",
    "EMAIL_DELIVERY_LOG": "REDACT", "SECURITY_AUDIT_LOG": "RETAIN",
    "LEGAL_HOLD_RECORD": "RETAIN", "BACKUP_ARCHIVE": "RETAIN",
    "ACCOUNT_TOMBSTONE": "REDACT"
}
OP_ORDER = {
    "REPORT_REMAINING_RECORD": 1, "REPORT_EXPOSED_PII": 2,
    "REPORT_ACTIVE_DATA_FLOW": 3, "REPORT_RESTORE_RISK": 4,
    "DISABLE_DATA_FLOW": 5, "BLOCK_RESTORE": 6, "DELETE_RECORD": 7,
    "REDACT_RECORD": 8, "ANONYMIZE_RECORD": 9,
    "VERIFY_RECORD_ABSENT": 10, "VERIFY_RECORD_REDACTED": 11,
    "VERIFY_RECORD_ANONYMIZED": 12, "VERIFY_RECORD_PRESENT": 13,
    "VERIFY_DATA_FLOW_DISABLED": 14, "VERIFY_RESTORE_BLOCKED": 15
}

def treatment_for(category, rules):
    for _, s in rules.iterrows():
        row = s.to_dict()
        if norm(first(row, "data_category")) == norm(category):
            return first(row, "required_action").upper()
    return DEFAULT_TREATMENT.get(str(category).upper(), "DELETE")

def make_steps(findings, status):
    """Findings are normalized dictionaries; caller must not treat reported status as proof."""
    if status == "NOT_APPLICABLE":
        return []
    if status == "COMPLETE":
        steps = []
        for f in findings:
            op = f.get("verify_operation")
            if op:
                steps.append({**f, "phase": "VERIFICATION", "operation": op,
                              "state": f.get("verify_state", ""), "evidence_id": f.get("evidence_id", "")})
        steps.sort(key=lambda x: (OP_ORDER.get(x["operation"], 99), x["system_id"], x["resource_id"]))
    else:
        steps = []
        for f in findings:
            if f.get("finding_operation"):
                steps.append({**f, "phase": "FINDING", "operation": f["finding_operation"],
                              "state": f.get("finding_state", "PRESENT"), "evidence_id": f.get("evidence_id", "")})
        for f in findings:
            if f.get("remediation_operation"):
                steps.append({**f, "phase": "REMEDIATION", "operation": f["remediation_operation"],
                              "state": f.get("remediation_state", ""), "evidence_id": ""})
        for f in findings:
            if f.get("verify_operation"):
                steps.append({**f, "phase": "VERIFICATION", "operation": f["verify_operation"],
                              "state": f.get("verify_state", ""), "evidence_id": ""})
        phase_order = {"FINDING": 0, "REMEDIATION": 1, "VERIFICATION": 2}
        steps.sort(key=lambda x: (phase_order[x["phase"]], OP_ORDER.get(x["operation"], 99),
                                  x["system_id"], x["resource_id"]))
    result = []
    for n, s in enumerate(steps, 1):
        result.append(evidence_step(n, s["phase"], s["system_id"], s["resource_id"],
                                   s["operation"], s["state"], s.get("evidence_id", "")))
    return result
