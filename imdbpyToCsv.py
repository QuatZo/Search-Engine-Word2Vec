from imdb import IMDb, IMDbError
import numpy as np
import pandas as pd

ia = IMDb()

fileR = open('imdbIDs.txt', "r").read()  # read file
fileR = fileR.split()  # list from string

# listOfInfos = ['genres', 'countries', 'rating', 'title', 'year', 'directors', 'plot', 'producers']
# temporary deleted: 'reviews', 'synapsis', 'awards', 'keywords', 'writers', 'editors'
# unnecessary: 'cast', 'production companies',


print(ia.get_movie_infoset())  # args
i = 1  # reshape <-> rows

for row in fileR:  # every movie id from database
    if row == '0000001' or row == '0000002':  # test
        try:
            movie = ia.get_movie(row)  # download all info about movie
            # print(movie.get_current_info())
            # movieMain = movie.infoset2keys['main']
            # print(movieMain)
            listOfInfos = list()
            listOfInfos.append(movie['title'])
            listOfInfos.append(movie['year'])

            listOfDirectors = list()
            for director in movie['directors']:
                listOfDirectors.append(director['name'])
            listOfInfos.append(" ,".join(listOfDirectors))

            listOfInfos.append(movie['rating'])
            listOfInfos.append(", ".join(movie['genres']))
            listOfInfos.append(", ".join(movie['plot']))

            if row == '0000001':
                rowInfo = np.array(listOfInfos)  # create an array
                rowInfoLen = len(rowInfo)  # amount of infos per movie
            else:
                i += 1
                rowInfo = np.append(rowInfo, listOfInfos).reshape((i, rowInfoLen))  # add to an array and reshape to 2D
        except IMDbError:
            print(e)

dataSet = pd.DataFrame(rowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plot'])  # create DataFrame (for AI)
dataSet.to_csv("database.csv", sep=";")  # convert DataFrame to csv
