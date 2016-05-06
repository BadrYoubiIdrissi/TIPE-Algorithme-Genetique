from Source.Node import Node
from Source.Tree import Tree
import random as rand
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
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


def showTree(tree):
    """Fonction qui affiche l'arbre
        Exemple (+)
                / \
               1   2  correspond à ( + 1 , 2 )"""

    def rshow(tree):
        if tree.isLeaf():
            # assert type(tree.node) != __main__.Node, "Shoudln't be a node"
            print(' ', tree.node, end=' ')  # Si c'est une feuille ou si c'est une chaine de caractère spécial
        else:
            print(' ( ', end='')
            print(tree.node.symbol, end='')
            for i in range(len(tree.branches)):
                rshow(tree.branches[i])
            print(' ) ', end='')

    rshow(tree)
    # print("Method : ",self.tree.method)
    print()

def test():
    tr = Tree()
    tr.genRand(2, [Polynomial([1]),Polynomial([0,1])], [add,mult,sub])
    # l = []
    # X = [i for i in range(5000)]
    # Y = []
    # f = [0 for i in range(11)]
    # for i in range(10000):
    #     l.append(tr.randomSubTree(0.1))
    # for j in range(11):
    #     for i in range(10000):
    #         if l[i].getDepth() == j:
    #             Y.append(l[i].depth)
    #             f[j] += 1
    # fracs = [f[i]/100 for i in range(11)]
    # print(fracs)
    # plt.pie(fracs)
    # plt.show()
    showTree(tr)
    tr2 = Tree()
    tr2.genRand(1, [Polynomial([1]), Polynomial([0, 1])], [add, mult, sub])
    showTree(tr2)
    tr.randomInsert(tr2)
    showTree(tr)
test()