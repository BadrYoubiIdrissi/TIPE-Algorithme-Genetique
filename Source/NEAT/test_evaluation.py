

from Individu import Individu
#import sys
#sys.path.append('chemin')
#Si sur Pyzo

prem=Individu(3,1)

print((prem.entrees[0]).valeur)
(prem.entrees[0]).valeur = 2
print((prem.entrees[0]).valeur)


print(prem.eval_part(0,[-1,0,1]))
print(prem.eval_part(1,[-1,0,1]))
print(prem.eval_part(2,[-1,0,1]))
print(prem.eval_part(3,[-1,0,1]))
print(prem.evaluation([-1,0,1]))


#L'évaluation e fonctionne pas, on a toujours la somme "sum" égale à 0