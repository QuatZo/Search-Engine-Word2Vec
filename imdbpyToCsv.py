# -------------------------------------------- TODO: ----------------------------------------------------------------- #
#                                                                                                                      #
# ----- Sposob zapisu autora (nie moze byc spacji)                                                                     #
# ----- Usuniecie znakow interpunkcyjnych ze zdan (wiaze sie z tym podzielenie recenzji etc na kolejne listy - zdań    #
# ----- Zapamiętywanie ostatniego zapisanego ID, by co odpalenie nie importowal danych z filmow o ID od 0000001        #
# ----- Komentarze                                                                                                     #
# ----- Zmienne lepiej odzwierciedlajace przechowywane dane                                                            #
#                                                                                                                      #
# Jesli cos z TODO zrobicie to usuncie. Jak zrobicie wszystko z listy TODO zostawcie naglowek i te wiadomosc           #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from imdb import IMDb, IMDbError
import numpy as np
import pandas as pd

ia = IMDb()

fileR = open('imdbIDs.txt', "r").read()  # read file
fileR = fileR.split()  # list from string

# listOfInfos = ['genres', 'countries', 'rating', 'title', 'year', 'directors', 'plot', 'producers']
# temporary deleted: 'reviews', 'synapsis', 'awards', 'keywords', 'writers', 'editors'
# unnecessary: 'cast', 'production companies',
# print(ia.get_movie_infoset())  # args

savedIds = list()
fileSavedIds = open("dataSetIds.txt", "r")  # baza movieID

i = 1  # reshape <-> rows
for row in fileR:  # kazdy movieID z bazy
    if int(row) < 1000:  # test
        try:
            movie = ia.get_movie(row)  # info nt filmow

            # print(movie.get_current_info())
            # movieMain = movie.infoset2keys['main']
            # print(movieMain)
            listOfInfos = list()
            listOfInfos.append(movie['title'])
            listOfInfos.append(movie['year'])

            listOfDirectors = list()
            for director in movie['directors']:
                listOfDirectors.append(director['name'])
            listOfInfos.append(" ".join(listOfDirectors))

            listOfInfos.append(movie['rating'])
            listOfInfos.append(" ".join(movie['genres']))

            # usuwamy .:: i autora tekstu -- START
            plots = list()
            for plot in movie['plot']:
                index = plot.index(".::")
                plot = plot[:index]
                plots.append(plot)
            listOfInfos.append(" ".join(plots))
            # usuwamy .:: i autora tekstu -- KONIEC

            if row == '0000001':
                keywords = list()
                rowInfo = np.array(listOfInfos)  # tablica numpy
                rowInfoLen = len(rowInfo)  # ilosc info per film
            else:
                i += 1
                rowInfo = np.append(rowInfo, listOfInfos).reshape((i, rowInfoLen))  # zmien tablice numpy na numpy 2D

            savedIds.append(row)

            # keywords -- START
            for word in listOfInfos[4].split():
                if word not in keywords:
                    keywords.append(word)
            for word in listOfInfos[5].split():
                if word not in keywords:
                    keywords.append(word)
            # keywords -- END

        except IMDbError as e:
            print(row, e)
        except KeyError as e:
            print("Brak pelnych danych filmu o ID: ", row, "; brakujace dane: ", e)

fileSavedIds.close()
npKeywords = np.array(keywords).reshape(len(keywords), 1)  # keywords

dataSet = pd.DataFrame(rowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plot'])  # stworz DataFrame
dataKeywords = pd.DataFrame(keywords, columns=['keyword'])

dataSet.to_csv("dataSet.csv", sep=";")  # przekonwertuj DataFrame to csv
dataKeywords.to_csv("dataKeywords.csv", sep=";")

fileSavedIds = open("dataSetIds.txt", "a+")
for Id in savedIds:
    if Id not in fileSavedIds:
        fileSavedIds.write(Id + "\n")
fileSavedIds.close()
# pd.read_csv("dataKeywords.csv", sep=";", index_col=0)
