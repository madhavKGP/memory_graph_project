import networkx as nx

from dedup.entity_resolution import canonicalize_entity
from dedup.relation_normalizer import normalize_relation
from dedup.entity_normalizer import normalize_entity


class MemoryGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    # -------------------------
    # ENTITY HANDLING
    # -------------------------

    def add_entity(self, entity):

        if not entity:
            return

        name = entity.get("name")
        entity_type = entity.get("type", "Entity")

        if not name:
            return

        # normalize + canonicalize
        name = normalize_entity(name)

        entity = canonicalize_entity({
            "name": name,
            "type": entity_type
        })

        name = entity["name"]
        entity_type = entity["type"]

        if not name:
            return

        if not self.graph.has_node(name):

            self.graph.add_node(
                name,
                type=entity_type
            )

    def ensure_node(self, name, default_type="Concept"):

        if not name:
            return None

        name = normalize_entity(name)

        if not name:
            return None

        if not self.graph.has_node(name):

            self.graph.add_node(
                name,
                type=default_type
            )

        return name

    # -------------------------
    # CLAIM HANDLING
    # -------------------------

    def add_claim(self, claim):

        if not claim:
            return

        subject = normalize_entity(claim.get("subject"))
        relation = normalize_relation(claim.get("relation"))
        obj = normalize_entity(claim.get("object"))
        evidence = claim.get("evidence")

        # ---- VALIDATION ----
        if not subject or not relation or not obj:
            print("Skipping invalid claim:", claim)
            return

        # Ensure nodes exist
        subject = self.ensure_node(subject)
        obj = self.ensure_node(obj)

        if not subject or not obj:
            return

        # -------------------------
        # EDGE DEDUPLICATION
        # -------------------------

        if self.graph.has_edge(subject, obj):

            edge_data = self.graph[subject][obj]

            if edge_data["relation"] == relation:

                if evidence not in edge_data["evidence"]:
                    edge_data["evidence"].append(evidence)

                return

        # Create edge
        self.graph.add_edge(
            subject,
            obj,
            relation=relation,
            evidence=[evidence] if evidence else []
        )

    # -------------------------
    # EXTRACTION INGESTION
    # -------------------------

    def add_extraction(self, extraction):

        if not extraction:
            return

        entities = extraction.get("entities", [])
        claims = extraction.get("claims", [])

        for entity in entities:
            self.add_entity(entity)

        for claim in claims:
            self.add_claim(claim)

    # -------------------------
    # DEBUG PRINT
    # -------------------------

    def print_graph(self):

        print("\nNodes:")

        for node, data in self.graph.nodes(data=True):
            print(node, data)

        print("\nClaims:")

        for u, v, data in self.graph.edges(data=True):

            print(f"\n{u} --{data['relation']}--> {v}")

            for ev in data["evidence"]:
                print("Evidence:", ev)