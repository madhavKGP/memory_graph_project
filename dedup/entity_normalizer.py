import re


def normalize_entity(name):

    if not name:
        return name

    name = name.strip()

    # email → name
    if "@" in name:

        username = name.split("@")[0]

        parts = username.split(".")

        parts = [p.capitalize() for p in parts]

        return " ".join(parts)

    # lowercase normalize
    name = name.lower()

    parts = name.split()

    parts = [p.capitalize() for p in parts]

    return " ".join(parts)