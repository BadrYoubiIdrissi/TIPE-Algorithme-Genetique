import cProfile
from Source.Individual import Individual
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
def test():
    ind = Individual()
    ind2 = Individual()
    ind.setTarget(lambda x: x**2)
    ind2.setTarget(lambda x: x**2)
    ind.poly = Polynomial([0,1,0,1])
    ind2.poly = Polynomial([0,1])
    ind.plotGraph()
    ind2.plotGraph()
    ind.updateFitness()
    ind2.updateFitness()
    print(ind.fitness)
    print(ind2.fitness)
    plt.show()
cProfile.run("test()")
