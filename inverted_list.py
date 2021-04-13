__author__ = "Hannes Halm"

import re
import matplotlib.pyplot as plt
import numpy as np
import cProfile


class InvertedIndex:

    def __init__(self):
        self.inverted_lists = {}
        self.number_of_films = 0
        self.number_of_words = 0

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
                        self.inverted_lists[word] = [[], 0]

                    self.inverted_lists[word][1] += 1

                    # Automatically sorted since for-loop
                    self.inverted_lists[word][0].append(record_id)

        for word, index_list in self.inverted_lists.items():
            index_list[0] = list(dict.fromkeys(index_list[0]))

    # Task 2
    def search_keyword(self, keywords):
        look = []
        for word in keywords:
            try:
                look.append(set(self.inverted_lists[word][0]))
            except:
                print(word, " was not found in any document")

        result = set(self.inverted_lists[keywords[0]][0]).intersection(*look)
        print(result)

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



def take_second(element):
    return element[1]


def main():
    movies = InvertedIndex()
    movies.read_from_file('movies.txt')

    print("Number of films: ", movies.number_of_films)
    print("Number of words: ", movies.number_of_words)
    #print("Amount of unique words ", len(movies.inverted_lists))

    keywords = ["japanese", "animated"]

    #movies.search_keyword(keywords)
    movies.plot_frequency()
    #movies.word_occurrence()



if __name__ == "__main__":
    cProfile.run('main()')