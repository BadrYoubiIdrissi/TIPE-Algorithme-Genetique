import cProfile
from Source.Individual import Individual

def test():
    ind = Individual()
    ind.setTarget(lambda x: 1)
    ind.genRand(5, "full")
    ind.showTree()
    ind.tree.randomNode(2)
cProfile.run("test()")
