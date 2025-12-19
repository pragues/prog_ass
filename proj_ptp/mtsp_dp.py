import networkx as nx

def mtsp_dp(G):
    """
    Solve the Traveling Salesman Problem (TSP) using dynamic programming.

    Parameters:
        G (nx.Graph): A NetworkX graph representing the city.

    Returns:
        list: A list of nodes representing the computed tour.

    Notes:
        - All nodes are represented as integers.
        - The solution must use dynamic programming.
        - The tour must begin and end at node 0.
        - The tour can only traverse existing edges in the graph.
        - The tour must visit every node in G exactly once.
    """
    
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    idx_to_node = {i: node for i, node in enumerate(nodes)}
    
    # build distance matrix from shortest paths
    dist = [[float('inf')] * n for _ in range(n)]
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))
    
    for u in nodes:
        for v in nodes:
            if u == v:
                dist[node_to_idx[u]][node_to_idx[v]] = 0
            else:
                dist[node_to_idx[u]][node_to_idx[v]] = shortest_paths[u][v]
    
    # denote visited nodes with bitmask
    full_mask = (1 << n) - 1
    dp = {}
    # for reconstruction
    parent = {}
    dp[(1, 0)] = 0
    
    for size in range(2, n + 1):
        import itertools
        # iterate all subsets
        for subset in itertools.combinations(range(1, n), size - 1):
            mask = 1 | sum(1 << x for x in subset)
            # try every i as last node
            for i in subset:
                prev_mask = mask ^ (1 << i)
                min_val = float('inf')
                best_j = -1
                
                # try all possible previous nodes
                for j in range(n):
                    if (prev_mask >> j) & 1:
                        if (prev_mask, j) in dp:
                            cost = dp[(prev_mask, j)] + dist[j][i]
                            if cost < min_val:
                                min_val = cost
                                best_j = j
                
                if min_val != float('inf'):
                    dp[(mask, i)] = min_val
                    parent[(mask, i)] = best_j
    
    # find the min cost to return to 0
    min_tour_cost = float('inf')
    last_node = -1
    
    for i in range(1, n):
        if (full_mask, i) in dp:
            cost = dp[(full_mask, i)] + dist[i][0]
            if cost < min_tour_cost:
                min_tour_cost = cost
                last_node = i
    
    # reconstruct the tour path from the last node backward
    path_indices = [0]
    curr_mask = full_mask
    curr_node = last_node
    
    temp_path = []
    while curr_node != 0:
        temp_path.append(curr_node)
        prev = parent[(curr_mask, curr_node)]
        curr_mask = curr_mask ^ (1 << curr_node)
        curr_node = prev
    
    temp_path.reverse()
    path_indices.extend(temp_path)
    path_indices.append(0)
    tour = [idx_to_node[i] for i in path_indices]
    
    return tour