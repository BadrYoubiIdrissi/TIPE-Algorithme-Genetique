import random as rand

class Tree:
    """Implementation basique d'un arbre
        depth = the depth of the deepest leaf"""

    def __init__(self, depth):
        self.depth = depth
        self.isLeaf = depth == 0

    def updateTreeDepth(self):
        """Met à jour la profondeur d'un arbre (et de ses sous arbre) selon la feuille la plus profonde (utile pour la methode grow)"""

        def rupdateTreeDepth(tree):
            if tree.isLeaf:
                tree.depth = 0
                return 0
            else:
                depths = []
                for i in range(tree.node.arity):
                    depths.append(1 + rupdateTreeDepth(tree.branches[i]))
                tree.depth = max(depths)
                return tree.depth
        rupdateTreeDepth(self)

    def genRand(self, termSet, funcSet, method="full"):
        """ Genere un arbre aléatoire soit avec la methode full ou grow
            termSet = Ensembles des feuilles (de longeur long_s)
            funcSet = Ensemble  des fonctions (de longeur long_f)"""
        self.method = method

        def rgenRand(tree):
            """Fonction recursive auxiliere qui d'un arbre à une profendeur fixé n génere une liste de sous
            arbres de profendeur n-1 en choisisant le noeud aleatoirement de l'ensemble des fonctions"""
            if tree.depth == 0 or (method == "grow" and rand.random() < len(termSet) / (len(funcSet) + len(termSet))):
                # Si on est arrivé à la profendeur maximale on met une feuille
                # Ou si la methode est Grow, on a une probabilité de long_s/(long_s+long_f) de choisir une feuille
                tree.node = termSet[rand.randint(0, len(termSet) - 1)]
                tree.isLeaf = True  # Cet arbre est donc forcement une feuille
            else:
                # Sinon on choisi une fonction aléatoire qu'on met dans le noeud
                tree.node = funcSet[rand.randint(0, len(funcSet) - 1)]
                # On initialise les branches à []
                tree.branches = []
                for i in range(tree.node.arity):
                    # Le nombre de branches est le nombre de prametres
                    subTree = Tree(tree.depth - 1)
                    # Les branches seront des sous arbres aleatoires de profendeur n-1
                    rgenRand(subTree)
                    tree.branches.append(subTree)

        rgenRand(self)  # On lance la fonction recursive
        #self.updateTreeDepth()

    def randomLeaf(self):
        """Fonction recursive auxiliaire qui parcours un arbre aleatoirement pour arriver à la profendeur voulu"""
        if self.isLeaf:
            # Si on est arrivé à la profendeur choisi ou si l'arbre est une feuille on renvoie l'arbre
            return self
        else:
            # Sinon on choisit aleatoirement une branche qu'on renvoie à recrandomNode
            randomBranch = self.branches[rand.randint(0, self.node.arity - 1)]
            return randomBranch.randomLeaf()

    def randomNode(self, depth):
        if depth == 0 or self.isLeaf:
            return self
        else:
            randomBranch = self.branches[rand.randint(0, self.node.arity - 1)]
            return randomBranch.randomNode(depth - 1)

    def randomSubTree(self, probLeaf=9e-2):  # To do : probabilités de selection 10% feuilles 90% noeuds
        """Fonction qui retourne un sous arbre aléatoire"""
        if self.isLeaf:
            return self
        elif rand.random() < probLeaf:
            return self.randomLeaf()
        else:
            rand_depth = rand.randint(0, self.depth - 1)  # On choisit la profondeur à laquelle on veut arriver aleatoirement
            return self.randomNode(rand_depth)

    def randomInsert(self, subTree):
        troncature = self.randomSubTree()
        troncature.node = subTree.node
        troncature.isLeaf = subTree.isLeaf
        if not subTree.isLeaf:
            troncature.branches = subTree.branches
        #self.updateTreeDepth()
