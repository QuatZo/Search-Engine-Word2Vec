# Dziala na pythonie 3.6, tensorflow nie dziala jeszcze na 3.7; pobrac z neta, zainstalowac 3.6
# Plik -> Opcje -> wyszukac 'interpreter', wyswietlic wszystkie, dodac swoj i wybrac 3.6
# zainstalowac ponizsze pakiety w w/w miejscu

import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # usuwa error

fileR = open("database.csv", "r").read()

fileR = fileR.split("\n")

for i in range(len(fileR)):
    fileR[i] = fileR[i].split(';')
    for j in range(len(fileR[i])):
        fileR[i][j] = fileR[i][j].split()

fileR = np.array(fileR[1:])

np1D = fileR.flatten()
print(np1D)

# fileRTf = tf.convert_to_tensor(fileR)
# sess = tf.InteractiveSession()
# print(fileRTf.eval())
# sess.close()
