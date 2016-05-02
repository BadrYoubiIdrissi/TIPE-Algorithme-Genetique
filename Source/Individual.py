from Source.Tree import Tree
import copy
import random as rand
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import scipy.integrate as integrate

class Individual:
    """Implementation d'un individu exemple: ici un polynome"""

    def __init__(self, parrentPopulation=None):
        self.parrentPopulation = parrentPopulation
        self.polynome = None

    def genRand(self, depth, method="full"):
        tree = Tree(depth)
        tree.genRand(self.parrentPopulation.termSet, self.parrentPopulation.funcSet, method)
        self.tree = tree
        self.interpretTerms()
        self.updateFitness()

    def evaluate(self, x):
        """Fonction renvoyant la valeur du polynome en x
            Idéé : on parcours récursivement l'arbre jusqu'a tomber sur des feuilles qui sont soit des constantes ou 'x' l'inconnu 
            qu'on remplace par la valeur voulu"""

        def rexecute(tree):
            if tree.isLeaf:
                if tree.node == 'x':
                    return x
                else:
                    return tree.node
            else:
                args = []
                for i in range(tree.node.arity):
                    args.append(rexecute(tree.branches[i]))
                return tree.node.run(args)

        return rexecute(self.tree)

    def poly_from_tree(self):
        def rpoly(tree):
            if tree.isLeaf:
                if tree.node == 'x':
                    return Polynomial([0, 1])
                else:
                    return Polynomial([tree.node])
            else:
                if tree.node.symbol == '+':
                    return rpoly(tree.branches[0]) + rpoly(tree.branches[1])
                elif tree.node.symbol == '*':
                    return rpoly(tree.branches[0]) * rpoly(tree.branches[1])
                elif tree.node.symbol == '-':
                    return rpoly(tree.branches[0]) - rpoly(tree.branches[1])

        return rpoly(self.tree)

    def showGraph(self):
        """Fonction tracant la courbe du polynome"""
        X = np.linspace(-1, 1, 100)
        Y = [self.evaluate(x) for x in X]
        plt.plot(X, Y, label="Poly")

    def showTree(self, showDepths=False):
        """Fonction qui affiche l'arbre 
            Exemple (+)
                    / \
                   1   2  correspond à ( + 1 , 2 )"""

        if i != len(tree.branches) - 1:
            print(',', end="")
        print(' ) ', end='')

        def rshow(tree):
            if tree.isLeaf or (type(tree.node) == str and tree.node[0] == '@'):
                # assert type(tree.node) != __main__.Node, "Shoudln't be a node"
                print(' ', tree.node, end=' ')  # Si c'est une feuille ou si c'est une chaine de caractère spécial
            else:
                if showDepths:
                    print(' (d' + str(tree.depth), end=' ')
                else:
                    print(' ( ', end='')
                print(tree.node.symbol, end='')
                for i in range(len(tree.branches)):
                    rshow(tree.branches[i])

        rshow(self.tree)
        # print("Method : ",self.tree.method)
        print()

    def interpretTerms(self):
        """Interpreteur de feuilles
            @ rand a b : entier aleatoire entre a et b"""

        def rinterpretTerm(tree):
            if tree.isLeaf:
                if type(tree.node) == str and tree.node[0] == '@':
                    command = tree.node.split(' ')
                    if command[1] == 'rand':
                        if command[2] == 'int':
                            a = int(command[3])
                            b = int(command[4])
                            tree.node = rand.randint(a, b)
                        else:
                            a = float(command[3])
                            b = float(command[4])
                            tree.node = a + (b - a) * rand.random()
            else:
                for i in range(tree.node.arity):
                    rinterpretTerm(tree.branches[i])

        rinterpretTerm(self.tree)

    def updateFitness(self):
        X = np.linspace(-1, 1, 20)
        Y = [abs(self.evaluate(x) - self.parrentPopulation.target(x)) for x in X]
        self.fitness = -integrate.simps(Y, X)
