import copy
import random
import numpy
from functools import partial

import pygame
pygame.init()
scale=10
window = pygame.display.set_mode((800, 600))

def renderFunction(ant):
    window.fill((255, 255, 255))
    for i in range(len(ant.matrix_exc)):
        for j in range(len(ant.matrix_exc[ant.row])):
            if ant.matrix_exc[i][j] == "food":
                pygame.draw.circle(window,(34,34,23),(i*scale,j*scale),5)
    pygame.draw.circle(window,(244,34,23),(ant.row*scale,ant.col*scale),10)
    pygame.draw.circle(window,(244,34,23),(ant.row*scale,ant.col*scale),ant.eaten,2)
    pygame.time.wait(100)
    pygame.display.update()

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

def progn(*args):
    for arg in args:
        arg()

def prog2(out1, out2): 
    return partial(progn,out1,out2)

def prog3(out1, out2, out3):     
    return partial(progn,out1,out2,out3)

def if_then_else(condition, out1, out2):
    out1() if condition() else out2()

class AntSimulator(object):
    direction = ["north","east","south","west"]
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]


    def __init__(self, max_moves):
        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.routine = None

    def _reset(self):
        self.row = self.row_start 
        self.col = self.col_start 
        self.dir = 1
        self.moves = 0  
        self.eaten = 0
        self.matrix_exc = copy.deepcopy(self.matrix)

    @property
    def position(self):
        return (self.row, self.col, self.direction[self.dir])

    def turn_left(self): 
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir - 1) % 4

    def turn_right(self):
        if self.moves < self.max_moves:
            self.moves += 1    
            self.dir = (self.dir + 1) % 4

    def move_forward(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
            self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
            if self.matrix_exc[self.row][self.col] == "food":
                self.eaten += 1
            self.matrix_exc[self.row][self.col] = "passed"

    def sense_food(self):
        ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col        
        return self.matrix_exc[ahead_row][ahead_col] == "food"

    def if_food_ahead(self, out1, out2):
        return partial(if_then_else, self.sense_food, out1, out2)

    def run(self,routine,individual):
        self._reset()
        global gen
        global start_gen
        if gen >= start_gen:
            print(individual)

        while self.moves < self.max_moves:
            routine()
            if gen >= start_gen:
                renderFunction(self)
        
        

    def parse_matrix(self, matrix):
        self.matrix = list()
        for i, line in enumerate(matrix):
            self.matrix.append(list())
            for j, col in enumerate(line):
                if col == "#":
                    self.matrix[-1].append("food")
                elif col == ".":
                    self.matrix[-1].append("empty")
                elif col == "S":
                    self.matrix[-1].append("empty")
                    self.row_start = self.row = i
                    self.col_start = self.col = j
                    self.dir = 1
        self.matrix_row = len(self.matrix)
        self.matrix_col = len(self.matrix[0])
        self.matrix_exc = copy.deepcopy(self.matrix)


# class AntSimulator2(object):
#     direction = ["north","east","south","west"]
#     dir_row = [1, 0, -1, 0]
#     dir_col = [0, 1, 0, -1]


#     def __init__(self, max_moves):
#         self.max_moves = max_moves
#         self.moves = 0
#         self.eaten = 0
#         self.routine = None

#     def _reset(self):
#         self.row = self.row_start 
#         self.col = self.col_start 
#         self.dir = 1
#         self.moves = 0  
#         self.eaten = 0
#         self.matrix_exc = copy.deepcopy(self.matrix)

#     @property
#     def position(self):
#         return (self.row, self.col, self.direction[self.dir])

#     def turn_left(self): 
#         if self.moves < self.max_moves:
#             self.moves += 1
#             self.dir = (self.dir - 1) % 4

#     def turn_right(self):
#         if self.moves < self.max_moves:
#             self.moves += 1    
#             self.dir = (self.dir + 1) % 4

#     def move_forward(self):
#         if self.moves < self.max_moves:
#             self.moves += 1
#             self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
#             self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
#             if self.matrix_exc[self.row][self.col] == "food":
#                 self.eaten += 1
#             self.matrix_exc[self.row][self.col] = "passed"

#     def sense_food(self):
#         ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
#         ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col        
#         return self.matrix_exc[ahead_row][ahead_col] == "food"

#     def if_food_ahead(self, out1, out2):
#         return partial(if_then_else, self.sense_food, out1, out2)

#     def run(self,routine,individual):
#         self._reset()
#         global gen

#         while self.moves < self.max_moves:
#             routine()
#             if gen > 50:
#                 print(individual)
#                 renderFunction(self)
        
# def parse_matrix(self, matrix):
#     self.matrix = list()
#     for i, line in enumerate(matrix):
#         self.matrix.append(list())
#         for j, col in enumerate(line):
#             if col == "#":
#                 self.matrix[-1].append("food")
#             elif col == ".":
#                 self.matrix[-1].append("empty")
#             elif col == "S":
#                 self.matrix[-1].append("empty")
#                 self.row_start = self.row = i
#                 self.col_start = self.col = j
#                 self.dir = 1
#     self.matrix_row = len(self.matrix)
#     self.matrix_col = len(self.matrix[0])
#     self.matrix_exc = copy.deepcopy(self.matrix)

ant = AntSimulator(600)

pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(ant.if_food_ahead, 2)
pset.addPrimitive(prog2, 2)
pset.addPrimitive(prog3, 3)
pset.addTerminal(ant.move_forward)
pset.addTerminal(ant.turn_left)
pset.addTerminal(ant.turn_right)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=10)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

funcCalled=0
gen=0
start_gen=20
def evalArtificialAnt(individual):
    global funcCalled
    global gen
    # Transform the tree expression to functional Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    ant.run(routine,individual)
    if funcCalled==299:
        funcCalled=0
        gen+=1
        print("gen incremented:",gen)
    funcCalled+=1
            # print(self.moves)
       
    return ant.eaten,

toolbox.register("evaluate", evalArtificialAnt)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    random.seed(69)

    with  open("ant/santafe_trail.txt") as trail_file:
      ant.parse_matrix(trail_file)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 200, stats, halloffame=hof)

    return pop, hof, stats

if __name__ == "__main__":
    main()