## Group13

- 122090437 QIU Runheng
- 122090669 YE Shuhuan
- 122090872 JIN Yiyao


## Question 2:

Our input generation strategy uses a two-phase approach to guarantee connectibity and the triangle inequality property:

**Phase 1: Sparse Graph Generation**

- Generate random 2D coordinates for all nodes
- Create a sparse connected graph by:
  - Randomly connecting nodes to ensure connectivity
  - Adding extra edges
  - Computing Euclidean distances as initial edge weights

**Phase 2: Metric Closure Construction**

- Use shortest path distances instead of direct Euclidean distances to satisfy triangle inequality
- Compute shortest paths between all node pairs using Dijkstra's algorithm
- Build a complete graph where edge weight(u,v) = shortest path distance from u to v in the sparse graph
- This guarantees triangle inequality: dist(u,v) ≤ dist(u,w) + dist(w,v)

This approach ensures all generated inputs pass the `ck_input` validation test.

## Question 3:

$$
\begin{array}{l}
\hline \mathbf{Algorithm\ 1}\ \text{PTP Algorithm with Insert/Delete Heuristic} \\
\hline 
T^{1} \leftarrow\{0\} \\
n=|V| \quad \triangleright \text{ Number of nodes} \\
\mathbf{for}\ k=1,2, \cdots \ \mathbf{do} \\
\quad \mathbf{for}\ i=1,2, \cdots, n \ \mathbf{do} \quad \triangleright \text{ Compute one node change of } T^{k} \\
\quad \quad \mathbf{if}\ i \in T^{k} \ \mathbf{then} \\
\quad \quad \quad T_{i}^{k}=T^{k} . \operatorname{remove}(i) \quad \triangleright \text{ Directly remove} \\
\quad \quad \mathbf{else} \\
\quad \quad \quad T_{i}^{k}=T^{k} \text {.least\_cost\_insert}(i) \\
\quad \quad \quad \triangleright \text{ Multiple places to insert. When connecting to} \\
\quad \text{a node in the tour use the shortest path to that node. Take the one with minimum } c(T) \text{.} \\
\quad \text{Notice that throughout the process we use the generalized cost function that for infeasible} \\
\quad \text{solutions we also take into account a far walking distance instead of putting infinity.} \\
\quad \quad \mathbf{end\ if} \\
\quad \mathbf{end\ for} \\
\quad \mathbf{if}\ b\left(T^{k}\right)=0 \ \mathbf{then} \\
\quad \quad i^{k}=\operatorname{argmin}_{i} \quad c\left(T_{i}^{k}\right) \quad \text{s.t. } b\left(T_{i}^{k}\right)=0 \\
\quad \mathbf{else} \\
\quad \quad i^{k}=\operatorname{argmin}_{i} \quad c\left(T_{i}^{k}\right) \quad \text{s.t. } b\left(T_{i}^{k}\right)<b\left(T^{k}\right) \\
\quad \mathbf{end\ if} \\
\quad \mathbf{if}\ c\left(T^{k}\right) \leq c\left(T_{i^{k}}^{k}\right) \text{ and } b\left(T^{k}\right)=0 \ \mathbf{then} \\
\quad \quad \text{Break} \\
\quad \mathbf{else} \\
\quad \quad T^{k+1}=T_{i^{k}}^{k} \\
\quad \mathbf{end\ if} \\
\mathbf{end\ for} \\
\hline
\end{array}
$$

We implement Algorithm 1 using the insert/delete heuristic approach.

1. **Infeasibility Function** `compute_infeasibility(tour, H)`:
   - Returns $b(T)$ = number of friends who cannot be picked up
   - A friend can be picked up if their home or any neighbor is in the tour
   - Feasible pickup locations: $\{h_m\} \cup \text{neighbors}(h_m)$

2. **Cost Function** `calculate_cost(tour, H, alpha)`:
   - Driving cost: sum of shortest path distances between consecutive nodes in tour
   - Walking cost: for each friend, the min distance to nearest valid pickup location
   - Total cost: $c(T) = \alpha \times \text{driving} + \text{walking}$
   - Uses large penalty values when infeasible

