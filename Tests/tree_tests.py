from Source.Node import Node
from Source.Tree import Tree
import random as rand
import numpy as np
from numpy.polynomial import Polynomial
import cProfile

add = Node((lambda args: args[0] + args[1]), 2, '+')
sub = Node((lambda args: args[0] - args[1]), 2, '-')
mult = Node((lambda args: args[0] * args[1]), 2, '*')

"""

def randomMonome():
    a = -10 + 20*rand.random()
    b = rand.randint(0, 10)
    l = [0 for i in range(b)]
    l.append(a)
    return Polynomial(l)

def re(tree,x):
    if tree.isLeaf:
        return tree.node(x)
    else:
        if tree.node.symbol == '+':
            return re(tree.branches[0],x) + re(tree.branches[1],x)
        elif tree.node.symbol == '*':
            return re(tree.branches[0],x) * re(tree.branches[1],x)
        elif tree.node.symbol == '-':
            return re(tree.branches[0],x) - re(tree.branches[1],x)
"""
def test():
    l = [0 for i in range(10)]
    for j in range(10):
        for i in range(100):
            tree = Tree(5)
            tree.genRand([Polynomial([1]),Polynomial([0,1])], [add,mult,sub], method="grow")
            tree.updateTreeDepth()
            l[tree.depth] += 1
        l[j] /= 1000
    print(l)

cProfile.run('test()')