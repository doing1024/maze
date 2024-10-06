import random
from queue import Queue


def generate_maze(rows, cols):
    while True:
        maze = create_maze_structure(rows, cols)
        if is_valid_maze(maze):
            return maze


def create_maze_structure(rows, cols):
    # 初始化迷宫
    maze = [["#" for _ in range(cols)] for _ in range(rows)]

    # 创建通道
    def create_path(x, y):
        maze[y][x] = "."
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == "#":
                maze[y + dy][x + dx] = "."
                create_path(nx, ny)

    create_path(1, 1)

    # 放置玩家
    empty_cells = [
        (x, y) for y in range(rows) for x in range(cols) if maze[y][x] == "."
    ]
    player_pos = random.sample(empty_cells, 2)
    maze[player_pos[0][1]][player_pos[0][0]] = "A"
    maze[player_pos[1][1]][player_pos[1][0]] = "B"
    empty_cells = [cell for cell in empty_cells if cell not in player_pos]

    # 放置协作机关
    def place_mechanism(symbol, linked_symbol):
        positions = random.sample(empty_cells, 2)
        maze[positions[0][1]][positions[0][0]] = symbol
        maze[positions[1][1]][positions[1][0]] = linked_symbol
        empty_cells.remove(positions[0])
        empty_cells.remove(positions[1])
        return positions[0], positions[1]

    mechanism1 = place_mechanism("1", "3")
    mechanism2 = place_mechanism("2", "4")

    # 选择出口位置
    exit_pos = random.choice(empty_cells)
    maze[exit_pos[1]][exit_pos[0]] = "D"
    empty_cells.remove(exit_pos)

    # 放置假出口
    fake_exits = random.sample(empty_cells, min(3, len(empty_cells)))
    for fake in fake_exits:
        maze[fake[1]][fake[0]] = "d"

    return maze


def is_valid_maze(maze):
    rows, cols = len(maze), len(maze[0])

    def bfs(start, allowed):
        queue = Queue()
        queue.put(start)
        visited = set([start])
        while not queue.empty():
            x, y = queue.get()
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < cols
                    and 0 <= ny < rows
                    and maze[ny][nx] in allowed
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.put((nx, ny))
        return visited

    # 找到玩家和出口的位置
    player_a, player_b, exit_pos = None, None, None
    mechanisms = {"1": None, "2": None, "3": None, "4": None}
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == "A":
                player_a = (x, y)
            elif maze[y][x] == "B":
                player_b = (x, y)
            elif maze[y][x] == "D":
                exit_pos = (x, y)
            elif maze[y][x] in "1234":
                mechanisms[maze[y][x]] = (x, y)

    # 检查玩家A是否可以到达1和2
    reachable_a = bfs(player_a, ".123D")
    if mechanisms["1"] not in reachable_a or mechanisms["2"] not in reachable_a:
        return False

    # 检查玩家B是否可以到达1和2
    reachable_b = bfs(player_b, ".124D")
    if mechanisms["1"] not in reachable_b or mechanisms["2"] not in reachable_b:
        return False

    # 检查在合作的情况下是否可以到达出口
    reachable_coop = bfs(player_a, ".1234D") | bfs(player_b, ".1234D")
    if exit_pos not in reachable_coop:
        return False

    # 检查单独行动是否无法到达出口
    reachable_a_alone = bfs(player_a, ".12D")
    reachable_b_alone = bfs(player_b, ".12D")
    if exit_pos in reachable_a_alone or exit_pos in reachable_b_alone:
        return False

    return True


def print_maze(maze):
    for row in maze:
        print("".join(row))


# 生成20x20的迷宫
size = 25
maze = generate_maze(size, size)
print_maze(maze)
