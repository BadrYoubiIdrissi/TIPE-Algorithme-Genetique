from Source.Node import Node
from numpy.polynomial import Polynomial

class DefaultSet():
    def __init__(self):
        add = Node((lambda args: args[0] + args[1]), 2, '+')
        sub = Node((lambda args: args[0] - args[1]), 2, '-')
        mult = Node((lambda args: args[0] * args[1]), 2, '*')
        self.termSet = [Polynomial([1]), Polynomial([0, 1])]
        self.funcSet = [add, sub, mult]