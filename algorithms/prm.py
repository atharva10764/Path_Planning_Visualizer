# algorithms/prm.py
import heapq
from core import (
    grid, ROWS, COLS,
    euclidean, line_of_sight, reconstruct_path,
    START, GOAL, OPEN, CLOSED, PATH, WALL
)

PRM_SAMPLES = 200
PRM_K = 10

def _draw_segment_path(path_points):
    """Paint continuous path between roadmap vertices."""
    for i in range(len(path_points) - 1):
        a = path_points[i]
        b = path_points[i + 1]
        (r1, c1) = a
        (r2, c2) = b
        dr = r2 - r1
        dc = c2 - c1
        steps = max(abs(dr), abs(dc))
        for j in range(steps + 1):
            rr = round(r1 + dr * j / steps)
            cc = round(c1 + dc * j / steps)
            if (rr, cc) not in (path_points[0], path_points[-1]):
                if grid[rr][cc] != WALL:
                    grid[rr][cc] = PATH

def run(start, goal):
    free_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] != WALL]
    if not free_cells:
        yield "fail"
        return

    import random
    samples = random.sample(free_cells, min(PRM_SAMPLES, len(free_cells)))
    if start not in samples:
        samples.append(start)
    if goal not in samples:
        samples.append(goal)

    adjacency = {p: [] for p in samples}

    for p in samples:
        others = [q for q in samples if q != p]
        others.sort(key=lambda q: euclidean(p, q))
        for q in others[:PRM_K]:
            if line_of_sight(p, q):
                d = euclidean(p, q)
                adjacency[p].append((q, d))
                adjacency[q].append((p, d))

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

        (r, c) = current
        if current not in (start, goal):
            if grid[r][c] not in (START, GOAL, WALL):
                grid[r][c] = CLOSED

        if current == goal:
            path_points = reconstruct_path(came_from, goal)
            path_points = [start] + path_points
            _draw_segment_path(path_points)
            yield "done"
            return

        for nb, cost in adjacency.get(current, []):
            nd = d + cost
            if nd < dist.get(nb, float("inf")):
                dist[nb] = nd
                came_from[nb] = current
                heapq.heappush(open_heap, (nd, nb))
                nr, nc = nb
                if nb not in (start, goal):
                    if grid[nr][nc] not in (START, GOAL, WALL):
                        grid[nr][nc] = OPEN

        yield "step"

    yield "fail"
