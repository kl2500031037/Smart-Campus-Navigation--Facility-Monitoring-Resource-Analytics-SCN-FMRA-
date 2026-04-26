from collections import deque

def bfs_path(graph, start, goal):
    visited = set()
    queue = deque([(start, [], 0)])

    while queue:
        current, path, dist = queue.popleft()

        if current == goal:
            return path, dist

        if current not in visited:
            visited.add(current)

            for neighbor, direction, d in graph.get(current, []):
                queue.append((
                    neighbor,
                    path + [(current, neighbor, direction, d)],
                    dist + d
                ))

    return None, 0