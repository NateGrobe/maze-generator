#!/usr/bin/env python3

import random
from turtle import *

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Cell:

    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.neighbours = []

    def checkWalls(self):
        return self.walls

    def removeWall(self, wall, neighbour):
        self.walls[wall] = False
        neighbour.walls[Cell.wall_pairs[wall]] = False

    def setVisited(self):
        self.visited = True

    def getVisited(self):
        return self.visited

    def getNeighbours(self, mx, my):
        if self.x > 0:
            self.neighbours.append((self.x - 1, self.y))

        if self.y > 0:
            self.neighbours.append((self.x, self.y - 1))

        if self.x < mx - 1:
            self.neighbours.append((self.x + 1, self.y))

        if self.y < my - 1:
            self.neighbours.append((self.x, self.y + 1))

        return self.neighbours

    def getCoords(self):
        return self.x, self.y


class Maze:
    def __init__(self, mx, my):
        self.mx, self.my = mx, my

        self.maze_grid = [[Cell(x, y) for y in range(self.my)] for x in range(self.mx)]

    def getCell(self, x, y):
        return self.maze_grid[x][y]

    def getGrid(self):
        return self.maze_grid

    def getUnvisNeighbour(self, cell):
        unvis_neighbours = []
        neighbours = cell.getNeighbours(self.mx, self.my)
        for i in neighbours:
            neigh_cell = self.maze_grid[i[0]][i[1]]
            if neigh_cell.getVisited() == False:
                unvis_neighbours.append(neigh_cell)
        return unvis_neighbours


def genMaze(x, y, d):
    cell_stack = Stack()
    maze = Maze(x, y)

    # Choose the initial cell, mark it as visited and push it to the stack
    current_cell = maze.getCell(0, 0)
    current_cell.setVisited()
    cell_stack.push(current_cell)

    # While the stack is not empty
    while cell_stack.isEmpty() == False:

        # Pop a cell from the stack and make it a current cell
        current_cell = cell_stack.pop()
        cx, cy = current_cell.getCoords()
        backtrack(cx, cy, d)
        unvis_cells = maze.getUnvisNeighbour(current_cell)

        # If the current cell has any neighbours which have not been visited
        if len(unvis_cells) > 0:

            # Push the current cell to the stack
            cell_stack.push(current_cell)

            # Choose one of the unvisited neighbours
            chosen_cell = unvis_cells[random.randint(0,len(unvis_cells) - 1)]
            chx, chy = chosen_cell.getCoords()
            cux, cuy = current_cell.getCoords()

            # Remove the wall between the current cell and the chosen cell
            if chx == cux - 1:
                current_cell.removeWall('N', chosen_cell)
                moveNorth(d)
            elif chy == cuy - 1:
                current_cell.removeWall('W', chosen_cell)
                moveWest(d)
            elif chx == cux + 1:
                current_cell.removeWall('S', chosen_cell)
                moveSouth(d)
            else:
                current_cell.removeWall('E', chosen_cell)
                moveEast(d)

            # Mark the chosen cell as visited and push it to the stack
            chosen_cell.setVisited()
            cell_stack.push(chosen_cell)

def moveWest(d):
    setheading(180)
    forward(d)

def moveEast(d):
    setheading(0)
    forward(d)

def moveNorth(d):
    setheading(90)
    forward(d)

def moveSouth(d):
    setheading(270)
    forward(d)

def backtrack(y, x, d):
    ty, tx = position()
    tx = int(round(tx))
    ty = int(round(ty))
    cx = 400 - y*d
    cy = -400 + x*d

    if cx != tx or ty != cy:
        color("blue")
        goto(cy,  cx)
        color("white")
    else:
        goto(cy, cx)


if __name__ == "__main__":
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
    genMaze(h, w, distance)

    mainloop()
