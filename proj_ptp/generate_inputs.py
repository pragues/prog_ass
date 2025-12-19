import networkx as nx
import random
import math

def generate_euclidean_graph(n, max_coord=1000):
    coords = {}
    for i in range(n):
        x = random.randint(0, max_coord)
        y = random.randint(0, max_coord)
        coords[i] = (x, y)
    
    G_sparse = nx.Graph()
    G_sparse.add_nodes_from(range(n))
    
    # add random edges to ensure connectivity
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        u, v = nodes[i], nodes[i + 1]
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        weight = max(1, int(round(dist)))
        G_sparse.add_edge(u, v, weight=weight)
    
    # connect shuffled neighbors
    num_additional_edges = min(3 * n, n * (n - 1) // 2 - (n - 1))
    all_possible_edges = [(i, j) for i in range(n) for j in range(i+1, n) if not G_sparse.has_edge(i, j)]
    
    if num_additional_edges > 0 and all_possible_edges:
        random.shuffle(all_possible_edges)
        for u, v in all_possible_edges[:num_additional_edges]:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            weight = max(1, int(round(dist)))
            G_sparse.add_edge(u, v, weight=weight)
    
    # satisfy triangle inequality
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G_sparse))
    
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            # use shortest path distance as edge weight
            weight = int(round(shortest_paths[i][j]))
            G.add_edge(i, j, weight=weight)
    
    return G

def write_input_file(filename, alpha, n, m, G, H):
    with open(filename, 'w') as f:
        # ensure format
        f.write(f"{alpha}\n")
        f.write(f"{n} {m}\n")
        f.write(" ".join(map(str, H)) + "\n")
        
        for node in range(n):
            neighbors = list(G.neighbors(node))
            degree = len(neighbors)
            f.write(f"{node} {degree}\n")
            
            for neighbor in sorted(neighbors):
                weight = G[node][neighbor]['weight']
                f.write(f"{neighbor} {weight}\n")

def generate_input(filename, alpha, max_nodes, num_friends):
    n = max_nodes
    m = num_friends
    
    # generate connected metric graph
    G = generate_euclidean_graph(n)
    
    available_nodes = list(range(1, n))
    H = sorted(random.sample(available_nodes, m))
    write_input_file(filename, alpha, n, m, G, H)


def main():
    random.seed(42)
    import os
    os.makedirs("inputs", exist_ok=True)
    generate_input("inputs/20_03.in", alpha=0.3, max_nodes=20, num_friends=10)
    generate_input("inputs/20_10.in", alpha=1.0, max_nodes=20, num_friends=10)
    generate_input("inputs/40_03.in", alpha=0.3, max_nodes=40, num_friends=20)
    generate_input("inputs/40_10.in", alpha=1.0, max_nodes=40, num_friends=20)

if __name__ == "__main__":
    main()
