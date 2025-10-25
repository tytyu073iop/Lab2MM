import math
import random
import numpy

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

# несмещённая оценка мат ожидания
def measureOfExpected(arr):
    return numpy.mean(arr)

def measureOfDispersiya(arr):
    # Делаем n-1
    return numpy.var(arr, ddof=1)


if __name__ == "__main__":
    n = 1000
    bernuli = [getBi(1, 0.5) for i in range(n)]
    print("bernuli:", bernuli)
    negBernuli = [getNegBi(5, 0.25) for i in range(n)]
    print("negative Bernuli: ", negBernuli)
    print("bernuli difference betwen otsenka and real is", abs(0.5 - measureOfExpected(bernuli)))
    print("bernuli difference betwen dispersiya and real is", abs(0.25 - measureOfDispersiya(bernuli)))
    print("neg bernuli difference betwen otsenka and real is", abs(15 - measureOfExpected(negBernuli)))
    print("neg bernuli difference betwen dispersiya and real is", abs(60 - measureOfDispersiya(negBernuli)))