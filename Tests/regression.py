from numpy.polynomial import Polynomial
from numpy import linspace
import numpy as np
import matplotlib.pyplot as plt

def polLagrange(X,x):
    assert x in X
    lx = Polynomial([1])
    for i in X:
        if i != x and abs(x-i):
            lx *= Polynomial([-i,1])/(x-i)
    return lx


plt.close()
X = linspace(-np.pi, np.pi,30)

p = Polynomial([0])

for i in X:
    p += np.sin(i)*polLagrange(X,i)

X2 = linspace(-1, 1,1000)
plt.plot(X2, [p(x) for x in X2])
plt.plot(X2, np.sin(X2))
plt.show()
