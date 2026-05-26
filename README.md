# 🌀 Maze Generator

A Python maze generator and solver using **Depth-First Search (DFS)** with recursive backtracking. Generates a random perfect maze and visualizes the solution path using Matplotlib.

---

## Preview

```
★ = Start (yellow)    ★ = End (red)    ■ = Solution path (green)
```

The maze is drawn using `matplotlib` line primitives — each cell's walls are individually rendered, giving a clean grid-based maze with a visible solution path from top-left to bottom-right.

---

## Features

- Random maze generation via DFS + recursive backtracking
- Guaranteed solvable — every cell is reachable (perfect maze)
- Auto-solved from any start/end coordinate
- Fully configurable width and height
- Matplotlib-based visualization

---

## Requirements

- Python 3.7+
- numpy
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python maze_fixed.py
```

To customize maze size, edit the bottom of `maze_fixed.py`:

```python
maze(width=16, height=12)   # change these values
```

Or call `maze()` in your own script:

```python
from maze_fixed import maze
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 7))
maze(width=24, height=18)
plt.show()
```

---

## How It Works

### Generation — DFS with Backtracking

1. Start at a random cell
2. Pick a random unvisited neighbor → knock down the wall between them
3. Move to that neighbor and repeat
4. If no unvisited neighbors exist → backtrack via stack
5. Repeat until all cells are visited

### Solution — DFS Pathfinding

1. Start at `(0, 0)`
2. Move through open walls (no backtracking through broken walls)
3. On dead end → backtrack
4. Continue until `(width-1, height-1)` is reached
5. Plot the solution path in green

---

## Project Structure

```
maze-generator/
├── maze_fixed.py       # Main script
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## License

MIT License — free to use, modify, and distribute.
