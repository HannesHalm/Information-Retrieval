import csv
from nltk import ngrams

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
            for i in range(len(word) - 3):
                q_word = word[i] + word[i + 1] + word[i + 2]
                if q_word not in self.inverted_lists:
                    # Dict with word as key and values in order being IDs, frequency, score
                    self.inverted_lists[q_word] = [[], 0, 1]

                self.inverted_lists[q_word][1] += 1

                # Automatically sorted since for-loop
                self.inverted_lists[q_word][0].append(record_id)

        for word, index_list in self.inverted_lists.items():
            index_list[0] = list(dict.fromkeys(index_list[0]))



ii = InvertedIndex()
ii.read_tsv_file("wikidata-entities.tsv")

print(len("Amount of 3-grams", ii.inverted_lists.items()))
print("Amount of words that start with k", len(ii.inverted_lists["$$k"]))
print("")
#for word, index_list in ii.inverted_lists.items():
 #   print(word, index_list)
