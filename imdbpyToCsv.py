# -------------------------------------------- TODO: ----------------------------------------------------------------- #
#                                                                                                                      #
# ----- Sposob zapisu autora (nie moze byc spacji)                                                                     #
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

savedIds = list()  # przygotowanie do trzeciej pozycji z listy TODO
fileSavedIds = open("dataSetIds.txt", "r+")  # baza movieID (tych które już mamy)

marks = {('.', ''), (',', ''), (':', ''), ('(', ''), (')', '')}  # lista znakow interpunkcyjnych do usunięcia

i = 1  # reshape <-> rows
for row in fileR:  # kazdy imdbID z bazy
    if int(row) < 10:  # test do 1000, żeby nie pobierać wszystkich xD, nie będzie jej jak będziemy pobierać wszystko
        try:
            movie = ia.get_movie(row)  # pobieramy info nt filmow o danym ID. Jak wywali Error -> wyświetla błąd ID

            # print(movie.get_current_info())
            # movieMain = movie.infoset2keys['main']
            # print(movieMain)
            listOfInfos = list()  # Lista informacji, w której będziemy przechowywać inforamcje na temat jednego filmu
            listOfInfos.append(movie['title'])  # na początek tytuł
            listOfInfos.append(movie['year'])  # potem rok produkcji

            listOfDirectors = list()
            for director in movie['directors']:  # lista reżyserów, może być więcej niż jeden więc jest pętla
                listOfDirectors.append(director['name'])  # imie reżysera
            listOfInfos.append(" ".join(listOfDirectors))

            listOfInfos.append(movie['rating'])          # ocena filmu
            listOfInfos.append(" ".join(movie['genres']))  # kategoria

            # usuwamy .:: i autora tekstu -- START
            plots = list()
            for plot in movie['plot']:
                index = plot.index(".::")  # szukamy ".::" i od tego miejsca ucinamy recenzje
                plot = plot[:index]
                plots.append(plot)
            listOfInfos.append(" ".join(plots))
            # usuwamy .:: i autora tekstu -- KONIEC

            # lista bez znaków interpunkcyjnych
            # usuwamy .:: i autora tekstu -- START
            plotsmarks = list()
            for plot in movie['plot']:
                index = plot.index(".::")  # szukamy ".::" i od tego miejsca ucinamy recenzje
                plot = plot[:index]
                for mark, blank in marks: # wyszukaj znaku interpunkcyjnego (lista marks) i go usun/zamien
                    plot = plot.replace(mark, blank)
                plotsmarks.append(plot)
            listOfInfos.append(" ".join(plotsmarks))
            # usuwamy .:: i autora tekstu -- KONIEC

            if row == '0000001':
                keywords = list()  # tworzymy liste słów kluczowych do danego ID
                rowInfo = np.array(listOfInfos)  # tablica numpy (ma więcej metod)
                rowInfoLen = len(rowInfo)  # ilosc info jaką pobraliśmy z filmu
            else:
                i += 1 # powiększamy "i" czyli liczbę wierszy
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

dataSet = pd.DataFrame(rowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plot', 'plotmarks'])  # stworz DataFrame
dataKeywords = pd.DataFrame(keywords, columns=['keyword'])

dataSet.to_csv("dataSet.csv", sep=";")  # przekonwertuj DataFrame to csv
dataKeywords.to_csv("dataKeywords.csv", sep=";")

fileSavedIds = open("dataSetIds.txt", "a+")  # to co trzeba zaimplementować, teraz zapisuje do dataSetIDs
for Id in savedIds:
    if Id not in fileSavedIds:
        fileSavedIds.write(Id + "\n")
fileSavedIds.close()
# pd.read_csv("dataKeywords.csv", sep=";", index_col=0) # metoda jak się odczytuje z pliku csv
