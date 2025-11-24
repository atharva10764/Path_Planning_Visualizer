import pygame
import random
from collections import deque

from core import (
    ROWS, COLS, grid,
    EMPTY, WALL, START, GOAL, OPEN, CLOSED, PATH,
    reset_search_states,
)

from algorithms import bfs, dfs, dijkstra, greedy, astar, rrt, prm

# ---------- CONFIG ----------
CELL_SIZE = 24
TOP_UI_HEIGHT = 80
FPS = 60

WALL_PROB = 0.32

# F1 color theme (RGB)
COLORS = {
    EMPTY: (255, 255, 255),   # #FFFFFF
    WALL:  (28, 28, 28),      # #1C1C1C
    START: (0, 210, 190),     # #00D2BE
    GOAL:  (45, 0, 225),      # #2D00E1
    OPEN:  (231, 19, 19),     # #E71313
    CLOSED:(106, 207, 113),   # #6ACF71
    PATH:  (255, 238, 0),     # #FFEE00
}

BG_COLOR = (106, 104, 104)      # #6A6868 window background
UI_BG = BG_COLOR
UI_TEXT = (0, 0, 0)
GRID_LINE = (239, 11, 11)

ALGO_NAMES = ["BFS", "DFS", "Dijkstra", "Greedy", "A*", "RRT", "PRM"]
ALGO_FUNCS = [
    bfs.run,
    dfs.run,
    dijkstra.run,
    greedy.run,
    astar.run,
    rrt.run,
    prm.run,
]

# ---------- GLOBAL STATE ----------
start_pos = None
goal_pos = None
running_algo = False
algo_gen = None
selected_algo_index = 4  # default A*
status_message = "Left-click: set START, then GOAL, then walls. SPACE to run."

# ---------- PYGAME INIT ----------
pygame.init()
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE + TOP_UI_HEIGHT
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("F1 Pathfinding Game (Pygame)")

clock = pygame.time.Clock()
font_small = pygame.font.SysFont("segoeui", 16)
font_title = pygame.font.SysFont("segoeui", 20, bold=True)


# ---------- CONNECTED MAP GENERATION ----------
def is_grid_connected():
    start = None
    total_free = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != WALL:
                total_free += 1
                if start is None:
                    start = (r, c)
    if start is None:
        return False

    q = deque([start])
    visited = {start}
    while q:
        cr, cc = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != WALL and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
    return len(visited) == total_free


def generate_connected_random_map():
    global start_pos, goal_pos, algo_gen, running_algo, status_message
    running_algo = False
    algo_gen = None
    start_pos = None
    goal_pos = None

    # clear grid to EMPTY (do NOT reassign grid, it's in core)
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = EMPTY

    cells = [(r, c) for r in range(ROWS) for c in range(COLS)]
    random.shuffle(cells)

    for r, c in cells:
        if random.random() < WALL_PROB:
            if grid[r][c] == WALL:
                continue
            grid[r][c] = WALL
            if not is_grid_connected():
                grid[r][c] = EMPTY

    status_message = "New map. Left-click: START, then GOAL, then walls. SPACE to run."


def clear_path_only():
    global algo_gen, running_algo, status_message
    running_algo = False
    algo_gen = None
    reset_search_states()
    if start_pos:
        grid[start_pos[0]][start_pos[1]] = START
    if goal_pos:
        grid[goal_pos[0]][goal_pos[1]] = GOAL
    status_message = "Path cleared. You can run another algorithm."


# ---------- RUN / CONTROL ----------
def run_algorithm():
    global algo_gen, running_algo, status_message

    if start_pos is None or goal_pos is None:
        status_message = "Set START and GOAL first."
        return

    reset_search_states()
    grid[start_pos[0]][start_pos[1]] = START
    grid[goal_pos[0]][goal_pos[1]] = GOAL

    algo_func = ALGO_FUNCS[selected_algo_index]
    name = ALGO_NAMES[selected_algo_index]
    algo_gen = algo_func(start_pos, goal_pos)

    running_algo = True
    status_message = f"Running {name} ..."


