import re


def normalize_person(name):

    if not name:
        return name

    name = name.lower()

    # remove email domain
    name = name.split("@")[0]

    # replace dots with spaces
    name = name.replace(".", " ")

    # remove extra spaces
    name = re.sub(r"\s+", " ", name)

    return name.title()


def canonicalize_entity(entity):

    if entity["type"] == "Person":
        entity["name"] = normalize_person(entity["name"])

    return entity