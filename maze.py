#!/usr/bin/env python3

import random
from turtle import *
from stack import Stack

# defines each cell of the maze
class Cell:

    # used when removing wall from between current cell and neighbor
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.neighbours = []

    # removes wall between current cell and neighbour cell
    def remove_wall(self, wall, neighbour):
        self.walls[wall] = False
        neighbour.walls[Cell.wall_pairs[wall]] = False

    # sets visted status to true
    def set_visited(self):
        self.visited = True

    # returns visited status
    def get_visited(self):
        return self.visited

    # returns neighbouring cells in relation to current cell
    def get_neighbours(self, mx, my):
        if self.x > 0:
            self.neighbours.append((self.x - 1, self.y))

        if self.y > 0:
            self.neighbours.append((self.x, self.y - 1))

        if self.x < mx - 1:
            self.neighbours.append((self.x + 1, self.y))

        if self.y < my - 1:
            self.neighbours.append((self.x, self.y + 1))

        return self.neighbours

    # returns current cells coordinates
    def get_coordinates(self):
        return self.x, self.y


# maze object for storing cells
class Maze:
    def __init__(self, mx, my):
        self.mx, self.my = mx, my
        self.maze_grid = [[Cell(x, y) for y in range(self.my)] for x in range(self.mx)]

    # returns current cell
    def get_cell(self, x, y):
        return self.maze_grid[x][y]

    # returns all unvisited neighbours of current cell
    def get_univis_neighbor(self, cell):
        unvis_neighbours = []
        neighbours = cell.get_neighbours(self.mx, self.my)
        for i in neighbours:
            neigh_cell = self.maze_grid[i[0]][i[1]]
            if neigh_cell.get_visited() == False:
                unvis_neighbours.append(neigh_cell)
        return unvis_neighbours

# generates maze and runs backtracking algorithm
def gen_maze(x, y, d):
    cell_stack = Stack()
    maze = Maze(x, y)

    # Choose the initial cell, mark it as visited and push it to the stack
    current_cell = maze.get_cell(0, 0)
    current_cell.set_visited()
    cell_stack.push(current_cell)

    # While the stack is not empty
    while cell_stack.isEmpty() == False:

        # Pop a cell from the stack and make it a current cell
        current_cell = cell_stack.pop()
        cx, cy = current_cell.get_coordinates()
        backtrack(cx, cy, d)
        if cx == x-1 and cy == y-1:
            unvis_cells = []
        else:
            unvis_cells = maze.get_univis_neighbor(current_cell)

        # If the current cell has any neighbours which have not been visited
        if len(unvis_cells) > 0:

            # Push the current cell to the stack
            cell_stack.push(current_cell)

            # Choose one of the unvisited neighbours
            # if currently at bottom right corner, force it to be an exit
            if ((cx == x-1 and cy == y-2) or (cx == x-2 and cy == y-1)) and maze.get_cell(x-1, y-1).get_visited() == False:
                chosen_cell = maze.get_cell(x-1, y-1)
            else:
                chosen_cell = unvis_cells[random.randint(0,len(unvis_cells) - 1)]
            chx, chy = chosen_cell.get_coordinates()
            cux, cuy = current_cell.get_coordinates()

            # Remove the wall between the current cell and the chosen cell
            if chx == cux - 1:
                current_cell.remove_wall('N', chosen_cell)
                move_north(d)
            elif chy == cuy - 1:
                current_cell.remove_wall('W', chosen_cell)
                move_west(d)
            elif chx == cux + 1:
                current_cell.remove_wall('S', chosen_cell)
                move_south(d)
            else:
                current_cell.remove_wall('E', chosen_cell)
                move_east(d)

            # Mark the chosen cell as visited and push it to the stack
            chosen_cell.set_visited()
            cell_stack.push(chosen_cell)

# sets turtle heading west
def move_west(d):
    setheading(180)
    forward(d)

# sets turtle heading east
def move_east(d):
    setheading(0)
    forward(d)

# sets turtle heading north
def move_north(d):
    setheading(90)
    forward(d)

# sets turtle heading south
def move_south(d):
    setheading(270)
    forward(d)

# if dead-end is reached then it returns the algorithm to the last cell with unvisited neighbours
def backtrack(y, x, d):
    ty, tx = position()
    tx = int(round(tx))
    ty = int(round(ty))
    cx = 400 - y*d
    cy = -400 + x*d

    # changes turtle colour from white to blue to better visualize backtracking
    if cx != tx or ty != cy:
        color("blue")
        goto(cy,  cx)
        color("white")
    else:
        goto(cy, cx)


if __name__ == "__main__":

    # driver code
    w = int(input("Width?\n>"))
    h = int(input("Height?\n>"))

    if w >= h:
        big = w
    else:
        big = h

    distance = 800 // big

    setup(width=1000, height=1000, startx=0, starty=0)
    bgcolor("grey")
    hideturtle()
    color("white")
    width((800 / big) * .75)
    speed(0)
    penup()
    goto(-400, 400)
    hideturtle()
    pendown()
    gen_maze(h, w, distance)

    mainloop()
