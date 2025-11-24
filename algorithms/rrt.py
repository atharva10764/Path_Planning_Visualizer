# algorithms/rrt.py
from core import (
    grid, ROWS, COLS, random_free_cell,
    euclidean, START, GOAL, OPEN, PATH
)

RRT_MAX_ITERS = 4000

def run(start, goal):
    tree_parent = {start: None}
    tree_nodes = [start]

    for _ in range(RRT_MAX_ITERS):
        q_rand = random_free_cell()
        q_near = min(tree_nodes, key=lambda n: euclidean(n, q_rand))

        dr = q_rand[0] - q_near[0]
        dc = q_rand[1] - q_near[1]
        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)
        q_new = (q_near[0] + step_r, q_near[1] + step_c)

        if not (0 <= q_new[0] < ROWS and 0 <= q_new[1] < COLS):
            yield "step"
            continue
        if grid[q_new[0]][q_new[1]] == START or grid[q_new[0]][q_new[1]] == GOAL:
            # still OK
            pass
        elif grid[q_new[0]][q_new[1]] == PATH or grid[q_new[0]][q_new[1]] == OPEN:
            pass
        elif grid[q_new[0]][q_new[1]] == 1:  # WALL
            yield "step"
            continue

        if q_new in tree_parent:
            yield "step"
            continue

        tree_parent[q_new] = q_near
        tree_nodes.append(q_new)

        if q_new not in (start, goal):
            if grid[q_new[0]][q_new[1]] not in (START, GOAL):
                grid[q_new[0]][q_new[1]] = OPEN

        if q_new == goal:
            curr = q_new
            path = []
            while curr is not None:
                path.append(curr)
                curr = tree_parent[curr]
            path.reverse()
            for (r, c) in path:
                if (r, c) not in (start, goal):
                    grid[r][c] = PATH
            yield "done"
            return

        yield "step"

    yield "fail"
