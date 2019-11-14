import wikipedia

map_1 = [
    [0, 1, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 1, 1]
]


def neighbors(id, m):
    r, c = id

    if m[r][c] == 0:
        return []

    r_pos = [r + dr for dr in range(-1, 2) if 0 <= r + dr < len(m)]
    c_pos = [c + dc for dc in range(-1, 2) if 0 <= c + dc < len(m[0])]

    neighbors = []
    for row in r_pos:
        for col in c_pos:
            if m[row][col] == 1 and (abs(c - col) + abs(r - row)) < 2:
                neighbors.append((row, col))

    print("Available neighbors for", id, 'were ', neighbors)
    return neighbors


def map_neighbors(id): return neighbors(id, map_1)


def BFS(source, target, neighbors, max_hops=10):
    visited = set()
    parent = {source: None}
    current = None

    # Each state-tuple is in the form (node, distance)
    q = [(source, 0)]

    while(len(q) != 0):
        current, current_distance = q.pop(0)
        print('Exploring ', current)

        if current not in visited and current_distance <= max_hops:
            visited.add(current)
            for n in neighbors(current):
                if n not in visited:
                    parent[n] = current if n not in parent else parent[n]
                    q.append((n, current_distance + 1))

                    # If target found, shortest path already found
                    if n == target:
                        print('Found target. Breaking!')
                        q = []
                        break

    if target in parent:
        reverse_path = [target]
        while reverse_path[-1] is not None:
            reverse_path.append(parent[reverse_path[-1]])
        path = reverse_path[::-1]

        print('A path was found!')
        print('The path is :', str(path[1:]))

    else:
        print("Target could not be found withing", max_hops, "steps")


# start = (0, 1)
# goal = (2, 3)

# BFS(start, goal, map_neighbors, max_hops=10)

start = 'Jonesboro Airport'
goal = 'Adolf Hitler'
BFS(start, goal, wikipedia.get_links, max_hops=5)
