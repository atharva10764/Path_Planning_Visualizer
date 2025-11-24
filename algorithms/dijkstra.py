# algorithms/dijkstra.py
import heapq
from core import grid, neighbors, reconstruct_path, START, GOAL, OPEN, CLOSED, PATH

def run(start, goal):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    dist = {start: 0}
    visited = set()

    while open_heap:
        d, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)

        if current != start and current != goal:
            r, c = current
            grid[r][c] = CLOSED

        if current == goal:
            path = reconstruct_path(came_from, goal)
            for (r, c) in path:
                if (r, c) not in (start, goal):
                    grid[r][c] = PATH
            yield "done"
            return

        for nb in neighbors(current):
            nd = d + 1
            if nd < dist.get(nb, float("inf")):
                dist[nb] = nd
                came_from[nb] = current
                heapq.heappush(open_heap, (nd, nb))
                nr, nc = nb
                if grid[nr][nc] not in (START, GOAL):
                    grid[nr][nc] = OPEN

        yield "step"

    yield "fail"
