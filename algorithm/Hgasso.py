from .NsgaII import NsgaII
from random import randrange
import math
import random


# Shehadeh, Hisham & Mustafa, Hossam & Tubishat, Mohammad. (2022).
# A Hybrid Genetic Algorithm and Sperm Swarm Optimization (HGASSO) for Multimodal Functions.
# International Journal of Applied Metaheuristic Computing. 13. 10.4018/IJAMC.292507.
# Copyright (c) 2022 Miller Cy Chan


# Hybrid Genetic Algorithm and Sperm Swarm Optimization (HGASSO)
class Hgasso(NsgaII):
    # Initializes Hybrid Genetic Algorithm and Sperm Swarm Optimization
    def __init__(self, configuration, numberOfCrossoverPoints=2, mutationSize=2, crossoverProbability=80,
                 mutationProbability=3):
        NsgaII.__init__(self, configuration, numberOfCrossoverPoints, mutationSize, crossoverProbability, mutationProbability)
        self._threshold = .5
        self._sBestScore, self._sgBestScore = 0, 0
        self._sBest, self._sgBest = [], []
        self._current_position, self._velocity = [], []


    def replacement(self, population):
        populationSize = len(population)
        start = int(populationSize * self._threshold)
        current_position = self._current_position
        sBest, sgBest = self._sBest, self._sgBest
        sBestScore, sgBestScore = self._sBestScore, self._sgBestScore

        for i in range(populationSize):
            fitness = population[i].fitness
            if i < start:
                population[i].extractPositions(current_position[i])
            elif fitness < sBestScore[i]:
                population[i].updatePositions(current_position[i])
                fitness = population[i].fitness

            if fitness > sBestScore[i]:
                sBestScore[i] = fitness
                sBest[i] = current_position[i]

            if fitness > sgBestScore:
                sgBestScore = fitness
                sgBest = current_position[i]

        self.updateVelocities(population)
        return super().replacement(population)


    def initialize(self, population):
        prototype = self._prototype
        size = 0
        current_position, velocity = self._current_position, self._velocity
        populationSize = len(population)
        for i in range(populationSize):
            positions = []
            # add new chromosome to population
            population[i] = prototype.makeNewFromPrototype(positions)
            if i < 1:
                size = len(positions)
                self._current_position = [[0] * size for _ in range(populationSize)]
                self._velocity = [[0] * size for _ in range(populationSize)]
                current_position, velocity = self._current_position, self._velocity

                self._sBest = [[0] * size for _ in range(populationSize)]
                self._sgBest = populationSize * [0]
                self._sBestScore = populationSize * [0]

            self._sBestScore[i] = population[i].fitness
            for j in range(size):
                current_position[i][j] = positions[j]
                velocity[i][j] = float(random.uniform(-.6464, .7157) / 3.0)


    def updateVelocities(self, population):
        sBest, sgBest = self._sBest, self._sgBest
        current_position, velocity = self._current_position, self._velocity
        populationSize = len(population)
        for i in range(populationSize):
            dim = len(velocity[i])
            for j in range(dim):
                velocity[i][j] = float(random.random() * math.log10(random.uniform(7.0, 14.0)) * velocity[i][j] + \
                math.log10(random.uniform(7.0, 14.0)) * math.log10(random.uniform(35.5, 38.5)) * (sBest[i][j] - current_position[i][j]) + \
                math.log10(random.uniform(7.0, 14.0)) * math.log10(random.uniform(35.5, 38.5)) * (sgBest[j] - current_position[i][j]))

                current_position[i][j] += velocity[i][j]

    def __str__(self):
        return "Hybrid Genetic Algorithm and Sperm Swarm Optimization (HGASSO)"
             