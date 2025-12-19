import networkx as nx
from mtsp_dp import mtsp_dp
from student_utils import *

def php_solver_from_tsp(G, H):
    """
    PHP solver via reduction to Euclidean TSP.

    Parameters:
        G (nx.Graph): A NetworkX graph representing the city.
            This directed graph is equivalent to an undirected one by construction.
        H (list): A list of home nodes that must be visited.

    Returns:
        list: A list of nodes traversed by your car (the computed tour).

    Notes:
        - All nodes are represented as integers.
        - Solve the problem by first transforming the PTHP problem to a TSP problem.
        - Use the dynamic programming algorithm introduced in lectures to solve TSP.
        - Construct a solution for the original PTHP problem after solving TSP.

    Constraints:
        - The tour must begin and end at node 0.
        - The tour can only traverse existing edges in the graph.
        - The tour must visit every node in H.
    """
    
    V_prime_original = sorted(set(H) | {0})
    shortest_paths = {}
    shortest_path_routes = {}
    
    # use dijkstra to compute shortest path 
    for source in V_prime_original:
        lengths, paths = nx.single_source_dijkstra(G, source)
        shortest_paths[source] = lengths
        shortest_path_routes[source] = paths
        
    old_to_new = {old_id: new_id for new_id, old_id in enumerate(V_prime_original)}
    new_to_old = {new_id: old_id for old_id, new_id in old_to_new.items()}
    
    # build reduced graph with compact node ids
    reduced_graph = nx.Graph()
    n_reduced = len(V_prime_original)
    
    for i in range(n_reduced):
        for j in range(i + 1, n_reduced):
            u_old = new_to_old[i]
            v_old = new_to_old[j]
            weight = shortest_paths[u_old][v_old]
            reduced_graph.add_edge(i, j, weight=weight)
    
    tsp_tour_compact = mtsp_dp(reduced_graph)
    
    # convert back to original id
    tsp_tour = [new_to_old[node] for node in tsp_tour_compact]
    tour = []
    
    for i in range(len(tsp_tour) - 1):
        u = tsp_tour[i]
        v = tsp_tour[i + 1]
        
        # get the shortest path from u to v
        path = shortest_path_routes[u][v]
        
        # add all nodes in the path except the end node
        tour.extend(path[:-1])
    
    # final node
    tour.append(tsp_tour[-1])
    
    return tour


if __name__ == "__main__":
    pass