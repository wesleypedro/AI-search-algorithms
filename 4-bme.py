#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
""" BFS - Best-First Search algorithm with a representation using pygame """
# -----------------------------------------------------------------------------

import math
import pygame
import sys
import random
from tkinter import messagebox, Tk

dimension = (width, height) = 640, 480

pygame.init()
window = pygame.display.set_mode(dimension)
window_title = "Best-First Search - BFS - Busca Pelo Melhor Primeiro/Busca Pela Melhor Escolha"
clock = pygame.time.Clock()

columns, rows = 64, 48
# columns, rows = 32, 24
cell_width = width//columns
cell_height = height//rows

grid = []
start_cell = []
end_cell = []

to_visit = []
visited = []
path = []

# Defines whether a random wall will be generated or not
set_random_wall = True         # True or False

# Defines whether the start_cell is at coordinates [0,0] or randomly generated coordinates
set_random_start_cell = False   # True or False

# Defines if the end cell is at predefined or randomly generated coordinates
set_random_end_cell = False     # True or False

# Defines if the diagonal movement is allowed or not
set_diagonal_movement = True    # True or False


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.wall = False
        self.previous = None

        self.distance = 0
        self.visited = False

        if set_random_wall and random.randint(0,100) < 20:
            self.wall = True
    
    def show(self, window, color, shape='rect'):
        if self.wall:
            color = (0, 0, 0)
        if shape == 'rect':
            pygame.draw.rect(window, color, (self.x*cell_width, self.y*cell_height, cell_width-1, cell_height-1))
        else:
            pygame.draw.circle(window, color, (self.x*cell_width+cell_width//2, self.y*cell_height+cell_height//2), cell_width//3)
    
    def add_neighbors(self, grid):
        # # Add neighbors at the top, right, bottom and left
        # if self.y > 0:
        #     self.neighbors.append(grid[self.x][self.y-1])
        # if self.x < columns - 1:
        #     self.neighbors.append(grid[self.x+1][self.y])
        # if self.y < rows - 1:
        #     self.neighbors.append(grid[self.x][self.y+1])
        # if self.x > 0:
        #     self.neighbors.append(grid[self.x-1][self.y])

        # Add neighbors at left, bottom, right, top respectively
        # Diagonals are added if and only if they are set to be added
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.x < columns - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])


def wall_manager(position, set_wall):
    global grid
    c = position[0] // cell_width
    r = position[1] // cell_height
    grid[c][r].wall = set_wall


def calculate_heuristic(current_cell, end_cell):
    # Manhattan distance
    return abs(current_cell.x - end_cell.x) + abs(current_cell.y - end_cell.y)

    # # Euclidian distance
    # return math.sqrt((current_cell.x - end_cell.x)**2 + (current_cell.y - end_cell.y)**2)


def set_title(paused):
    global window_title
    if paused:
        pygame.display.set_caption("[PAUSED] " + window_title)
    else:
        pygame.display.set_caption(window_title)


def create_grid():
    global grid
    for c in range(columns):
        arr = []
        for r in range(rows):
            arr.append(Cell(c, r))
        grid.append(arr)


def add_neighbors_to_cell():
    global grid
    for c in range(columns):
        for r in range(rows):
            grid[c][r].add_neighbors(grid)


def define_start_and_end_cell():
    global start_cell
    global end_cell

    if set_random_start_cell:
        start_cell = grid[random.randint(0, columns-1)][random.randint(0, rows-1)]
    else:
        start_cell = grid[0][0]
    
    if set_random_end_cell:
        end_cell = grid[random.randint(0, columns-1)][random.randint(0, rows-1)]
    else:
        end_cell = grid[columns - (columns//3) + (columns%5)][rows - (rows//8) + (rows%3)]

    start_cell.wall = False
    end_cell.wall = False
    start_cell.distance = calculate_heuristic(start_cell, end_cell)
    to_visit.append(start_cell)


def close():
    pygame.quit()
    sys.exit()


def main():
    background_color = (118, 54, 38)
    start_color = (50, 255, 50)
    to_visit_color = (144, 175, 197)
    visited_color = (51, 107, 135)
    path_color = (75, 135, 165)
    path_circle_color = (42, 49, 50)
    end_color = (255, 50, 50)

    paused = False
    running = False
    flag = False
    noFlag = True

    set_title(paused)
    create_grid()
    # add_neighbors_to_cell()
    define_start_and_end_cell()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    wall_manager(pygame.mouse.get_pos(), event.button==1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    wall_manager(pygame.mouse.get_pos(), event.buttons[0])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                if event.key == pygame.K_RETURN:
                    running = True
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    set_title(paused)
        

        if paused:
            continue
        
        if running:

            if len(to_visit) > 0 and not flag:
                
                current_cell = to_visit.pop(0)

                if  current_cell == end_cell:
                    temporary = current_cell
                    sum_nodes_vertices = 0
                    sum_nodes_distances = 0
                    while temporary.previous:
                        path.append(temporary.previous)
                        sum_nodes_vertices += 1
                        sum_nodes_distances += temporary.distance
                        temporary = temporary.previous
                        
                    if not flag:
                        flag = True
                        Tk().wm_withdraw()
                        messagebox.showinfo("Solution Found", "Solution was found!\nPath length: " + str(sum_nodes_vertices) + "\nTotal Path Distance: " + str(sum_nodes_distances))
                    elif flag:
                        continue

                if flag == False:

                    current_cell.visited = True
                    visited.append(current_cell)

                    current_cell.add_neighbors(grid)

                    for cn in current_cell.neighbors:
                        if cn.wall or cn.visited:
                            continue

                        if cn not in visited and cn not in to_visit:
                            cn.previous = current_cell
                            cn.distance = calculate_heuristic(cn, end_cell)
                            to_visit.append(cn)
                        
                        elif cn in visited and cn.distance < current_cell.distance:
                            cn.previous = current_cell
                            visited.remove(cn)
                            to_visit.append(cn)
                            
                    to_visit.sort(key=lambda x: x.distance)
            
            else:
                if not flag and noFlag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution Found", "There was no solution!")
                    noFlag = False
                else:
                    continue
        

        window.fill(background_color)

        for c in range(columns):
            for r in range(rows):
                cell = grid[c][r]
                cell.show(window, to_visit_color)

                if flag and cell in path:
                    cell.show(window, path_color)
                    cell.show(window, path_circle_color, 'circle')
                elif cell in visited:
                    cell.show(window, visited_color)
                if cell in to_visit and not flag:
                    cell.show(window, to_visit_color)
                    cell.show(window, visited_color, 'circle')

                if cell == start_cell:
                    cell.show(window, start_color)
                if cell == end_cell:
                    cell.show(window, end_color)


        clock.tick(60)
        
        pygame.display.update()


if __name__ == '__main__':
    main()