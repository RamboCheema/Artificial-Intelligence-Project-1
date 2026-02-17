import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import heapq

ROWS = 15
COLS = 15

print("Select Algorithm:")
print("1. BFS")
print("2. DFS")
print("3. UCS")
print("4. DLS")
print("5. IDDFS")
print("6. BIDIRECTIONAL")

choice = input("Enter choice number: ")

algorithms = {
    "1": "BFS",
    "2": "DFS",
    "3": "UCS",
    "4": "DLS",
    "5": "IDDFS",
    "6": "BIDIRECTIONAL"
}

ALGORITHM = algorithms.get(choice, "BFS")

def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    grid[10][2] = 2   # Start
    grid[5][10] = 3   # Target

    for i in range(2, 13):
        grid[i][7] = 1   # Wall

    return grid

grid = create_grid()
start = (10, 2)
target = (5, 10)

moves = [
    (-1, 0), (0, 1), (1, 0), (0, -1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

#  Using RGB Color Map for Giving Colors #

color_map = {
    0: (1, 1, 1),        # White (Unexplored)
    1: (1, 0, 0),        # Red (Wall)
    2: (0, 0, 1),        # Blue (Start)
    3: (0, 1, 0),        # Green (Target)
    4: (1, 1, 0),        # Yellow (Frontier)
    5: (0.8, 0.8, 0.8),  # Light Gray (Visited)
    6: (0.6, 0, 0.6)     # Purple (Path)
}


def draw():
    plt.clf()
    plt.title("GOOD PERFORMANCE TIME APP - " + ALGORITHM)

    image = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(color_map[grid[i][j]])
        image.append(row)

    plt.imshow(image)

    for i in range(ROWS):
        for j in range(COLS):
            value = grid[i][j]

            if value == 0:
                text = "0"
            elif value == 1:
                text = "-1"
            elif value == 2:
                text = "S"
            elif value == 3:
                text = "T"
            else:
                text = ""

            plt.text(j, i, text,
                     ha='center', va='center',
                     fontsize=7, color='black')

    plt.xticks(range(COLS))
    plt.yticks(range(ROWS))
    plt.grid(True)

    # Show the Patches for Enhancing the User Experience
    legend_items = [
        mpatches.Patch(color=color_map[0], label='Unexplored (0)'),
        mpatches.Patch(color=color_map[1], label='Wall (-1)'),
        mpatches.Patch(color=color_map[2], label='Start (S)'),
        mpatches.Patch(color=color_map[3], label='Target (T)'),
        mpatches.Patch(color=color_map[4], label='Frontier'),
        mpatches.Patch(color=color_map[5], label='Visited'),
        mpatches.Patch(color=color_map[6], label='Final Path')
    ]

    plt.legend(handles=legend_items, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.pause(0.05)

# BFS Algorithm

def bfs():
    queue = [start]
    visited = set([start])
    parent = {}

    while queue:
        current = queue.pop(0)

        if current == target:
            return parent

        for move in moves:
            nr = current[0] + move[0]
            nc = current[1] + move[1]

            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != 1 and (nr, nc) not in visited:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw()

    return parent

# DFS Algorithm

def dfs():
    stack = [start]
    visited = set([start])
    parent = {}

    while stack:
        current = stack.pop()

        if current == target:
            return parent

        for move in moves:
            nr = current[0] + move[0]
            nc = current[1] + move[1]

            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != 1 and (nr, nc) not in visited:
                    stack.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw()

    return parent

# UCS Algorithm
def ucs():
    pq = []
    heapq.heappush(pq, (0, start))
    parent = {}
    cost = {start: 0}

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current == target:
            return parent

        for move in moves:
            nr = current[0] + move[0]
            nc = current[1] + move[1]

            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != 1:
                    new_cost = current_cost + 1
                    if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                        cost[(nr, nc)] = new_cost
                        heapq.heappush(pq, (new_cost, (nr, nc)))
                        parent[(nr, nc)] = current
                        if grid[nr][nc] == 0:
                            grid[nr][nc] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw()

    return parent

# DLS Algorithm

def dls(limit):
    stack = [(start, 0)]
    parent = {}
    visited = set([start])

    while stack:
        current, depth = stack.pop()

        if current == target:
            return parent

        if depth < limit:
            for move in moves:
                nr = current[0] + move[0]
                nc = current[1] + move[1]

                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if grid[nr][nc] != 1 and (nr, nc) not in visited:
                        stack.append(((nr, nc), depth + 1))
                        visited.add((nr, nc))
                        parent[(nr, nc)] = current
                        if grid[nr][nc] == 0:
                            grid[nr][nc] = 4

        if current != start:
            grid[current[0]][current[1]] = 5

        draw()

    return parent

# IDDFS Algorithm 

def iddfs():
    for depth in range(1, ROWS * COLS):
        grid[:] = create_grid()
        result = dls(depth)
        if target in result:
            return result
    return {}

#BiDirectional Algorithm
def bidirectional():
    from collections import deque

    queue_start = deque([start])
    queue_goal = deque([target])

    parent_start = {start: None}
    parent_goal = {target: None}

    while queue_start and queue_goal:

        current_start = queue_start.popleft()
        for move in moves:
            ns = (current_start[0] + move[0], current_start[1] + move[1])
            if 0 <= ns[0] < ROWS and 0 <= ns[1] < COLS:
                if grid[ns[0]][ns[1]] != 1 and ns not in parent_start:
                    parent_start[ns] = current_start
                    queue_start.append(ns)
                    if ns in parent_goal:
                        parent_start.update(parent_goal)
                        return parent_start

        current_goal = queue_goal.popleft()
        for move in moves:
            ng = (current_goal[0] + move[0], current_goal[1] + move[1])
            if 0 <= ng[0] < ROWS and 0 <= ng[1] < COLS:
                if grid[ng[0]][ng[1]] != 1 and ng not in parent_goal:
                    parent_goal[ng] = current_goal
                    queue_goal.append(ng)

        draw()

    return {}

def run_algorithm():
    if ALGORITHM == "BFS":
        return bfs()
    elif ALGORITHM == "DFS":
        return dfs()
    elif ALGORITHM == "UCS":
        return ucs()
    elif ALGORITHM == "DLS":
        return dls(10)
    elif ALGORITHM == "IDDFS":
        return iddfs()
    elif ALGORITHM == "BIDIRECTIONAL":
        return bidirectional()
def draw_path(parent):
    node = target
    while node in parent and parent[node] is not None:
        node = parent[node]
        if node != start:
            grid[node[0]][node[1]] = 6
        draw()

plt.figure(figsize=(10, 7))
parents = run_algorithm()
draw_path(parents)
plt.show()
