def search_graph(graph, query):

    results = []

    query = query.lower()

    for u, v, data in graph.edges(data=True):

        relation = data["relation"].lower()

        if query in u.lower() or query in v.lower() or query in relation:

            results.append({
                "subject": u,
                "relation": data["relation"],
                "object": v,
                "evidence": data["evidence"]
            })

    return results