import networkx as nx
from student_utils import *

def ptp_solver(G:nx.DiGraph, H:list, alpha:float):
    """
    PTP solver.

    Parameters:
        G (nx.DiGraph): A NetworkX graph representing the city.
            This directed graph is equivalent to an undirected one by construction.
        H (list): A list of home nodes.
        alpha (float): The coefficient for calculating cost.

    Returns:
        tuple: A tuple containing:
            - tour (list): A list of nodes traversed by your car.
            - pick_up_locs_dict (dict): A dictionary where:
                - Keys are pick-up locations.
                - Values are lists or tuples containing friends who get picked up
                  at that specific pick-up location. Friends are represented by
                  their home nodes.

    Notes:
    - All nodes are represented as integers.
    - The tour must begin and end at node 0.
    - The tour can only go through existing edges in the graph.
    - Pick-up locations must be part of the tour.
    - Each friend should be picked up exactly once.
    - The pick-up locations must be neighbors of the friends' home nodes or their homes.
    """
    
    # compute shortest paths
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))
    
    n = G.number_of_nodes()
    all_nodes = set(G.nodes())
    
    def compute_infeasibility(tour, H):
        tour_set = set(tour)
        infeasible_count = 0
        
        for home in H:
            # get valid nodes, with home and neighbors
            valid_locs = {home}
            for neighbor in G.neighbors(home):
                valid_locs.add(neighbor)
            
            # check if tour has valid locations
            if len(tour_set & valid_locs) == 0:
                # no valid pickup points for this one
                infeasible_count += 1
        
        return infeasible_count
    
    def calculate_cost(tour, H):
        # calculate driving cost
        driving_cost = 0
        for i in range(len(tour) - 1):
            u, v = tour[i], tour[i+1]
            if u in shortest_paths and v in shortest_paths[u]:
                driving_cost += shortest_paths[u][v]
            else:
                # nodes not feasible, set penalty
                driving_cost += 1000000
        
        # calculate walking cost
        walking_cost = 0
        tour_set = set(tour)
        
        for home in H:
            valid_locs = []
            if home in tour_set:
                valid_locs.append(home)
            for neighbor in G.neighbors(home):
                if neighbor in tour_set:
                    valid_locs.append(neighbor)
            
            if len(valid_locs) == 0:
                # infeasible with penalty
                walking_cost += shortest_paths[home][0] * 100
            else:
                # pick the closest valid location
                min_walk = float('inf')
                for loc in valid_locs:
                    if loc == home:
                        min_walk = 0
                        break
                    else:
                        walk_dist = G[home][loc]['weight']
                        if walk_dist < min_walk:
                            min_walk = walk_dist
                walking_cost += min_walk
        
        total_cost = driving_cost + alpha * walking_cost
        return total_cost
    
    T = [0]
    for k in range(1, n + 1):
        for i in all_nodes:
            T_candidate = None
            
            if i in T:
                # try to remove node i but not start node
                if i != 0:
                    T_candidate = [node for node in T if node != i]
            else:
                T_candidate = least_cost_insert(T, i, shortest_paths)
            
            if T_candidate is not None and len(T_candidate) >= 2:
                c_candidate = calculate_cost(T_candidate, H)
                c_current = calculate_cost(T, H)
                b_candidate = compute_infeasibility(T_candidate, H)
                b_current = compute_infeasibility(T, H)
                
                if b_candidate == 0:
                    # candidate is feasible
                    if b_current == 0:
                        # both feasible then take min
                        if c_candidate < c_current:
                            T = T_candidate
                            break
                    else:
                        T = T_candidate
                        break
                else:
                    if b_current > 0:
                        # both infeasible then take less infeasibility or less cost one
                        if b_candidate < b_current or (b_candidate == b_current and c_candidate < c_current):
                            T = T_candidate
                            break
        
        c_current = calculate_cost(T, H)
        b_current = compute_infeasibility(T, H)
        
        if b_current == 0:
            # feasible solution to improve
            break
    
    # start and end at 0
    if T[0] != 0:
        T = [0] + T
    if T[-1] != 0:
        T.append(0)
    
    shortest_path_routes = dict(nx.all_pairs_dijkstra_path(G))
    expanded_tour = []
    
    for i in range(len(T) - 1):
        u, v = T[i], T[i+1]
        # get shortest path from u to v
        path = shortest_path_routes[u][v]
        expanded_tour.extend(path[:-1])
    expanded_tour.append(T[-1])
    
    # assign friends to pickup node
    pick_up_locs_dict = {}
    tour_set = set(expanded_tour)
    
    for home in H:
        valid_locs = []
        if home in tour_set:
            valid_locs.append((0, home))
        for neighbor in G.neighbors(home):
            if neighbor in tour_set:
                valid_locs.append((G[home][neighbor]['weight'], neighbor))
        
        if valid_locs:
            valid_locs.sort()
            # choose closet one
            _, best_loc = valid_locs[0]
            
            if best_loc not in pick_up_locs_dict:
                pick_up_locs_dict[best_loc] = []
            pick_up_locs_dict[best_loc].append(home)
    
    return expanded_tour, pick_up_locs_dict


def least_cost_insert(tour, node, shortest_paths):
    if len(tour) == 1:
        return [tour[0], node, tour[0]]
    
    best_tour = None
    best_cost = float('inf')
    
    # try each position
    for pos in range(1, len(tour)):
        new_tour = tour[:pos] + [node] + tour[pos:]
        cost = 0
        for i in range(len(new_tour) - 1):
            u, v = new_tour[i], new_tour[i+1]
            if u in shortest_paths and v in shortest_paths[u]:
                cost += shortest_paths[u][v]
            else:
                cost += 1000000
        
        if cost < best_cost:
            best_cost = cost
            best_tour = new_tour
    
    return best_tour if best_tour else tour


if __name__ == "__main__":
    pass
