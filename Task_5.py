__author__ = "Hannes Halm"
import random as r
import time as t
import matplotlib.pyplot as plt

def sum_ordered_list(ordered_list):
    start = t.process_time()
    ordered_sum = 0
    for value in ordered_list:
        ordered_sum += value

    end = t.process_time()
    return end - start

def sum_unordered_list(ordered_list):
    shuffled_list = ordered_list.copy()
    r.shuffle(shuffled_list)

    start = t.process_time()
    shuffled_sum = 0
    for value in shuffled_list:
        shuffled_sum += shuffled_list[value]

    end = t.process_time()
    return end - start

def main():
    length = 10000
    iterations = 10
    ordered_list = []

    ordered_times = []
    unordered_times = []
    for i in range(length):
        ordered_list.append(i)

    for i in range(iterations):
        for i in range(length - len(ordered_list)):
            ordered_list.append(i)

        ordered_times.append(sum_ordered_list(ordered_list))
        unordered_times.append(sum_unordered_list(ordered_list))

        print(len(ordered_list))

        length *= 2

    print(ordered_times)
    print(unordered_times)
    line1, = plt.plot(ordered_times, label="ordered_times")
    line2, = plt.plot(unordered_times, label="unordered_times")
    plt.legend([line1, line2], ['ordered', 'unordered'])
    plt.xlabel("iteration")
    plt.ylabel("time")
    plt.show()
if __name__ == "__main__":
    main()