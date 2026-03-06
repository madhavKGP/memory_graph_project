import pickle
from data.loader import load_emails
from extraction.extractor import extract_from_email
from graph.graph_builder import MemoryGraph
from retrieval.vector_index import ClaimVectorIndex

print("SCRIPT STARTED")

CSV_PATH = r"D:\python\memory_graph_project\emails.csv"


def build_memory():

    print("Loading emails...")

    # limit emails to avoid massive runtime
    emails = load_emails(CSV_PATH, limit=100)

    graph = MemoryGraph()

    print("Processing emails...")

    for i, email in enumerate(emails):

        print(f"Processing email {i}")

        extraction = extract_from_email(email)

        if extraction:
            graph.add_extraction(extraction)

        if i % 100 == 0:
            print("Processed", i, "emails")

        # checkpoint
        if i % 2000 == 0 and i != 0:

            with open("memory_graph_partial.pkl", "wb") as f:
                pickle.dump(graph.graph, f)

            print("Checkpoint saved at", i)

    print("Building vector index...")

    print("Initializing embedding model...")
    vector_index = ClaimVectorIndex()
    print("Embedding model ready")

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