def image_to_edges(channel):
    rows, cols = channel.shape
    edges = []
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j

            if j + 1 < cols:  # right
                right_idx = i * cols + (j + 1)
                w = abs(int(channel[i, j]) - int(channel[i, j + 1]))
                edges.append((idx, right_idx, w))

            if i + 1 < rows:  # down
                down_idx = (i + 1) * cols + j
                w = abs(int(channel[i, j]) - int(channel[i + 1, j]))
                edges.append((idx, down_idx, w))

    return edges, rows, cols


def find(parent, node):
    while parent[node] != node:
        parent[node] = parent[parent[node]]
        node = parent[node]
    return node


def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if xroot == yroot:
        return

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    else:
        parent[yroot] = xroot
        if rank[xroot] == rank[yroot]:
            rank[xroot] += 1


def kruskal_mst(channel):
    edges, rows, cols = image_to_edges(channel)
    edges.sort(key=lambda e: e[2])

    size = rows * cols
    parent = {i: i for i in range(size)}
    rank = {i: 0 for i in range(size)}

    mst_adj = {i: [] for i in range(size)}

    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_adj[u].append((v, w))
            mst_adj[v].append((u, w))

    return mst_adj, rows, cols


def dfs_order(mst_adj, start_node, size):
    visited, stack, order = set(), [start_node], []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)

            for nbr, _ in reversed(mst_adj[node]):
                if nbr not in visited:
                    stack.append(nbr)

    # fill remaining nodes (safe)
    for node in range(size):
        if node not in visited:
            order.append(node)

    return order
