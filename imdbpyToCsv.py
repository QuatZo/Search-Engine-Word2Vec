# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Komentarze                                                                                                    #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane                                                           #
#                                                                                                                      #
# Jesli cos zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                       #
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

savedIds = list()  # przygotowanie do trzeciej pozycji z listy do zrobienia
fileSavedIds = open("dataSetIds.txt", "r+")  # baza movieID (tych które już mamy)

marks = {'.', ',', '<', '>', '/', '?', ';', ':', '\'', '\'s', '"', '[', '{', ']', '}', '!', '@', '#', '$', '%', '^',
         '&', '&', '*', '(', ')', '-', '_', '=', '+'}  # lista znakow specjalnych do usunięcia

lastId = str(1).zfill(7)  # ustawione jako 0000001
with open('dataSetIds.txt') as Ids:
    lastId = list(Ids)[-1]  # pobranie ostatniego id żeby nie powtarzać pobierania danych do pliku od początku
tempId = lastId

i = 0  # reshape <-> rows
for row in fileR:  # kazdy imdbID z bazy
    if int(row) <= int(tempId) + 10 and row > lastId:
        try:
            if int(row) % 100 == 0:
                print('dupa')
            movie = ia.get_movie(row)  # pobieramy info nt filmow o danym ID. Jak wywali Error -> wyświetla błąd ID

            # print(movie.get_current_info())
            # movieMain = movie.infoset2keys['main']
            # print(movieMain)
            listOfInfos = list()  # Lista informacji, które będziemy przechowywać inforamcje na temat jednego filmu
            listOfInfos.append(movie['title'])  # na początek tytuł
            listOfInfos.append(movie['year'])  # potem rok produkcji

            listOfDirectors = list()
            listOfDirectorsSpace = list()
            for director in movie['directors']:  # lista reżyserów, może być więcej niż jeden więc jest pętla
                tempDirectors = director['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                listOfDirectors.append(tempDirectors)
            listOfInfos.append(" ".join(listOfDirectors))

            listOfInfos.append(movie['rating'])  # ocena filmu
            listOfInfos.append(" ".join(movie['genres']))  # kategoria

            # usuwamy .::, autora tekstu i znaki specjalne -- START
            plots = list()
            plotsmarks = list()
            for plot in movie['plot']:
                index = plot.find(".::")  # szukamy ".::" i od tego miejsca ucinamy recenzje
                plot = plot[:index]
                plots.append(plot)
                for mark in marks:  # wyszukaj znaku interpunkcyjnego (lista marks) i go usun/zamien
                    plot = plot.replace(mark, '')
                plotsmarks.append(plot)
            # listOfInfos.append(" ".join(plots))
            listOfInfos.append(" ".join(plotsmarks))
            # usuwamy .::, autora tekstu i znaki specjalne  -- KONIEC

            if i == 0:
                keywords = list()  # tworzymy liste słów kluczowych do danego ID
                rowInfo = np.array(listOfInfos)  # tablica numpy (ma więcej metod)
                rowInfoLen = len(rowInfo)  # ilosc info jaką pobraliśmy z filmu
                i += 1  # powiększamy "i" czyli liczbę wierszy
            else:
                i += 1  # powiększamy "i" czyli liczbę wierszy
                rowInfo = np.append(rowInfo, listOfInfos).reshape((i, rowInfoLen))  # zmien tablice numpy na numpy 2D

            savedIds.append(row)

            # keywords -- START
            for word in listOfInfos[4].split():  # pętla która zapisuje wszystkie keywords
                if word not in keywords:
                    keywords.append(word)
            for word in listOfInfos[5].split():  # taka sama pętla, ale inne info
                if word not in keywords:
                    keywords.append(word)
            # keywords -- END

        except IMDbError as e:
            print(row, e)
        except KeyError as e:
            print("Brak pelnych danych filmu o ID: ", row, "; brakujace dane: ", e)

fileSavedIds.close()  # tutaj potrzebna talibca gdzie kolumną są wszystkie ID
npKeywords = np.array(keywords).reshape(len(keywords), 1)  # keywords

tempdataSet = pd.DataFrame(rowInfo,
                       columns=['title', 'year', 'directors', 'rating', 'genres', 'plotmarks'])  # stworz DataFrame
dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)

dataSet = pd.concat([dataSet, tempdataSet])
dataSet = dataSet.reset_index(drop=True)

tempdataKeywords = pd.DataFrame(keywords, columns=['keyword'])
dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)

dataKeywords = pd.concat([dataKeywords, tempdataKeywords])
dataKeywords = dataKeywords.reset_index(drop=True)

dataSet.to_csv("dataSet.csv", sep=";")  # przekonwertuj DataFrame to csv
dataKeywords.to_csv("dataKeywords.csv", sep=";")

fileSavedIds = open("dataSetIds.txt", "a+")  # to co trzeba zaimplementować, teraz zapisuje do dataSetIDs
for Id in savedIds:
    if Id not in fileSavedIds:
        fileSavedIds.write(Id + "\n")
fileSavedIds.close()
# pd.read_csv("dataKeywords.csv", sep=";", index_col=0) # metoda jak się odczytuje z pliku csv
