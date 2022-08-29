__author__ = "Hannes Halm"
import random
import string
import time
from profilehooks import profile

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def generate_test(length=10, n=10000):
    test = []
    for i in range(n):
        test.append("".join([random.choice(string.ascii_lowercase) for i in range(length)]))

    return test


def execute_test(test):
    result = []
    start = time.perf_counter()
    for i in range(len(test)):
        result.append(levenshtein(test[i], test[i-1]))
    return time.perf_counter() - start


times = []

for i in range(10):
    times.append(execute_test(generate_test()))

print(times)
print("Average time", sum(times)/len(times))