import pickle
from data.loader import load_emails
from extraction.extractor import extract_from_email
from graph.graph_builder import MemoryGraph

from retrieval.retriever import search_graph
from retrieval.vector_index import ClaimVectorIndex
from retrieval.answer_formatter import print_answers
from retrieval.graph_reasoning import dfs_reasoning

CSV_PATH = r"D:\python\memory_graph_project\emails.csv"


def main():

    emails = load_emails(CSV_PATH, limit=5)

    graph = MemoryGraph()

    for email in emails:

        # print("\n====================")
        # print("EMAIL SUBJECT:", email["subject"])

        extraction = extract_from_email(email)

        # print("\nExtraction Result:")
        # print(extraction)

        if extraction:
            graph.add_extraction(extraction)

    graph.print_graph()

    # ----------------------------
    # SIMPLE GRAPH QUERY
    # ----------------------------

    # print("\n\nSTRING QUERY TEST")

    # query = "meeting"
    # results = search_graph(graph.graph, query)
    #  print_answers(results)

    # ----------------------------
    # SAVE GRAPH
    # ----------------------------

    with open("memory_graph.pkl", "wb") as f:
        pickle.dump(graph.graph, f)

    # ----------------------------
    # BUILD VECTOR INDEX
    # ----------------------------

    vector_index = ClaimVectorIndex()

    for u, v, data in graph.graph.edges(data=True):

        vector_index.add_claim(
            u,
            data["relation"],
            v,
            data["evidence"]
        )

    # ----------------------------
    # SAVE VECTOR INDEX
    # ----------------------------

    with open("vector_index.pkl", "wb") as f:
        pickle.dump(vector_index, f)

    # ----------------------------
    # SEMANTIC QUERY TEST
    # ----------------------------

    print("\n\nSEMANTIC QUERY TEST")

    semantic_query = "Who emailed Greg?"
    results = vector_index.search(semantic_query)
    print_answers(results)

    print("\n\nGRAPH REASONING TEST")

    paths = dfs_reasoning(graph.graph, "Phillip Allen")

    for path in paths:

        print("\nReasoning Path")

        for step in path:

            print(step[0], "--", step[1], "-->", step[2])



if __name__ == "__main__":
    main()