import random as rand

class Tree:
    """Implementation basique d'un arbre
        depth = the depth of the deepest leaf"""

    def __init__(self,node = None, branches = None):
        self.node = node
        if branches != None:
            self.branches = branches
        else:
            self.branches = []
        self.depth = self.getDepth()

    def getDepth(self):
        if self.branches == []:
            if self.node == None:
                return -1
            else:
                return 0
        else:
            self.updateDepth()
            return self.depth
    def getMinDepth(self):
        def rgetmd(tree):
            if tree.isLeaf():
                return 0
            else:
                depths = []
                for i in range(tree.node.arity):
                    depths.append(1 + rgetmd(tree.branches[i]))
                return min(depths)
        return rgetmd(self)
    def isLeaf(self):
        return self.branches == []

    def updateDepth(self):
        """Met à jour la profondeur d'un arbre (et de ses sous arbre) selon la feuille la plus profonde (utile pour la methode grow)"""
        def rupdateDepth(tree):
            if tree.isLeaf():
                tree.depth = 0
                return 0
            else:
                depths = []
                for i in range(tree.node.arity):
                    depths.append(1 + rupdateDepth(tree.branches[i]))
                tree.depth = max(depths)
                return tree.depth
        rupdateDepth(self)

    def genRand(self, depth, termSet, funcSet, method="full"):
        """ Genere un arbre aléatoire soit avec la methode full ou grow
            termSet = Ensembles des feuilles (de longeur long_s)
            funcSet = Ensemble  des fonctions (de longeur long_f)"""
        self.method = method
        self.depth = depth
        def rgenRand(tree):
            """Fonction recursive auxiliere qui d'un arbre à une profendeur fixé n génere une liste de sous
            arbres de profendeur n-1 en choisisant le noeud aleatoirement de l'ensemble des fonctions"""
            if tree.depth == 0 or (method == "grow" and rand.random() < len(termSet) / (len(funcSet) + len(termSet))):
                # Si on est arrivé à la profendeur maximale on met une feuille
                # Ou si la methode est Grow, on a une probabilité de long_s/(long_s+long_f) de choisir une feuille
                tree.node = termSet[rand.randint(0, len(termSet) - 1)]
            else:
                # Sinon on choisi une fonction aléatoire qu'on met dans le noeud
                tree.node = funcSet[rand.randint(0, len(funcSet) - 1)]
                for i in range(tree.node.arity):
                    # Le nombre de branches est le nombre de prametres
                    subTree = Tree()
                    subTree.depth = tree.depth - 1
                    # Les branches seront des sous arbres aleatoires de profendeur n-1
                    rgenRand(subTree)
                    tree.branches.append(subTree)
        rgenRand(self)  # On lance la fonction recursive
        if method == "grow":
            self.updateDepth()

    def randomLeaf(self):
        """Fonction recursive auxiliaire qui parcours un arbre aleatoirement pour arriver à la profendeur voulu"""
        if self.isLeaf():
            # Si on est arrivé à la profendeur choisi ou si l'arbre est une feuille on renvoie l'arbre
            return self
        else:
            # Sinon on choisit aleatoirement une branche qu'on renvoie à recrandomNode
            randomBranch = self.branches[rand.randint(0, self.node.arity - 1)]
            return randomBranch.randomLeaf()

    def randomNode(self, depth):
        if depth == 0 or self.isLeaf():
            return self
        else:
            randomBranch = self.branches[rand.randint(0, self.node.arity - 1)]
            return randomBranch.randomNode(depth - 1)

    def randomNonLeafNode(self, depth):
        if self.getMinDepth() == 1 or depth == 1:
            return self
        else:
            randomBranch = self.branches[rand.randint(0, self.node.arity - 1)]
            return randomBranch.randomNonLeafNode(depth - 1)

    def randomSubTree(self, probLeaf=1e-1):  # To do : probabilités de selection 10% feuilles 90% noeuds
        """Fonction qui retourne un sous arbre aléatoire"""
        if self.isLeaf():
            return self
        elif rand.random() < probLeaf:
            return self.randomLeaf()
        else:
            rand_depth = rand.randint(0, self.depth - 1)  # On choisit la profondeur à laquelle on veut arriver aleatoirement
            return self.randomNode(rand_depth)

    def randomInsert(self, subTree):
        if self.isLeaf():
            self.copyFrom(subTree)
        else:
            troncature = self.randomNonLeafNode(self.depth)
            randBranche = rand.randint(0,troncature.node.arity-1)
            troncature.branches[randBranche] = subTree.copy()
    def copyFrom(self,subTree):
        subc = subTree.copy()
        self.node = subc.node
        self.branches = subc.branches
        self.depth = subc.depth
    def copy(self):
        def rc(tree):
            if tree.isLeaf():
                ntree = Tree(tree.node)
            else:
                nbranches = []
                for i in range(tree.node.arity):
                    nbranches.append(rc(tree.branches[i]))
                ntree = Tree(tree.node, nbranches)
            return ntree
        return rc(self)