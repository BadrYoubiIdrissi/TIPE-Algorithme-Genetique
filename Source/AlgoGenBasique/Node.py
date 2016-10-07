class Node:
    """Implementation d'un Noeud (fonction)
        f = la fonction representative.
        / ! \ les parametres doivent être dans une liste
        arity = nomre de parametres  de la fonction
        symbol = representationde la fonction pour l'affichage"""
    def __init__(self, f, arity, symbol = 'No Symbol'):
        self.run = f
        self.arity = arity
        self.symbol = symbol