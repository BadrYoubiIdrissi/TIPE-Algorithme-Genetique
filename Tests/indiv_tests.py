import cProfile
from Source.Individual import Individual

ind = Individual()
ind.setTarget(lambda x: 1)
ind.genRand(0, "full")
def test():
    print(ind.fitness)
    ind.showGraph()
cProfile.run("test()")

# print(ind)
#


