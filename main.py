import math
import random

# биномиальное распределение (Бернули при n = 1)
def getBi(n: int, p:float):
    if (p > 1 or p < 0):
        raise ValueError("p is varoyatnost uspeha ot 0 do 1")
    if (n < 1):
        raise ValueError("n is naturalnoe")
    
    sluchaunayaVelechina = 0;
    for i in range(n):
        sluchaunayaVelechina += math.floor(p - random.random() + 1)
    return sluchaunayaVelechina

#returns negative results amount
def getNegBi(r: int, p: float):
    if not (r >= 1 and 0 < p < 1):
        raise ValueError("Неверные параметры: r ≥ 1, 0 < p < 1")

    failures = 0
    successes = 0

    while successes < r:
        if random.random() < p:
            successes += 1
        else:
            failures += 1

    return failures


for i in range(10):
    print(getBi(1000, 0.5))
print('\nstep\n')
for i in range(10):
    print(getNegBi(1000, 0.5))