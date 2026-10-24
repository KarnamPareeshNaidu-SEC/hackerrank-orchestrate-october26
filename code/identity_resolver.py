
from common import norm

IDENTITY_FIELDS = {
    "email",
    "old_email",
    "new_email",
    "previous_email",
    "phone",
    "old_phone",
    "new_phone",
    "name",
    "old_name",
    "new_name",
    "user_id",
    "identity_id",
    "email_hash",
}


def build_graph(identities, audit):
    """
    Build the identity relationship graph once.
    Related emails, names, phone numbers, and IDs
    can then be resolved without repeatedly scanning
    every row of the dataframes.
    """
    graph = {}

    for df in (identities, audit):
        if df is None or df.empty:
            continue

        columns = [
            column
            for column in df.columns
            if str(column).strip().casefold() in IDENTITY_FIELDS
        ]

        if not columns:
            continue

        for values in df[columns].itertuples(
            index=False, name=None
        ):
            values_set = {
                norm(value)
                for value in values
                if norm(value)
            }

            for value in values_set:
                graph.setdefault(value, set()).update(
                    values_set - {value}
                )

    return graph


def resolve_from_graph(email, graph):
    """
    Find all identifiers connected to the supplied email.
    """
    start = norm(email)

    if not start:
        return set()

    known = {start}
    pending = [start]

    while pending:
        current = pending.pop()

        for linked in graph.get(current, ()):
            if linked not in known:
                known.add(linked)
                pending.append(linked)

    return known


def resolve_identifiers(email, identities, audit):
    """
    Compatibility function for any other code that still
    calls resolve_identifiers directly.
    """
    graph = build_graph(identities, audit)
    return resolve_from_graph(email, graph)


def identity_rows(identifiers, identities, audit):
    """
    Return rows containing any of the supplied identifiers.
    This helper uses vectorized pandas operations.
    """
    results = []

    for df in (identities, audit):
        if df is None or df.empty:
            continue

        columns = [
            column
            for column in df.columns
            if str(column).strip().casefold() in IDENTITY_FIELDS
        ]

        if not columns:
            continue

        normalized = df[columns].fillna("").astype(str)

        normalized = normalized.apply(
            lambda column: column.str.strip().str.casefold()
        )

        mask = normalized.isin(identifiers).any(axis=1)

        results.extend(
            df.loc[mask].to_dict(orient="records")
        )

    return results
