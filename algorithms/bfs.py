# algorithms/bfs.py
from collections import deque
from core import grid, neighbors, reconstruct_path, START, GOAL, OPEN, CLOSED, PATH

def run(start, goal):
    q = deque([start])
    visited = {start}
    came_from = {}

    while q:
        current = q.popleft()
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
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = current
                q.append(nb)
                if nb != goal:
                    nr, nc = nb
                    if grid[nr][nc] not in (START, GOAL):
                        grid[nr][nc] = OPEN

        yield "step"

    yield "fail"
