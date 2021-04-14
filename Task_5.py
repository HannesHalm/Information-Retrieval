import random as r

length = 10
ordered_list = []
shuffled_list = []
for i in range(length):
    ordered_list.append(i)

shuffled_list = ordered_list.copy()
r.shuffle(shuffled_list)

ordered_sum = 0
for value in ordered_list:
    ordered_sum += value

print(ordered_sum)

shuffled_sum = 0
for value in shuffled_list:
    shuffled_sum += shuffled_list.index(value)

print(shuffled_sum)