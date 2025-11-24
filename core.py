# core.py
import math
import random

# ---------- GRID + CONSTANTS ----------
ROWS, COLS = 25, 40

EMPTY, WALL, START, GOAL, OPEN, CLOSED, PATH = range(7)

# Global grid shared by main + algorithms
grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


# ---------- BASIC HELPERS ----------
def neighbors(rc):
    r, c = rc
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] != WALL:
                yield (nr, nc)


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def manhattan(a, b):
    (r1, c1) = a
    (r2, c2) = b
    return abs(r1 - r2) + abs(c1 - c2)


def euclidean(a, b):
    (r1, c1) = a
    (r2, c2) = b
    return math.hypot(r2 - r1, c2 - c1)


def random_free_cell():
    while True:
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        if grid[r][c] != WALL:
            return (r, c)


def line_of_sight(a, b):
    """Check if straight line between a and b crosses any wall."""
    (r1, c1) = a
    (r2, c2) = b
    dr = r2 - r1
    dc = c2 - c1
    steps = max(abs(dr), abs(dc))
    if steps == 0:
        return grid[r1][c1] != WALL
    for i in range(steps + 1):
        rr = round(r1 + dr * i / steps)
        cc = round(c1 + dc * i / steps)
        if grid[rr][cc] == WALL:
            return False
    return True


def reset_search_states():
    """Clear OPEN/CLOSED/PATH back to EMPTY but keep walls."""
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] in (OPEN, CLOSED, PATH):
                grid[r][c] = EMPTY


def draw_segment_path(path_points, start, goal):
    """Paint continuous path between roadmap vertices (for PRM)."""
    from .core import grid as g  # optional if you save this in a package, otherwise remove this line

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
            if (rr, cc) not in (start, goal):
                if grid[rr][cc] != WALL:
                    grid[rr][cc] = PATH
