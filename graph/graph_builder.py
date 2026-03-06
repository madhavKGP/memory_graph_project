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

        # normalize + canonicalize
        entity_name = normalize_entity(entity["name"])
        entity = canonicalize_entity(
            {"name": entity_name, "type": entity["type"]}
        )

        name = entity["name"]
        entity_type = entity["type"]

        if not self.graph.has_node(name):

            self.graph.add_node(
                name,
                type=entity_type
            )

    def ensure_node(self, name, default_type="Concept"):

        name = normalize_entity(name)

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

        subject = normalize_entity(claim["subject"])
        relation = normalize_relation(claim["relation"])
        obj = normalize_entity(claim["object"])

        evidence = claim["evidence"]

        # Ensure nodes exist
        subject = self.ensure_node(subject)
        obj = self.ensure_node(obj)

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
            evidence=[evidence]
        )

    # -------------------------
    # EXTRACTION INGESTION
    # -------------------------

    def add_extraction(self, extraction):

        for entity in extraction["entities"]:
            self.add_entity(entity)

        for claim in extraction["claims"]:
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