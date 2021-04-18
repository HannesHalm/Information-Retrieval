__author__ = "Hannes Halm"

import re
import matplotlib.pyplot as plt
import numpy as np
from profilehooks import profile

class InvertedIndex:

    def __init__(self):
        self.inverted_lists = {}
        self.number_of_films = 0
        self.number_of_words = 0

    #@profile
    def read_from_file(self, file_name):
        record_id = 0
        with open(file_name, encoding='utf-8') as file:
            for line in file:
                record_id += 1
                self.number_of_films += 1
                words = re.split("[^a-zA-Z']+", line)       # Tokenize

                for word in words:
                    self.number_of_words += 1
                    word = word.lower()
                    if word not in self.inverted_lists:
                        # Dict with word as key and values in order being IDs, frequency, score
                        self.inverted_lists[word] = [[], 0, 1]

                    self.inverted_lists[word][1] += 1

                    # Automatically sorted since for-loop
                    self.inverted_lists[word][0].append(record_id)

        for word, index_list in self.inverted_lists.items():
            index_list[0] = list(dict.fromkeys(index_list[0]))

    # Task 2
    def and_query(self, keywords):
        result = []
        word_list = self.inverted_lists[keywords.pop(0)][0]

        for word in word_list:
            result.append([word, 0])

        for word in keywords:
            result = self.search_keyword(result, self.inverted_lists[word][0])

        print(result)

    #@profile
    def search_keyword(self, list1, list2):
        result = []
        i1 = 0
        i2 = 0

        n1 = len(list1)
        n2 = len(list2)
        while 1:
            if i1 < n1 and list1[i1][0] < list2[i2]:
                i1 += 1
            if i1 == n1: break
            if i2 < n2 and list2[i2] < list1[i1][0]:
                i2 += 1
            if i2 == n2: break
            if list1[i1][0] == list2[i2]:
                result.append([list1[i1][0], list1[i1][1] + 1])

                i1 += 1
                i2 += 1
                if i1 == n1 or i2 == n2: break

        return result

    # Task 3
    def plot_frequency(self):
        frequency = []
        frequency_words = []
        for word, inverted_list in sorted(self.inverted_lists.items()):
            frequency.append(inverted_list[1])
            frequency_words.append((inverted_list[1], word))

        frequency_words.sort()

        frequency.sort(reverse=1)
        x_axis = np.array(np.linspace(1, len(frequency_words), len(frequency_words)))
        y_axis = np.array(frequency)

        # log both scales
        x_axis = np.log10(x_axis)
        y_axis = np.log10(y_axis)

        # calculate alpha using regression
        m, b = np.polyfit(x_axis, y_axis, 1)
        print("alpha", -m)

        # plot
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plt.xlabel("n th word")
        plt.ylabel("word frequency")
        ax1.plot(frequency)
        ax2.plot(x_axis, y_axis)

        plt.show()

    # Task 4
    def word_occurrence(self):
        frequency = []
        frequency_words = []
        for word, inverted_list in sorted(self.inverted_lists.items()):
            frequency.append(len(inverted_list[0]))
            frequency_words.append((word, len(inverted_list[0])))

        frequency_words.sort(key=take_second)
        frequency.sort(reverse=1)


        for list in frequency_words:
            print(list[0], list [1])


    def or_query(self, keywords):
        result = []
        word_list = self.inverted_lists[keywords.pop(0)][0]

        for word in word_list:
            result.append([word, 1])

        for word in keywords:
            result = self.or_search(result, self.inverted_lists[word][0])

        print("or ",result)

    #@profile
    def or_search(self, list1, list2):
        result = []
        i1 = 0
        i2 = 0

        n1 = len(list1)
        n2 = len(list2)
        while 1:
            if i1 < n1 and list1[i1][0] < list2[i2]:
                result.append([list1[i1][0], list1[i1][1]])
                i1 += 1
            if i1 == n1: break
            if i2 < n2 and list2[i2] < list1[i1][0]:
                result.append([list2[i2], 1])
                i2 += 1
            if i2 == n2: break

            if list1[i1][0] == list2[i2]:
                result.append([list1[i1][0], list1[i1][1] + 1])
                i1 += 1
                i2 += 1
                if i1 == n1 or i2 == n2: break

        return result



def take_second(element):
    return element[1]


def main():
    movies = InvertedIndex()
    movies.read_from_file('movies_reduced.txt')

    print("Number of films: ", movies.number_of_films)
    print("Number of words: ", movies.number_of_words)
    #print("Amount of unique words ", len(movies.inverted_lists))

    keywords = ["comedy", "japanese", "and", "the"]

    movies.and_query(keywords)
    movies.or_query(keywords)
    #movies.plot_frequency()
    #movies.word_occurrence()



if __name__ == "__main__":
    main()