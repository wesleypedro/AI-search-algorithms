#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
""" UCS - Uniform Cost Search algorithm with a representation using pygame """
# -----------------------------------------------------------------------------

import pygame
import sys
import random
import numpy as np
from tkinter import messagebox, Tk

dimension = (width, height) = 640, 480

pygame.init()
window = pygame.display.set_mode(dimension)
window_title = "Uniform Cost Search - UCS - Busca de Custo Uniforme"
clock = pygame.time.Clock()


# -----------------------------------------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------------------------------------

# columns, rows = 64, 48
columns, rows = 32, 24
cell_width = width//columns
cell_height = height//rows

grid = []
start_cell = []
end_cell = []

to_visit = []
visited = []
path = []

add_weights = False
add_weight_to = None


# -----------------------------------------------------------------------------
# GLOBAL MODIFICATIONS ATRTIBUTES
# -----------------------------------------------------------------------------

# Defines whether a random wall will be generated or not
set_random_wall = False         # True or False

# Defines whether the start_cell is at coordinates [0,0] or randomly generated coordinates
set_random_start_cell = False   # True or False

# Defines if the end cell is at predefined or randomly generated coordinates
set_random_end_cell = False     # True or False

# Defines whether weights are generated randomly or not
set_random_weights = True       # True or False

# If set to True, no weight will be assigned to edges
set_weights_as_zero = True      # True or False


