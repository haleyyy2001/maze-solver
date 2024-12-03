# Maze Solver: Search Algorithms for Pathfinding

## Project Overview

This repository contains the implementation of a search agent capable of solving mazes using four fundamental search algorithms. The agent, designed for robotic pathfinding tasks, navigates through a maze to find an optimal path from a designated start point (`s`) to a goal point (`g`) while avoiding obstacles (`o`). The implemented algorithms include Breadth-First Search (BFS), Depth-First Search (DFS), A* Search, and Iterative Deepening A* (IDA*).

## Features

- **Maze Representation:** Supports rectangular grids with walls, obstacles, and open paths.
- **Search Algorithms:**
  - **BFS:** Explores all nodes level by level, ensuring optimal paths for uniform cost scenarios.
  - **DFS:** Explores as deep as possible, using backtracking to find paths.
  - **A* Search:** Combines cost-so-far with an admissible heuristic (Manhattan distance) for efficient and optimal search.
  - **IDA* Search:** Iterative deepening combined with A* heuristic for memory efficiency.
- **Performance Metrics:** Tracks statistics for each algorithm:
  - Path to goal with visualization
  - Total cost (number of steps)
  - Nodes expanded
  - Maximum nodes stored in memory
  - Maximum search depth
  - Running time
  - Peak RAM usage

## Usage

### Prerequisites
- Python 3.x
- Libraries: `resource`, `time`, `queue`

### Running the Solver
The solver accepts a maze file and a set of flags specifying the algorithms to execute.

#### Example Commands:
```bash
python3 maze.py -m maze1.txt -bfs
python3 maze.py -m maze2.txt -dfs -astar -ida
python3 maze.py -m maze3.txt -all
```

### Input Format
The maze should be a text file where:
- `s` marks the starting point.
- `g` marks the goal.
- `o` marks obstacles.
- Blank spaces (` `) represent open paths.

### Output Format
The output includes:
1. The maze with the solution path marked by `*`.
2. Performance statistics for the selected algorithms.

## Key Highlights

- **URDL Expansion Order:** Nodes are expanded in Up, Right, Down, Left order, ensuring consistency across algorithms.
- **Optimized Data Structures:** Tailored frontier management and heuristic evaluations for improved performance.
- **Comprehensive Testing:** Designed to handle small to large mazes, ensuring correctness and efficiency.

## Future Improvements
- Integration with graphical visualization tools for dynamic pathfinding demonstrations.
- Support for custom heuristics and additional search algorithms.

## License
This project is released under the MIT License. See [LICENSE](LICENSE) for details.
