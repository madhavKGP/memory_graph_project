def dfs_reasoning(graph, start_entity, max_depth=2):

    visited = set()
    paths = []

    def dfs(node, path, depth):

        if depth > max_depth:
            return

        for neighbor in graph.neighbors(node):

            edge_data = graph.get_edge_data(node, neighbor)

            relation = edge_data["relation"]

            new_path = path + [(node, relation, neighbor)]

            paths.append(new_path)

            if neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, new_path, depth + 1)

    dfs(start_entity, [], 0)

    return paths