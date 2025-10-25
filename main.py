import math
import random
import numpy
import scipy
from collections import Counter

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

def pirsonForBernuli(arr):
    observed_counts = Counter(arr)
    return scipy.stats.chisquare([observed_counts[0], observed_counts[1]]).pvalue

def pirsonForNegBernuli(arr, r, p):
    from scipy.stats import nbinom
    from collections import Counter

    observed_counts = Counter(arr)
    total = len(arr)
    max_k = max(observed_counts.keys())

    # Собираем наблюдаемые и ожидаемые частоты
    observed = []
    expected = []

    for k in range(max_k + 1):
        observed.append(observed_counts.get(k, 0))
        expected_prob = nbinom.pmf(k, r, p)
        expected.append(expected_prob * total)

    # Нормализуем ожидаемые частоты, чтобы сумма совпадала с наблюдаемой
    expected_sum = sum(expected)
    observed_sum = sum(observed)
    if expected_sum == 0:
        raise ValueError("Ожидаемые частоты равны нулю — проверь параметры r и p")

    scale_factor = observed_sum / expected_sum
    expected = [e * scale_factor for e in expected]

    # Объединяем редкие категории (ожидаемая < 5)
    obs_combined = []
    exp_combined = []
    temp_obs = 0
    temp_exp = 0

    for o, e in zip(observed, expected):
        temp_obs += o
        temp_exp += e
        if temp_exp >= 5:
            obs_combined.append(temp_obs)
            exp_combined.append(temp_exp)
            temp_obs = 0
            temp_exp = 0

    # Добавляем остатки
    if temp_exp > 0:
        if obs_combined:
            obs_combined[-1] += temp_obs
            exp_combined[-1] += temp_exp
        else:
            obs_combined.append(temp_obs)
            exp_combined.append(temp_exp)

    # Проверка согласия
    chi2_stat, p_value = scipy.stats.chisquare(f_obs=obs_combined, f_exp=exp_combined)
    return p_value

def estimate_alpha_for_bernuli(trials=1000, n=1, p=0.5, epsilon=0.05):
    false_positives = 0
    for _ in range(trials):
        sample = [getBi(n, p) for _ in range(1000)]
        p_value = pirsonForBernuli(sample)
        if p_value < epsilon:
            false_positives += 1
    return false_positives / trials

def estimate_alpha_for_negbernuli(trials=1000, r=5, p=0.25, epsilon=0.05):
    false_positives = 0
    for _ in range(trials):
        sample = [getNegBi(r, p) for _ in range(1000)]
        p_value = pirsonForNegBernuli(sample, r, p)
        if p_value < epsilon:
            false_positives += 1
    return false_positives / trials


if __name__ == "__main__":
    n = 1000
    epsilon = 0.05
    bernuli = [getBi(1, 0.5) for i in range(n)]
    print("bernuli:", bernuli)
    negBernuli = [getNegBi(5, 0.25) for i in range(n)]
    print("negative Bernuli: ", negBernuli)
    print("bernuli difference betwen otsenka and real is", abs(0.5 - measureOfExpected(bernuli)))
    print("bernuli difference betwen dispersiya and real is", abs(0.25 - measureOfDispersiya(bernuli)))
    print("neg bernuli difference betwen otsenka and real is", abs(15 - measureOfExpected(negBernuli)))
    print("neg bernuli difference betwen dispersiya and real is", abs(60 - measureOfDispersiya(negBernuli)))
    # print(pirsonForBernuli(bernuli, [0.5, 0.5]))
    print("bernuli pirson: ", "passed" if pirsonForBernuli(bernuli) >= epsilon else "failed")
    # print(pirsonForNegBernuli(negBernuli, 5, 0.25))
    print("neg bernuli pirson: ", "passed" if pirsonForNegBernuli(negBernuli, 5, 0.25) >= epsilon else "failed")
    print("1 phaze error for bernuli: ", estimate_alpha_for_bernuli())
    print("1 phaze error for neg bernuli: ", estimate_alpha_for_negbernuli())