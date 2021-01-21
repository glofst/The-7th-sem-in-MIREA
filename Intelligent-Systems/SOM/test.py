from math import log

result = [(n / (2 * log(n)))/n for n in range(2, 100)]
print(result)
print(sum(result) / len(result))
