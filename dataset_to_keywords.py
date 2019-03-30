import numpy as np
import pandas as pd


# region Variables
path_to_dataset = "dataset.csv"
path_to_keywords = "datakeywords.csv"
percentages = [5*p for p in range(1, 21)]
corpus = list()
i = 0
# endregion

# region Files
df_set = pd.read_csv(path_to_dataset, sep=";", index_col=0)  # baza danych (czytamy pliki)
try:
    datakeywords = pd.read_csv(path_to_keywords, sep=";", index_col=0).to_numpy()  # czytaj plik .csv
except FileNotFoundError as e:
    open(path_to_keywords, "w+").write(";keyword")  # jeśli go nie ma, to utwórz
    datakeywords = pd.read_csv(path_to_keywords, sep=";", index_col=0).to_numpy()  # a potem czytaj
# endregion

# region Tokenization
for row in df_set.values:
    temp_str = ""
    for i in range(len(row)):
        if i == 1 or i == 3:
            continue
        if str(row[i]).casefold() != 'nan':
            temp_str += str(row[i]).replace('.', ',').casefold() + '.'
    corpus.append(temp_str)
corpus = "".join(corpus)
corpus = corpus.replace('?', '.').replace('!', '.').split('.')  # zamiana znaków '?' i '!' na kropki
tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji
tokenized_sentences_len = len(tokenized_sentences)
# endregion

# region Keywords
percentage = tokenized_sentences_len / 100
for sentence in tokenized_sentences:
    i += 1
    for word in sentence:
        try:
            int(word)
        except ValueError:
            if word in datakeywords:
                continue
            datakeywords = np.append(datakeywords, word)
    actual_percentage = round(i / percentage)
    for j in percentages:
        if i == int(percentage * j):
            print(actual_percentage, '% [{}/{}]'.format(i, tokenized_sentences_len))

datakeywords = pd.DataFrame(datakeywords, columns=['keyword'])
datakeywords.to_csv(path_to_keywords, sep=";")  # zmiana na plik .csv
# endregion
