from Source.Population import Population
import matplotlib.pyplot as plt
import cProfile
from numpy import cos

pop = Population(500)
pop.setTarget(lambda x: x**3 + x + 1)
pop.genRand(2,5)

def test():
    c=0
    while pop.bestCurrentFitness() < -1e-2 and c < 5:
        pop.evolve()
        c+=1
    print(c)
    print(pop.bestIndividual(pop.currentGeneration))
    print(pop.bestCurrentFitness())

    #Distribution des profendeurs d'arbres :
    """
    X = [i for i in range(1, 1001)]
    Y = []
    for i in range(0,15):
        for j in range(1000):
            if pop.currentGeneration[j].tree.depth == i: #Remplacer .tree.depth par .poly.degree() pour la distrbution de degrées
                Y.append(i)
    plt.plot(X, Y)
    plt.show()
    """

cProfile.run("test()")

