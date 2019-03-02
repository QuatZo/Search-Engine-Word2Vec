# cast
# genres
# countries
# rating
# title
# year
# directors
# reviews
# production companies
# plot/synopsis
# awards (np. czy film dostał Oscara)
# keywords
# Opcjonalnie
# (writers
# producers
# editors)

# movie = ia.get_movie('0068646')
# for info in movie.infoset2keys['main']:
# print(info)
# print(movie.get(info))
# print(movie.get('top 250 rank'))

from imdb import IMDb, IMDbError

ia = IMDb()

fileR = open('imdbIDs.txt', "r").read()
fileR = fileR.split()

for row in fileR:
    if row == '0000001':
        try:
            movie = ia.get_movie(row)
            print(movie.get_current_info())
            movieMain = movie.infoset2keys['main']
            print(movieMain)
            print(movie['title'])
            # for info in movieMain:
            #     print(movie.get(info))
        except IMDbError as e:
            print(e)
