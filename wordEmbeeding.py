import numpy as np

fileR = open("database.csv", "r").read()

fileR = fileR.split("\n")

for i in range(len(fileR)):
    fileR[i] = fileR[i].split(';')

fileR = np.array(fileR[1:])

print(fileR)