def handle_left_click(pos):
    global start_pos, goal_pos, status_message

    if running_algo:
        return

    x, y = pos
    if y < TOP_UI_HEIGHT:
        return  # clicked on UI bar
    grid_y = y - TOP_UI_HEIGHT
    c = x // CELL_SIZE
    r = grid_y // CELL_SIZE
    if not (0 <= r < ROWS and 0 <= c < COLS):
        return

    cell = grid[r][c]

    # 1) Set START
    if start_pos is None:
        if cell == WALL:
            grid[r][c] = EMPTY
        start_pos = (r, c)
        grid[r][c] = START
        status_message = "Start set. Now click to set GOAL."

    # 2) Set GOAL
    elif goal_pos is None:
        if (r, c) == start_pos:
            status_message = "Goal can't be on START. Click another cell."
        else:
            if cell == WALL:
                grid[r][c] = EMPTY
            goal_pos = (r, c)
            grid[r][c] = GOAL
            status_message = "Goal set. Click to toggle walls or press SPACE."

    # 3) Toggle walls
    else:
        if (r, c) == start_pos or (r, c) == goal_pos:
            return
        if cell == WALL:
            grid[r][c] = EMPTY
        elif cell in (EMPTY, OPEN, CLOSED, PATH):
            grid[r][c] = WALL


# ---------- DRAWING ----------
def draw():
    screen.fill(BG_COLOR)

    # UI bar
    pygame.draw.rect(screen, UI_BG, (0, 0, WINDOW_WIDTH, TOP_UI_HEIGHT))

    title_surf = font_title.render("Pathfinding Visualizer", True, UI_TEXT)
    screen.blit(title_surf, (16, 10))

    algo_name = ALGO_NAMES[selected_algo_index]
    algo_text = f"Algorithm: {algo_name}  [1:BFS 2:DFS 3:Dij 4:Greedy 5:A* 6:RRT 7:PRM]"
    algo_surf = font_small.render(algo_text, True, UI_TEXT)
    screen.blit(algo_surf, (16, 40))

    status_surf = font_small.render(status_message, True, UI_TEXT)
    screen.blit(status_surf, (16, 60))

    # grid
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = TOP_UI_HEIGHT + r * CELL_SIZE
            color = COLORS[grid[r][c]]
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # highlight start/goal with small circles
    if start_pos:
        sx = start_pos[1] * CELL_SIZE + CELL_SIZE // 2
        sy = TOP_UI_HEIGHT + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, (249, 250, 251), (sx, sy), CELL_SIZE // 4, 2)
    if goal_pos:
        gx = goal_pos[1] * CELL_SIZE + CELL_SIZE // 2
        gy = TOP_UI_HEIGHT + goal_pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, (249, 250, 251), (gx, gy), CELL_SIZE // 4, 2)


# ---------- MAIN LOOP ----------
def main():
    global running_algo, algo_gen, selected_algo_index, status_message

    generate_connected_random_map()

    running = True
    while running:
        dt = clock.tick(FPS)

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    run_algorithm()

                elif event.key == pygame.K_n:
                    generate_connected_random_map()

                elif event.key == pygame.K_c:
                    clear_path_only()

                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3,
                                   pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7):
                    selected_algo_index = event.key - pygame.K_1
                    algo_name = ALGO_NAMES[selected_algo_index]
                    status_message = f"Selected {algo_name}. SPACE to run."

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_left_click(event.pos)

        # --- update algorithm ---
        if running_algo and algo_gen is not None:
            try:
                for _ in range(5):  # multiple steps per frame
                    state = next(algo_gen)
                    if state in ("done", "fail"):
                        running_algo = False
                        if state == "done":
                            status_message = f"Path found with {ALGO_NAMES[selected_algo_index]}."
                        else:
                            status_message = "No path found."
                        break
            except StopIteration:
                running_algo = False

        # --- draw ---
        draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
