from .NsgaII import NsgaII
import numpy as np
from time import time


# Dhiman, Gaurav & Singh, Krishna & Slowik, Adam & Chang, Victor & Yildiz, Ali & Kaur, Amandeep & Garg, Meenakshi. (2021).
# EMoSOA: A New Evolutionary Multi-objective Seagull Optimization Algorithm for Global Optimization.
# International Journal of Machine Learning and Cybernetics. 12. 10.1007/s13042-020-01189-1. 
# Copyright (c) 2022 Miller Cy Chan


# Evolutionary multi-objective seagull optimization algorithm for global optimization (EMoSOA)
class Emosoa(NsgaII):
    def __init__(self, configuration, numberOfCrossoverPoints=2, mutationSize=2, crossoverProbability=80,
                 mutationProbability=3, maxIterations=5000):
        self._max_iterations = maxIterations
        super().__init__(configuration, numberOfCrossoverPoints, mutationSize, crossoverProbability,
                        mutationProbability)
        self._currentGeneration, self._repeatRatio = 0, 0
        self._bestScore, self._gBestScore = [], 0
        self._current_position, self._gBest = [], []


    def exploitation(self):
        positions = self._current_position
        b, Fc = 1, 2 - self._currentGeneration * (2 / self._max_iterations)
        dim = positions.shape
        tau = 2 * np.pi

        r1, r2 = np.random.random(dim), np.random.random(dim)

        A1, C1 = 2 * Fc * r1 - Fc, 2 * r2
        ll = (Fc - 1) * np.random.random(dim) + 1

        D_alphs = Fc * positions + A1 * (self._gBest - positions)
        positions = D_alphs * np.exp(b * ll) * np.cos(ll * tau) + self._gBest


    def replacement(self, population):
        populationSize = len(population)
        climax = .9

        for i in range(populationSize):
            fitness = population[i].fitness
            if fitness < self._bestScore[i]:
                population[i].updatePositions(self._current_position[i])
                fitness = population[i].fitness

            if fitness > self._bestScore[i]:
                self._bestScore[i] = fitness
                population[i].extractPositions(self._current_position[i])

            if fitness > self._gBestScore:
                self._gBestScore = fitness
                population[i].extractPositions(self._current_position[i])
                self._gBest = self._current_position[i][:]

            if self._repeatRatio > climax and self._gBestScore > climax:
                if i > (2 * populationSize * self._gBestScore):
                    population[i].updatePositions(self._current_position[i])

        self.exploitation()
        return super().replacement(population)

    def initialize(self, population):
        prototype = self._prototype
        size = 0
        populationSize = len(population)
        for i in range(populationSize):
            positions = []
            # add new search agent to population
            population[i] = searchAgent = prototype.makeNewFromPrototype(positions)
            if i < 1:
                size = len(positions)
                self._current_position = np.zeros((populationSize, size), dtype=float)

                self._gBest = np.zeros(populationSize, dtype=float)
                self._bestScore = np.zeros(populationSize, dtype=float)

            self._bestScore[i] = searchAgent.fitness
            self._current_position[i] = positions


    # Starts and executes algorithm
    def run(self, maxRepeat=9999, minFitness=0.999):
        mutationSize = self._mutationSize
        mutationProbability = self._mutationProbability
        nonDominatedSorting = self.nonDominatedSorting
        selection = self.selection
        populationSize = self._populationSize
        population = populationSize * [None]

        self.initialize(population)
        np.random.seed(int(time()))

        # Current generation
        currentGeneration = self._currentGeneration

        repeat, lastBestFit = 0, 0.0

        while currentGeneration < self._max_iterations:
            if currentGeneration > 0:
                bestFitness = self.result.fitness
                print("Fitness:", "{:f}\t".format(bestFitness), "Generation:", currentGeneration, end="\r")

                # algorithm has reached criteria?
                if bestFitness > minFitness:
                    break

                difference = abs(bestFitness - lastBestFit)
                if difference <= 0.0000001:
                    repeat += 1
                else:
                    repeat = 0

                self._repeatRatio = repeat * 100 / maxRepeat
                if repeat > (maxRepeat / 100):
                    self.reform()

            # crossover
            offspring = self.replacement(population)

            # mutation
            for child in offspring:
                child.mutation(mutationSize, mutationProbability)

            totalChromosome = population + offspring

            # non-dominated sorting
            front = nonDominatedSorting(totalChromosome)
            if len(front) == 0:
                break

            # selection
            population = selection(front, totalChromosome)
            self._populationSize = populationSize = len(population)

            # comparison
            if currentGeneration == 0:
                self._chromosomes = population
            else:
                totalChromosome = population + self._chromosomes
                newBestFront = nonDominatedSorting(totalChromosome)
                if len(newBestFront) == 0:
                    break
                self._chromosomes = selection(newBestFront, totalChromosome)
                lastBestFit = bestFitness

            currentGeneration += 1
            self._currentGeneration = currentGeneration

    def __str__(self):
        return "Evolutionary multi-objective seagull optimization algorithm for global optimization (EMoSOA)"