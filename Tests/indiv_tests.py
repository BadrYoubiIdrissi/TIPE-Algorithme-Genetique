import cProfile
from Source.Individual import Individual

def test():
    for i in range(400):
        ind = Individual()
        ind.setTarget(lambda x: 1)
        ind.genRand(5, "full")
cProfile.run("test()")

# print(ind)
#


