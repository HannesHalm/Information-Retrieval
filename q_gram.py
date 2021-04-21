import csv

tsv_file = open("wikidata-entities.tsv", encoding="utf8")
read_tsv = csv.reader(tsv_file, delimiter="\t")

for row in read_tsv:
    try:
        print(row)
    except:
        print("something went wrong")
