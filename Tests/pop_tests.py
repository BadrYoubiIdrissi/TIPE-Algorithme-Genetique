from Source.Population import Population
import matplotlib.pyplot as plt
import cProfile


def test():
    pop = Population(1000)
    pop.setTarget(lambda x: x ** 2)
    pop.genRand(2,5)
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