3. **Insert/Delete Operations**:
   - If node $i \in T$: try removing it (except node 0)
   - If node $i \notin T$: try inserting it at all possible positions using `least_cost_insert()`
   - `least_cost_insert()`: try all insertion positions and returns the tour with minimum driving cost

4. **Candidate Generation and Selection**:
   - For each iteration k, generate all candidate tours $T_i^k$ for every node i
   - Compute cost $c(T_i^k)$ and infeasible nodes $b(T_i^k)$ for each candidate
   - Selection strategy:
     - If $b(T^k) = 0$ (feasible): select $\arg\min_i c(T_i^k)$ among feasible candidates
     - If $b(T^k) > 0$ (infeasible): select $\arg\min_i c(T_i^k)$ with $b(T_i^k) < b(T^k)$ to reduce infeasibility and as well as cost
   - Termination condition: stop when $c(T^k) \leq c(T_{i^k}^k)$ and $b(T^k) = 0$

5. **Pickup Assignment**:
   - For each friend, find all valid pickup locations in the expanded tour
   - Assign friend to the closest valid location
   - Return tour and pickup location dictionary

**Performance:**

- **Time Complexity**: O(k × n²) where k is number of iterations (k ≤ 2n) with double n size inner iteration inside, and n is the number of nodes
  - Tour expansion: O(|V'| × L) where L is average path length
- **Space Complexity**: O(n²) for storing all-pairs shortest paths
- **Solution Quality**: Heuristic approach, not guaranteed optimal but provides good feasible solutions

## Question 4.1

We implement the Held-Karp dynamic programming algorithm to solve Metric TSP in `mtsp_dp.py`.

The Held-Karp algorithm uses bitmask dynamic programming to find the optimal TSP tour with time complexity O(n² × 2ⁿ).

1. **Node mapping**:
   - Map original node IDs to continuous indices (0, 1, 2, ..., n-1)
   - Required for bitmask representation where bit i with 0/1 indicates whether node i is visited

2. **Distance Matrix**:
   - Use `all_pairs_dijkstra_path_length` to compute shortest paths between all node pairs
   - Build distance matrix `dist[i][j]` = shortest path distance from node i to node j based on dijkstra method

3. **DP State Definition**:
   - State: `dp[(mask, last)]` = minimum cost to visit nodes in mask state and end at node last
   - `mask`: bitmask representing visited nodes, where bit i = 1 if node i visited
   - Base case: `dp[(1, 0)] = 0` (start at node 0 with only node 0 visited)

4. **DP Transition**:
   - For each subset size from 2 to n, generate all possible subsets containing node 0
   - For each subset and each possible ending node i in the subset:
     - Try all possible previous nodes j
     - Update: `dp[(mask, i)] = min(dp[(mask-{i}, j)] + dist[j][i])`
   - Track parent nodes for path reconstruction

5. **Optimal Tour Cost**:
   - Try all possible last nodes before returning to node 0
   - Find minimum: `min{dp[(full_mask, i)] + dist[i][0]}` for i = 1 to n-1

6. **Path Reconstruction**:
   - Backtrack using parent pointers from the optimal last node
   - Build tour backward from last_node → parent → parent → ... → node 0
   - Convert indices back to original node IDs

**Performance:**

- **Time Complexity**: O(n² × 2ⁿ)
  - DP: 2ⁿ × n (all subsets × all ending nodes)
  - Each state transition: O(n) (try all previous nodes)
- **Space Complexity**: O(n² × 2ⁿ) for DP table and parent tracking
- **Solution Quality**: Guarantees optimal TSP solution

## Question 4.2

We solve PHP by reducing it to M-TSP in `php_from_tsp.py`, following the three-step transformation described in the PDF.

**Steps:**

1. **Construct Complete Graph G'**:
   - Create node set V' = H ∪ {0}, home and start nodes
   - For every pair (u,v) in V', compute edge weight = shortest path distance from u to v in original graph G
   - Use `single_source_dijkstra` from each node in V' for efficiency

2. **Solve M-TSP on G'**:
   - Apply node mapping: map V' nodes to continuous indices from 0
   - Build reduced graph with mapped indices
   - Call `mtsp_dp(reduced_graph)` from Question 4.1 to get optimal tour C'
   - Convert tour back to original node IDs

3. **Expand Tour to Original Graph**:
   - For each edge (u,v) in simplified tour C', replace it with the actual shortest path from u to v in G
   - Use precomputed `shortest_path_routes[u][v]` for each edge
   - Concatenate paths while avoiding node duplication

It is valid because:

- G' is the metric closure of V' in G (a complete graph with shortest path distances)
- Triangle inequality is automatically satisfied by shortest path property
- Optimal TSP tour on G' corresponds to optimal PHP tour when expanded to G
- Expansion preserves tour cost since edge weights in G' equal actual shortest paths in G

**Performance:**

- **Time Complexity**: O(|V'|² × 2^|V'| + |V'| × |E| × log|V|)
  - Shortest path computation: O(|V'| × |E| × log|V|) using Dijkstra
  - TSP solving: O(|V'|² × 2^|V'|) for mtsp
  - Tour expansion: O(|V'| × L) where L is average path length

## Question 5.1

Show that PTP is NP-hard:

We proof by reduction: If a problem is NP-hard and if an existing NP-hard problem can be reduced to in polynomial time. We know PHP is NP-hard since M-TSP can be reduced to it. 

Consider the PTP cost function: $\alpha \sum w_{u_{i-1}u_i} + \sum d_{p_mh_m}$. If we choose a specific instance where the walking cost is extremely high compared to the driving cost i.e., by making $\alpha$ very small or the walking distances between nodes very large, the optimal solution for PTP will naturally force the pickup locations $p_m$ to be exactly the home locations $h_m$ to minimize the second term of the cost function.

Equivalence: For these specific values of $\alpha$, the solution to PTP is identical to the solution to PHP.

Conclusion: Since PHP is a special case of PTP and PHP is NP-hard, PTP must also be NP-hard

## Question 5.2

Show that the cost of PHP is at most twice of that of the optimal solution. That is $\beta = \frac{C_{php}}{C_{ptpopt}} \le 2$ Also show that this bound is tight. i.e. there is an instance where $\beta =2$ (at least asymptotically). Can assume $\alpha=1$ for simplicity. 

**Proof**: Asssume $\alpha=1$. The optimal PTP solution contains a car tour $T_{opt}$ and a set of pickup locations {$p_m$}. The optimal cost is $C_{ptpopt} = \text{Length}(T_{opt}) + \sum_{m \in F} d(h_m, p_m)$

Construct a feasible PHP solution based on $T_{opt}$. For every friend $m$, the car follows $T_{opt}$ until it reaches $p_m$. At $p_m$, the car deviates to the friend's home $h_m$ and then returns to $p_m$ before continuing the tour. The extra distance added for each friend $m$ to visit their home is at most $2 \times d(p_m, h_m)$ (the round trip from the pickup point to the home)

Total length of the constructed PHP tour: $L_{php} \le \text{Length}(T_{opt}) + \sum_{m \in F} 2 \times d(h_m, p_m)$

Since $\alpha = 1$ and walking distance in PHP is 0, the total cost $C_{php} = L_{php}$

$\therefore C_{php} \le 2 \times \left( \text{Length}(T_{opt}) + \sum_{m \in F} d(h_m, p_m) \right) = 2 \times C_{ptpopt}$

Therefore, $\beta = \frac{C_{php}}{C_{ptpopt}} \le 2$

**proof of tightness** To show the bound of $\beta =2$ is tight, we do the following construction:

- Graph Structure: A "star" graph where your house (Node 0) is the center.
- Locations: There are $n$ friends. Each friend's home $h_m$ is connected to a common intermediate node $v$ with an edge weight of $1$. Node $v$ is connected to Node 0 with a very small edge weight $\epsilon$.
- PTP Optimal Strategy: The car drives from $0 \to v \to 0$ (distance $2\epsilon$). All friends walk from $h_m$ to $v$.
- $C_{ptpopt} = 2\epsilon + n \times 1 \approx n$ (as $\epsilon \to 0$)
- PHP Optimal Strategy: The car must visit every $h_m$. Since each $h_m$ is a leaf node, the car must travel $v \to h_m \to v$ for every friend. 

$C_{php} = 2\epsilon + n \times (1 + 1) \approx 2n$.

As $n \to \infty$ and $\epsilon \to 0$, the ratio $\beta = \frac{2n}{n} = 2$