# -----------------------------------------------------------------------------
# CLASSE
# -----------------------------------------------------------------------------

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False
        self.previous = None

        self.neighbors = []
        
        self.right = None
        self.down = None
        self.left = None
        self.up = None

        self.right_weight = 0
        self.down_weight = 0
        self.left_weight = 0
        self.up_weight = 0

        self.distance = 0

        if set_random_wall and random.randint(0,100) < 20:
            self.wall = True
    
    def show(self, window, color, shape='rect'):
        # Font=pygame.font.SysFont('timesnewroman',  12)
        # if self.right:
        #     rw = Font.render(str(self.right_weight), True, (0,0,0))
        #     window.blit(rw, (self.x*cell_width+cell_width//2, self.y*cell_height+cell_height//2))
        # if self.down:
        #     dw = Font.render(str(self.down_weight), True, (0,0,0))
        #     window.blit(dw, (self.x*cell_width+cell_width//2, self.y*cell_height+cell_height//2))
        if self.wall:
            color = (0, 0, 0)
        if shape == 'rect':
            pygame.draw.rect(window, color, (self.x*cell_width, self.y*cell_height, cell_width-1, cell_height-1))

        else:
            pygame.draw.circle(window, color, (self.x*cell_width+cell_width//2, self.y*cell_height+cell_height//2), cell_width//3)
    
    def get_right_neighbor(self, grid):
        return grid[self.x+1][self.y] if self.x < columns - 1 else None

    def get_down_neighbor(self, grid):
        return grid[self.x][self.y+1] if self.y < rows - 1 else None
    
    def get_left_neighbor(self, grid):
        return grid[self.x-1][self.y] if self.x > 0 else None
    
    def get_up_neighbor(self, grid):
        return grid[self.x][self.y-1] if self.y > 0 else None
    
    
    def add_neighbors(self, grid):
        # Add neighbors at right, down, left, top respectively
        self.right = self.get_right_neighbor(grid)
        self.down = self.get_down_neighbor(grid)
        self.left = self.get_left_neighbor(grid)
        self.up = self.get_up_neighbor(grid)
    

    def get_neighbors(self):
        if self.up:
            self.neighbors.append(self.up)
        if self.left:
            self.neighbors.append(self.left)
        if self.down:
            self.neighbors.append(self.down)
        if self.right:
            self.neighbors.append(self.right)


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

def get_random_weights(columns_, rows_):
    return np.random.randint(1, 10, size=(columns_, rows_))

    
def get_static_weights(columns_, rows_):
    np.random.seed(1)
    return np.random.randint(1, 10, size=(columns_, rows_))


def wall_manager(position, set_wall):
    # global grid
    c = position[0] // cell_width
    r = position[1] // cell_height
    grid[c][r].wall = set_wall


def set_title(paused):
    # global window_title
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
    global start_cell, end_cell

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
    start_cell.distance = 0
    to_visit.append(start_cell)


def get_weights():
    global grid
    weights_ = []
    if set_random_weights:
        weights_ = get_random_weights(columns_=columns, rows_=(2*rows))
    else:
        weights_ = get_static_weights(columns_=columns, rows_=(2*rows))

    for c in range(columns):
        for r in range(rows):
            if not grid[c][r].right:
                if grid[c][r].down:
                    grid[c][r].down_weight = weights_[c][(2*r)+1]
                    grid[c][r].down.up_weight = weights_[c][(2*r)+1]
                    
            elif not grid[c][r].down:
                if grid[c][r].right:
                    grid[c][r].right_weight = weights_[c][2*r]
                    grid[c][r].right.left_weight = weights_[c][2*r]

            else:
                grid[c][r].right_weight = weights_[c][2*r]
                grid[c][r].down_weight = weights_[c][(2*r)+1]

                grid[c][r].right.left_weight = weights_[c][2*r]
                grid[c][r].down.up_weight = weights_[c][(2*r)+1]


def add_weight_to_cell(position):
    global add_weight_to, grid

    c = position[0] // cell_width
    r = position[1] // cell_height
    
    if add_weight_to == pygame.K_RIGHT:
        if grid[c][r].right:
            grid[c][r].right_weight += 1
            grid[c][r].right.left_weight += 1

    elif add_weight_to == pygame.K_DOWN:
        if grid[c][r].down:
            grid[c][r].down_weight += 1
            grid[c][r].down.up_weight += 1

    elif add_weight_to == pygame.K_LEFT:
        if grid[c][r].left:
            grid[c][r].left_weight += 1
            grid[c][r].left.right_weight += 1

    elif add_weight_to == pygame.K_UP:
        if grid[c][r].up:
            grid[c][r].up_weight += 1
            grid[c][r].up.down_weight += 1


def get_edge_weight(current_cell, cn):
    if current_cell.right == cn:
        return current_cell.right_weight
    elif current_cell.down == cn:
        return current_cell.down_weight
    elif current_cell.left == cn:
        return current_cell.left_weight
    elif current_cell.up == cn:
        return current_cell.up_weight


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

    running = False
    flag = False
    noFlag = True
    paused = False

    global add_weights, add_weight_to, grid

    set_title(paused)
    create_grid()
    add_neighbors_to_cell()
    if not set_weights_as_zero:
        get_weights()
    define_start_and_end_cell()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if add_weights and event.button == 1:
                    add_weight_to_cell(pygame.mouse.get_pos())
                elif event.button in (1, 3):
                    wall_manager(pygame.mouse.get_pos(), event.button==1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    wall_manager(pygame.mouse.get_pos(), event.buttons[0])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                elif event.key == pygame.K_RETURN:
                    add_weights = False
                    running = True
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    set_title(paused)
                elif not running and event.key in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP):
                    if event.key != add_weight_to:
                        add_weights = True
                        add_weight_to = event.key
                    else:
                        add_weights = False
                        add_weight_to = None

        
        if running and not paused:
            if len(to_visit) > 0:
                current_cell = to_visit.pop(0)

                if current_cell == end_cell:
                    temporary = current_cell
                    path_nodes = 0
                    while temporary.previous:
                        path.append(temporary.previous)
                        path_nodes += 1
                        # print(get_edge_weight(temporary, temporary.previous))
                        temporary = temporary.previous
                        
                    if not flag:
                        # for t in to_visit:
                        #     print(t.distance)
                        flag = True
                        Tk().wm_withdraw()
                        messagebox.showinfo("Solution Found", "Solution was found!\nPath length: " + str(path_nodes) + "\nTotal Path Distance: " + str(end_cell.distance))
                    elif flag:
                        continue
                
                if flag == False:
                    visited.append(current_cell)

                    current_cell.get_neighbors()

                    for cn in current_cell.neighbors:
                        # print('r', cn.right_weight) if cn.right_weight > 0 else None
                        # print('l', cn.left_weight) if cn.left_weight > 0 else None
                        if cn.wall:
                            continue

                        if cn not in visited and cn not in to_visit:
                            cn.previous = current_cell
                            cn.distance = current_cell.distance + get_edge_weight(current_cell, cn)
                            # print('- ',get_edge_weight(current_cell, cn)) if get_edge_weight(current_cell, cn) > 0 else None
                            to_visit.append(cn)
                        
                        elif cn in to_visit:
                            temp_cn_dist = current_cell.distance + get_edge_weight(current_cell, cn)
                            cn_in_visited = to_visit[to_visit.index(cn)]
                            if temp_cn_dist < cn_in_visited.distance:
                                cn.parent = current_cell
                                cn.distance = temp_cn_dist
                                # print(cn.distance)
                                to_visit.remove(cn_in_visited)
                                to_visit.append(cn)
                                # print(' - ', cn.distance) if cn.distance > 0 else None

                    to_visit.sort(key=lambda x: x.distance)
                    # print(to_visit[0].distance) if to_visit[0].distance > 0 else None
                    # for t in to_visit:
                    #     print(t.distance) if t.distance > 0 else None
            
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

                if cell in path:
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


# Code based on:
# https://sites.icmc.usp.br/sandra/G2_t2/Busca.html