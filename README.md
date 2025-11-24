# Pathfinding Visualizer 

A fully interactive pathfinding visualizer built using **Python + Pygame** designed for clarity, animation, and educational visualization of search algorithms.

This project allows users to:

- Generate a **random connected maze**
- Choose any of the implemented algorithms
- Visually watch how each algorithm explores the grid
- Select **start** and **goal** points interactively
- Add or remove walls manually
- Clear paths without deleting the maze
- Compare performance and behavior of classical search algorithms

👉 **Inspired by Clement Mihailescu's original Pathfinding Visualizer** (React):  
https://github.com/clementmihailescu/Pathfinding-Visualizer  
This version is built completely from scratch in Python with Pygame.

---

## 🚀 Features

### ✔ Connected Random Maze  
- Generates a **fully connected** maze ensuring at least one valid path exists between any start and goal.
- Uses randomized wall placement + connectivity preservation.

### ✔ Interactive Controls  
| Action | Description |
|--------|-------------|
| **Left Click** | Set START → Set GOAL → Toggle walls |
| **SPACE** | Run the selected pathfinding algorithm |
| **N** | Generate a new random map |
| **C** | Clear only the path (keep walls + start/goal) |
| **1–7** | Switch algorithms instantly |
| **ESC** | Quit the application |

### ✔ Algorithms Implemented  
| Name | Status |
|------|--------|
| **BFS (Breadth-First Search)** | ✔ |
| **DFS (Depth-First Search)** | ✔ |
| **Dijkstra’s Algorithm** | ✔ |
| **Greedy Best-First Search** | ✔ |
| **A\*** (A-Star Search) | ✔ |
| **RRT (Rapidly-Exploring Random Trees)** | ✔ |
| **PRM (Probabilistic Roadmap Method)** | ✔ |


