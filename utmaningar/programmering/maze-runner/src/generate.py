import random
import sys

def out(text="", end="\n"):
    print(text, end=end)
    sys.stdout.flush()

def generate_maze(xm, ym):
    maze = [["#" for _ in range(xm)] for _ in range(ym) ]
    stack = [(0, 0)]

    while stack:
        current_cell = stack[-1]
        maze[current_cell[0]][current_cell[1]] = "."

        neighbours = [
            (current_cell[0] - 2, current_cell[1]),
            (current_cell[0] + 2, current_cell[1]),
            (current_cell[0], current_cell[1] - 2),
            (current_cell[0], current_cell[1] + 2)
        ]
    
        unvisited_neighbours = [neighbour for neighbour in neighbours if 0 <= neighbour[0] < ym and 0 <= neighbour[1] < xm and maze[neighbour[0]][neighbour[1]] == "#"]

        if unvisited_neighbours:
            chosen_neighbour = random.choice(unvisited_neighbours)
            wall_between = ((current_cell[0] + chosen_neighbour[0]) // 2, (current_cell[1] +  chosen_neighbour[1]) // 2)
            maze[wall_between[0]][wall_between[1]] = "."
            stack.append(chosen_neighbour)
        else:
            stack.pop()
    
    maze[0][0] = "."
    maze[ym - 1][xm - 2] = "."

    return maze

class Maze:
    def __init__(self,xm,ym):
        self.mPos = (0, 0)
        self.mXm = xm
        self.mYm = ym
        self.mMaze = generate_maze(self.mXm,self.mYm)

    def print(self,visibility):
        if not visibility:
            max_range = self.mXm
        else:
            max_range = visibility
        for y in range(max(0, self.mPos[0] - max_range - 1), min(self.mYm, self.mPos[0] + max_range + 2)):
            for x in range(max(0, self.mPos[1] - max_range - 1), min(self.mXm, self.mPos[1] + max_range + 2)):
                if self.mPos[0] == y and self.mPos[1] == x:
                    out("*",end="")
                elif visibility == 0 or (abs(self.mPos[0] - y) + abs(self.mPos[1] - x)) <= max_range:
                    out(self.mMaze[y][x],end="")
                else:
                    out("?",end="")
            out()

    def valid(self,pos):
        if pos[0] < 0 or pos[0] >= self.mYm:
            return False
        if pos[1] < 0 or pos[1] >= self.mXm:
            return False
        if self.mMaze[pos[0]][pos[1]] == '#':
            return False
        return True   

    def move(self,direction):
        if direction == 'w':
            pos = (self.mPos[0] - 1, self.mPos[1])
        elif direction == 's':
            pos = (self.mPos[0] + 1, self.mPos[1])
        elif direction == 'a':
            pos = (self.mPos[0], self.mPos[1] - 1)
        elif direction == 'd':
            pos = (self.mPos[0], self.mPos[1] + 1)
        else: 
            return False
        if not self.valid(pos):
            return False
        self.mPos = pos
        return True

    def goal(self):
        if self.mPos[0] == self.mYm - 1 and self.mPos[1] == self.mXm - 2:
            return True
        return False

        


