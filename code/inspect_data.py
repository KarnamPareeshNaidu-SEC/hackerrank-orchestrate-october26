
from common import norm, first


def matching_activity(identifiers, activity):
    """
    Match identifiers against individual activity fields.
    Avoid broad substring matches.
    """
    found = []

    if activity is None or activity.empty:
        return found

    normalized_identifiers = {
        norm(identifier)
        for identifier in identifiers
        if norm(identifier)
    }

    if not normalized_identifiers:
        return found

    identifier_fields = {
        "email",
        "user_id",
        "subject_id",
        "subject_reference",
        "identity_id",
        "resource_id",
        "account_id",
        "customer_id",
        "request_id",
    }

    for row in activity.to_dict(orient="records"):
        matched = False

        for key, value in row.items():
            field = str(key).casefold().strip()
            field_value = norm(value)

            if field in identifier_fields:
                if field_value in normalized_identifiers:
                    matched = True
                    break

        if matched:
            found.append(row)

    return found


def describe_activity(row):
    """
    Extract standard fields from an activity record.
    """
    return {
        "activity_id": first(row, "activity_id", "event_id"),
        "event_type": first(row, "event_type", "operation"),
        "source_system": first(row, "source_system", "system_id"),
        "target_system": first(row, "target_system"),
        "resource_id": first(row, "resource_id"),
        "result": first(
            row, "reported_result", "result", "status"
        ),
        "details": first(row, "details"),
    }
