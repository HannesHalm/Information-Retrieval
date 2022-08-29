__author__ = "Hannes Halm"
import csv
from nltk import ngrams
import numpy as np
import matplotlib.pyplot as plt

class InvertedIndex:

    def __init__(self, q=3):
        self.inverted_lists = {}
        self.number_of_films = 0
        self.number_of_words = 0
        self.q = q

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


    def read_tsv_file(self, filename):
        tsv_file = open(filename, encoding="utf8")
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        record_id = 0
        for line in read_tsv:
            record_id += 1
            word = "$$" + line[0].replace(" ", "$$") + "$$"
            word = word.lower()

            # q-gram of size 3 iterate over padded word
            for i in range(len(word) - 2):
                self.number_of_words += 1

                q_word = word[i] + word[i + 1] + word[i + 2]    # construct word q-gram of size 3
                if q_word not in self.inverted_lists:
                    # Dict with word as key and values in order being IDs, frequency, score
                    self.inverted_lists[q_word] = [[], 0, 1]

                self.inverted_lists[q_word][1] += 1

                # Automatically sorted since for-loop
                self.inverted_lists[q_word][0].append(record_id)

        for word, index_list in self.inverted_lists.items():
            index_list[0] = list(dict.fromkeys(index_list[0]))

    def word_occurence(self):
        most_frequent = 0
        key = ""

        for word, inverted_list in self.inverted_lists.items():
            if most_frequent < inverted_list[1]:
                key = word
                most_frequent = inverted_list[1]

        return key

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

ii = InvertedIndex()
ii.read_tsv_file("wikidata-entities.tsv")

print("Amount of 3-grams", len(ii.inverted_lists.items()))
print("Amount of 3-grams", ii.number_of_words)
print("Amount of words that start with k", len(ii.inverted_lists["$$k"]))
most_frequent_word = ii.word_occurence()
print("Most frequent word", most_frequent_word, "total occurences:", ii.inverted_lists[most_frequent_word][1], "occurs in this many documents", len(ii.inverted_lists[most_frequent_word][0]))

ii.plot_frequency()


#for word, index_list in ii.inverted_lists.items():
 #   print(word, index_list)
