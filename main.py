import math
from math import factorial
import random

def getRandomMeasures(pArr, cArr, n: int):
    if (len(pArr) != len(cArr)):
        raise IndexError("arrays should be the same size")
    
    qArr = [0.0] * len(pArr)
    for i in range(1, len(pArr) - 1):
        qArr[i] += qArr[i-1] + pArr[i]
    qArr[len(qArr) - 1] = 1

    values = [0] * n
    for i in range(n):
        value = random.random()
        where = 0
        for w, j in enumerate(qArr, 1):
            if (value > qArr[w-1] and value < qArr[w]):
                where = w
                break
        values[i] = cArr[where]
    
    return values


def combinations(n: int, i: int):
    if (n < 0 or i < 0):
        raise ValueError("both arguments should be positive")
    return float(factorial(n)) / (factorial(i)*factorial(n-i))

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

def NegBiFunc(k: int, r: int, p: float):
    return combinations(k+r-1, k)*p^k*(p-1)^r

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