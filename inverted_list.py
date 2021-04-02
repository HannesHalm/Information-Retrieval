__author__ = "Hannes Halm"

import re
import matplotlib.pyplot as plt
import numpy as np

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
                        self.inverted_lists[word] = ([], 0)
                        #self.inverted_lists[word] = ([], 0)

                    # Automatically sorted since for-loop
                    self.inverted_lists[word][0].append(record_id)


    def search_keyword(self, keywords):
        look = []
        for word in keywords:
            try:
                look.append(set(self.inverted_lists[word][0]))
            except:
                print(word, " was not found in any document")

        result = set(self.inverted_lists[keywords[0]][0]).intersection(*look)
        print(result)


    def plot_frequency(self):
        frequency = []
        frequency_words = []
        for word, inverted_list in sorted(self.inverted_lists.items()):
            frequency.append(len(inverted_list[0]))
            frequency_words.append((word, len(inverted_list[0])))

        frequency_words.sort(key=take_second)
        frequency.sort(reverse=1)
        for word in frequency_words:
            print(word)

        plt.plot(frequency)
        plt.show()


def take_second(element):
    return element[1]


def main():
    movies = InvertedIndex()
    movies.read_from_file('movies.txt')

    print("Number of films: ", movies.number_of_films)
    print("Number of words: ", movies.number_of_words)
    #print("Amount of unique words ", len(movies.inverted_lists))


    keywords = ["japanese", "animated"]

    movies.search_keyword(keywords)
    movies.plot_frequency()
    #print(movies.inverted_lists[])


if __name__ == "__main__":
    main()