import numpy
import numpy.random as rng
import matplotlib.pyplot as pyplot


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.backtrack = [0, 0, 0, 0]   # N, E, S, W
        self.solution = [0, 0, 0, 0]
        self.walls = [1, 1, 1, 1]
        self.border = [0, 0, 0, 0]
        self.visited = False

    def drawCell(self):
        if self.walls[0] == 1:
            pyplot.hlines(y=self.y,     xmin=self.x, xmax=self.x + 1, linewidth=1, color='b')
        if self.walls[1] == 1:
            pyplot.vlines(x=self.x + 1, ymin=self.y, ymax=self.y + 1, linewidth=1, color='b')
        if self.walls[2] == 1:
            pyplot.hlines(y=self.y + 1, xmin=self.x, xmax=self.x + 1, linewidth=1, color='b')
        if self.walls[3] == 1:
            pyplot.vlines(x=self.x,     ymin=self.y, ymax=self.y + 1, linewidth=1, color='b')

    def setupBorder(self, xmax, ymax):
        if self.y == 0:    self.border[0] = 1  # N border
        if self.x == xmax: self.border[1] = 1  # E border
        if self.y == ymax: self.border[2] = 1  # S border
        if self.x == 0:    self.border[3] = 1  # W border


def rand(lo, hi):
    """Inclusive randint replacement for deprecated numpy.random.random_integers."""
    return rng.randint(lo, hi + 1)


def maze(width=16, height=12):
    # Initialize 2D cell array (all walls present)
    cells = [[Cell(x, y) for y in range(height)] for x in range(width)]
    for y in range(height):
        for x in range(width):
            cells[x][y].setupBorder(width - 1, height - 1)

    # Pick a random starting cell
    start_x = rand(0, width - 1)
    start_y = rand(0, height - 1)
    print(f'Starting cell: ({start_x}, {start_y})')

    stack = []
    current_cell = cells[start_x][start_y]
    num_visited = 1
    num_total = width * height

    # DFS maze generation
    while num_visited < num_total:
        neighbours = checkNeighbours(cells, current_cell, current_cell.x, current_cell.y)
        n = len(neighbours)
        if n > 0:
            chosen = neighbours[rand(0, n - 1)]
            knockdownWallBtw(current_cell, chosen)
            stack.append(current_cell)
            current_cell = chosen
            num_visited += 1
        else:
            current_cell = stack.pop()

    # Draw all cells
    for y in range(height):
        for x in range(width):
            cells[x][y].drawCell()

    # Solve from (0,0) to (width-1, height-1)
    calcSolution(cells, 0, 0, width - 1, height - 1)

    pyplot.axis([0, width, height, 0])   # flip y so (0,0) is top-left


def checkNeighbours(cells, current_cell, x, y):
    """Return unvisited neighbours that still have all walls intact."""
    neighbours = []
    if current_cell.border[0] == 0:          # North (y decreases)
        nt = cells[x][y - 1]
        if nt.walls == [1, 1, 1, 1]:
            neighbours.append(nt)
    if current_cell.border[1] == 0:          # East
        nr = cells[x + 1][y]
        if nr.walls == [1, 1, 1, 1]:
            neighbours.append(nr)
    if current_cell.border[2] == 0:          # South (y increases)
        nb = cells[x][y + 1]
        if nb.walls == [1, 1, 1, 1]:
            neighbours.append(nb)
    if current_cell.border[3] == 0:          # West
        nl = cells[x - 1][y]
        if nl.walls == [1, 1, 1, 1]:
            neighbours.append(nl)
    return neighbours


def knockdownWallBtw(cell, nbr):
    """Remove the shared wall between two adjacent cells."""
    if nbr.y == cell.y - 1:   # neighbour is North
        cell.walls[0] = 0; nbr.walls[2] = 0
    elif nbr.x == cell.x + 1: # neighbour is East
        cell.walls[1] = 0; nbr.walls[3] = 0
    elif nbr.y == cell.y + 1: # neighbour is South
        cell.walls[2] = 0; nbr.walls[0] = 0
    elif nbr.x == cell.x - 1: # neighbour is West
        cell.walls[3] = 0; nbr.walls[1] = 0


def calcSolution(cells, startx, starty, endx, endy):
    """DFS path from start to end; plots solution in green."""
    start_cell = cells[startx][starty]
    end_cell   = cells[endx][endy]

    stack = []
    current_cell = start_cell
    current_cell.visited = True

    while current_cell != end_cell:
        neighbours = getAllNeighboursNotYetVisited(cells, current_cell)
        n = len(neighbours)
        if n > 0:
            chosen = neighbours[rand(0, n - 1)]
            chosen.visited = True
            stack.append(current_cell)
            current_cell = chosen
        else:
            current_cell = stack.pop()

    # Draw solution path
    for c in stack:
        pyplot.plot(c.x + 0.5, c.y + 0.5, linestyle='None', marker='s', color='g')
    pyplot.plot(start_cell.x + 0.5, start_cell.y + 0.5, linestyle='None',
                marker='*', color='y', markersize=20, label='Start')
    pyplot.plot(end_cell.x + 0.5,   end_cell.y + 0.5,   linestyle='None',
                marker='*', color='r', markersize=20, label='End')
    pyplot.legend(loc='upper right')


def getAllNeighboursNotYetVisited(cells, c):
    """Return reachable (no wall), unvisited neighbours."""
    neighbours = []
    if c.border[0] == 0 and c.walls[0] == 0:
        n = cells[c.x][c.y - 1]
        if not n.visited: neighbours.append(n)
    if c.border[1] == 0 and c.walls[1] == 0:
        n = cells[c.x + 1][c.y]
        if not n.visited: neighbours.append(n)
    if c.border[2] == 0 and c.walls[2] == 0:
        n = cells[c.x][c.y + 1]
        if not n.visited: neighbours.append(n)
    if c.border[3] == 0 and c.walls[3] == 0:
        n = cells[c.x - 1][c.y]
        if not n.visited: neighbours.append(n)
    return neighbours


if __name__ == '__main__':
    pyplot.figure(figsize=(10, 7))
    maze(16, 12)
    pyplot.title('Maze — ★ Start (yellow)   ★ End (red)   ■ Solution (green)')
    pyplot.tight_layout()
    pyplot.show()
