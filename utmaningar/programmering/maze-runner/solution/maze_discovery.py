import sys
import socket
import itertools
import collections

PROMPT = 'Flytta (A,W,S,D): '
MOVE_MAP = {
    (-1, 0): 'W',
    ( 1, 0): 'S',
    ( 0,-1): 'A',
    ( 0, 1): 'D',
}
Point = tuple[int,int]

def bfs(maze: dict[Point, str], start: Point) -> dict[Point, Point | None]:
    parent_map: dict[Point, Point | None] = {start: None}
    q = collections.deque([start])
    while q:
        curr = q.pop()
        for dr, dc in MOVE_MAP.keys():
            p = curr[0] + dr, curr[1] + dc
            if maze.get(p, '#') == '#' or p in parent_map:
                continue
            parent_map[p] = curr
            if maze[p] != '?':
                q.append(p)
    return parent_map

def add_maze(maze: dict[Point, str], s: str, curr: Point) -> bool:
    view = [l for l in s.splitlines() if l and all(c in '.#?*' for c in l)]
    for r in range(len(view)):
        for c in range(len(view[0])):
            if view[r][c] == '*':
                curr = curr[0] - r, curr[1] - c
    for r in range(len(view)):
        for c in range(len(view[0])):
            p = curr[0] + r, curr[1] + c
            if maze.get(p, '?') == '?':
                maze[p] = view[r][c]
    return '.' in view[-1]

def build_path(maze: dict[Point, str], parent_map: dict[Point, Point | None], curr: Point | None):
    path = []
    while curr:
        path += [curr]
        curr = parent_map[curr]
    return path[::-1]

def read_input(soc: socket.socket) -> str:
    s = ''
    while '*' not in s or not s.endswith(PROMPT):
        s += soc.recv(1<<16).decode('utf-8')
        if 'Hej då' in s:
            break
    s = s.replace(PROMPT, '')
    print(s)
    return None if 'Hej då' in s else s

def main() -> None:
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} IP PORT')
        return
    ip, port = sys.argv[1], int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((ip, port))
        soc.sendall(b'3\n')
        maze: dict[Point, str] = {}
        pos = (0,0)
        while s := read_input(soc):
            found_end = add_maze(maze, s, pos)
            parent_map = bfs(maze, pos)

            goal_tile = '.' if found_end or all(maze[p] != '?' for p in parent_map) else '?'
            goal = max((p for p in parent_map if maze[p] == goal_tile), key=lambda p: p[0]+p[1])
            path = build_path(maze, parent_map, goal)

            # the '?' tile might be a wall, so walk one step before
            last = len(path) - (2 if goal_tile == '?' else 1)
            pos = path[last]

            cmd = []
            for i in range(last):
                (r1,c1), (r2,c2) = path[i+1], path[i]
                cmd += [MOVE_MAP[(r1-r2, c1-c2)]]
            print(''.join(cmd))
            soc.sendall('\n'.join(cmd + ['E\n']).encode('utf-8'))

if __name__ == '__main__':
    main()
