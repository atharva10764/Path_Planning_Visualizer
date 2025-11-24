# algorithms/astar.py
import heapq
from core import (
    grid, neighbors, reconstruct_path,
    START, GOAL, OPEN, CLOSED, PATH, manhattan
)

def run(start, goal):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed_set:
            continue

        if current != start and current != goal:
            r, c = current
            grid[r][c] = CLOSED
        closed_set.add(current)

        if current == goal:
            path = reconstruct_path(came_from, goal)
            for (r, c) in path:
                if (r, c) not in (start, goal):
                    grid[r][c] = PATH
            yield "done"
            return

        for nb in neighbors(current):
            tentative = g_score[current] + 1
            if tentative < g_score.get(nb, float("inf")):
                came_from[nb] = current
                g_score[nb] = tentative
                f = tentative + manhattan(nb, goal)
                heapq.heappush(open_heap, (f, nb))
                nr, nc = nb
                if nb not in closed_set and (nr, nc) not in (start, goal):
                    if grid[nr][nc] not in (START, GOAL):
                        grid[nr][nc] = OPEN

        yield "step"

    yield "fail"
