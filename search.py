from wikipedia import *
import os
from pprint import pprint

distances_memo_dump = 'distances_memo_dump.pl'
distances_memo = None


def BFS(source, target, neighbors, max_hops=10):
    global distances_memo

    if distances_memo == None and os.path.isfile(distances_memo_dump):
        distances_memo = pickle.load(open(distances_memo_dump, "rb"))
    elif distances_memo == None:
        distances_memo = {}

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
            neighbor_list = neighbors(current)
            neighbor_list.sort(key=lambda el: distances_memo.get(el, 100))
            for n in neighbor_list:
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
        path = reverse_path[::-1][1:]

        for i in range(len(path) - 1):
            distances_memo[path[i]] = len(path) - i - 1
        pickle.dump(distances_memo, open(distances_memo_dump, "wb"))

        print('A path was found!')
        print('The path is :', str(path))

    else:
        print("Target could not be found withing", max_hops, "steps")


goal = 'Adolf Hitler'

for _ in range(100):
    start = get_random_title()
    BFS(start, goal, get_links, max_hops=5)

pprint(distances_memo)
