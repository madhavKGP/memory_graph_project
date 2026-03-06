
import re


def normalize_relation(relation: str) -> str:
    """
    Convert relation text into a normalized snake_case form.
    No hardcoded mappings.
    """

    if not relation:
        return "related_to"

    # lowercase
    relation = relation.lower()

    # remove punctuation
    relation = re.sub(r"[^\w\s]", "", relation)

    # collapse multiple spaces
    relation = re.sub(r"\s+", " ", relation)

    # trim
    relation = relation.strip()

    # convert to snake_case
    relation = relation.replace(" ", "_")

    return relation