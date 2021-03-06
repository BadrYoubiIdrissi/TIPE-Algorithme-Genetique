from Source.Tree import Tree
from Source.Individual import Individual
from Source.DefaultSet import DefaultSet
import copy
import random as rand


class Population:
    def __init__(self, size, termSet = DefaultSet().termSet, funcSet = DefaultSet().funcSet ):
        self.size = size
        self.currentGeneration = []
        self.generationCount = 0
        self.termSet = termSet
        self.funcSet = funcSet
        self.target = None
    def __repr__(self):
        s = ""
        for e in self.currentGeneration:
            s+="Ind : "+e.__repr__()
            s+=" Fitness : "+str(e.fitness)
            s+='\n'
        return s

    def setTarget(self, target):
        self.target = target

    def genRand(self, minIndvSize, maxIndvSize):
        self.generationCount = 0
        self.currentGeneration = []
        for i in range(self.size):
            if i % 2 == 0:
                method = "full"
            else:
                method = "grow"
            depth = minIndvSize + (i // 2) % (maxIndvSize + 1 - minIndvSize)  # Des profendeur cycliques selon l'indice de l'individu
            randomInd = Individual(self.termSet, self.funcSet)
            randomInd.setTarget(self.target)
            randomInd.genRand(depth, method)
            self.currentGeneration.append(randomInd)

    def mergeSort(self, alist):
        """Algorithme de tri fusion : pris du site http://interactivepython.org/runestone/static/pythonds/SortSearch/TheMergeSort.html
        Avec quelque modifications pour que ca marche"""
        if len(alist) > 1:
            mid = len(alist) // 2
            lefthalf = alist[:mid]
            righthalf = alist[mid:]

            self.mergeSort(lefthalf)
            self.mergeSort(righthalf)

            i = 0
            j = 0
            k = 0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i].fitness > righthalf[j].fitness:
                    alist[k] = lefthalf[i]
                    i = i + 1
                else:
                    alist[k] = righthalf[j]
                    j = j + 1
                k = k + 1

            while i < len(lefthalf):
                alist[k] = lefthalf[i]
                i = i + 1
                k = k + 1

            while j < len(righthalf):
                alist[k] = righthalf[j]
                j = j + 1
                k = k + 1

    def sortCurrentGeneration(self):
        self.mergeSort(self.currentGeneration)

    def bestIndividual(self, list):
        max = list[0]
        for i in list:
            if i.fitness > max.fitness:
                max = i
        return max

    def worstIndividual(self, list):
        max = list[0]
        for i in list:
            if i.fitness < max.fitness:
                max = i
        return max

    def bestCurrentFitness(self):
        return self.bestIndividual(self.currentGeneration).fitness

    def worstCurrentFitness(self):
        return self.worstIndividual(self.currentGeneration).fitness

    def relFitness(self, ind):
        return ind.fitness / self.totalFitness()

    def totalFitness(self):
        fsum = 0
        for i in self.currentGeneration:
            fsum += i.fitness
        return fsum

    def fitnessProp(self):
        self.sortCurrentGeneration()
        ran = rand.random()
        f = 0
        i = 0
        while ran > f:
            f += self.relFitness(self.currentGeneration[i])
            i += 1
        return self.currentGeneration[i - 1]

    def tournamentSelection(self, nbCandidates=None, probBest=0.8):
        candidates = []
        if nbCandidates == None:
            nbCandidates = rand.randint(1, self.size)
        for i in range(nbCandidates):
            randInt = rand.randint(0, self.size - 1)
            candidates.append(self.currentGeneration[randInt])
        return self.bestIndividual(candidates)
        # self.mergeSort(candidates)
        # randf = rand.random()
        # n = len(candidates)
        # s=0
        # for i in range(n):
        #     s += probBest * ((1 - probBest) ** (n - i - 1))
        #     print(s)
        #     if randf < s:
        #         return candidates[n - i - 1]
        # return candidates[0]

    def crossOver(self, ind1, ind2):
        child = Individual(self.termSet,self.funcSet)
        childTree = ind2.tree.copy()
        childTree.randomInsert(ind1.tree.randomSubTree())
        child.tree = childTree
        child.setTarget(self.target)
        child.toPoly()
        child.updateFitness()
        return child

    def mutation(self):
        random_indiv = self.currentGeneration[rand.randint(0, self.size - 1)]
        mutation_indiv = Individual(self.termSet, self.funcSet)
        mutation_indiv.setTarget(self.target)
        mutation_indiv.genRand(random_indiv.tree.depth)
        random_indiv = self.crossOver(random_indiv, mutation_indiv)
        return random_indiv

    def evolve(self):
        newGeneration = []
        for i in range(self.size):
            if rand.random() < 1e-1:
                newGeneration.append(self.mutation())
            else:
                parent1 = self.tournamentSelection()
                parent2 = self.tournamentSelection()
                while parent2 == parent1:
                    parent2 = self.tournamentSelection()
                newGeneration.append(self.crossOver(parent1, parent2))
        self.generationCount += 1
        self.currentGeneration = newGeneration
