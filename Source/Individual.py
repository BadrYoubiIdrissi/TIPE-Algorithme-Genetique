from Source.Tree import Tree
from Source.Node import Node
from numpy import linspace
from matplotlib.pyplot import plot,show
from numpy.polynomial import Polynomial
from scipy.integrate import simps

class Individual:
    """Implementation d'un individu exemple: ici un polynome"""

    def __init__(self, termSet = [], funcSet = []):
        if termSet == [] or funcSet == []: #On initialise l'esmble des feuilles et des fonctions ç des valeurs par défaut
            add = Node((lambda args: args[0] + args[1]), 2, '+')
            sub = Node((lambda args: args[0] - args[1]), 2, '-')
            mult = Node((lambda args: args[0] * args[1]), 2, '*')
            self.termSet = [Polynomial([1]),Polynomial([0,1])]
            self.funcSet = [add, sub, mult]
        else:
            self.termSet = termSet
            self.funcSet = funcSet
        self.poly = None #L'attribut poly va contenir le polynome correspondant à l'arbre
        self.target = None

    def __repr__(self):
        # s = ""
        # n = self.poly.degree()
        # for i in range(n):
        #     s+= " "+str(self.poly.coef[n-i])+"X**"+str(n-i)+" +"
        # s+= " "+str(self.poly.coef[n])
        return self.poly.__str__()

    def genRand(self, depth, method="full"):
        tree = Tree(depth)
        tree.genRand(self.termSet, self.funcSet, method)
        self.tree = tree
        self.toPoly()
        self.updateFitness()

    # def evaluate(self, x):
    #     """Fonction renvoyant la valeur du polynome en x
    #         Idéé : on parcours récursivement l'arbre jusqu'a tomber sur des feuilles qui sont soit des constantes ou 'x' l'inconnu
    #         qu'on remplace par la valeur voulu"""
    #
    #     def rexecute(tree):
    #         if tree.isLeaf:
    #             if tree.node == 'x':
    #                 return x
    #             else:
    #                 return tree.node
    #         else:
    #             args = []
    #             for i in range(tree.node.arity):
    #                 args.append(rexecute(tree.branches[i]))
    #             return tree.node.run(args)
    #
    #     return rexecute(self.tree)

    def toPoly(self):
        def rp(tree):
            if tree.isLeaf:
                return tree.node
            else:
                if tree.node.symbol == '+':
                    return rp(tree.branches[0]) + rp(tree.branches[1])
                elif tree.node.symbol == '*':
                    return rp(tree.branches[0]) * rp(tree.branches[1])
                elif tree.node.symbol == '-':
                    return rp(tree.branches[0]) - rp(tree.branches[1])
        self.poly = rp(self.tree)

    def evaluate(self, x):
        assert self.poly != None , "Pas un polynome"
        return self.poly(x)

    def setTarget(self,target):
        self.target = target

    def showGraph(self):
        """Fonction tracant la courbe du polynome"""
        X = linspace(-1, 1, 100)
        Y = [self.evaluate(x) for x in X]
        plot(X, Y, label="Poly")
        show()

    def showTree(self, showDepths=False):
        """Fonction qui affiche l'arbre 
            Exemple (+)
                    / \
                   1   2  correspond à ( + 1 , 2 )"""
        def rshow(tree):
            if tree.isLeaf:
                # assert type(tree.node) != __main__.Node, "Shoudln't be a node"
                print(' ', tree.node, end=' ')  # Si c'est une feuille ou si c'est une chaine de caractère spécial
            else:
                print(' ( ', end='')
                print(tree.node.symbol, end='')
                for i in range(len(tree.branches)):
                    rshow(tree.branches[i])
                print(' ) ', end='')
        rshow(self.tree)
        # print("Method : ",self.tree.method)
        print()

        # def interpretTerms(self):
        #     """Interpreteur de feuilles
        #         @ rand a b : entier aleatoire entre a et b"""
        #
        #     def rinterpretTerm(tree):
        #         if tree.isLeaf:
        #             if type(tree.node) == str and tree.node[0] == '@':
        #                 command = tree.node.split(' ')
        #                 if command[1] == 'rand':
        #                     if command[2] == 'int':
        #                         a = int(command[3])
        #                         b = int(command[4])
        #                         tree.node = rand.randint(a, b)
        #                     else:
        #                         a = float(command[3])
        #                         b = float(command[4])
        #                         tree.node = a + (b - a) * rand.random()
        #         else:
        #             for i in range(tree.node.arity):
        #                 rinterpretTerm(tree.branches[i])
        #
        #     rinterpretTerm(self.tree)

    def updateFitness(self):
        X = linspace(-1, 1, 50)
        assert self.target != None, "target still not set"
        Y = [abs(self.evaluate(x) - self.target(x)) for x in X]
        self.fitness = -simps(Y, X)
