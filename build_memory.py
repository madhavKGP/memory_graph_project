import pickle
from data.loader import load_emails
from extraction.extractor import extract_from_email
from graph.graph_builder import MemoryGraph
from retrieval.vector_index import ClaimVectorIndex

CSV_PATH = r"D:\python\memory_graph_project\emails.csv"


def build_memory():

    emails = load_emails(CSV_PATH)

    graph = MemoryGraph()

    print("Processing emails...")

    for i, email in enumerate(emails):

        extraction = extract_from_email(email)

        if extraction:
            graph.add_extraction(extraction)

        if i % 100 == 0:
            print("Processed", i, "emails")

    print("Building vector index...")

    vector_index = ClaimVectorIndex()

    for u, v, data in graph.graph.edges(data=True):

        vector_index.add_claim(
            u,
            data["relation"],
            v,
            data["evidence"]
        )

    print("Saving graph...")

    with open("memory_graph.pkl", "wb") as f:
        pickle.dump(graph.graph, f)

    print("Saving vector index...")

    with open("vector_index.pkl", "wb") as f:
        pickle.dump(vector_index, f)

    print("DONE")


if __name__ == "__main__":
    build_memory()