# ----------------------------------------------------- CREDITS ------------------------------------------------------ #
# PLOT - ALL WORDS - https://stackoverflow.com/a/43956937                                                              #
# PLOT - https://medium.com/@aneesha/using-tsne-to-plot-a-subset-of-similar-words-from-word2vec-bb8eeaea6229           #

import numpy as np
import matplotlib.pyplot as plt
from gensim.models import word2vec
from sklearn.manifold import TSNE
import pandas as pd


def display_allwords_tsnescatterplot(arg_path_to_model):
    model = word2vec.Word2Vec.load(arg_path_to_model)
    vocab = list(model.wv.vocab)
    X = model[vocab]
    tsne = TSNE(n_components=2, random_state=0)
    X_tsne = tsne.fit_transform(X)
    df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)  # labele to to co laguje wykres
    plt.show()


def display_closestwords_tsnescatterplot(arg_path_to_model, word):
    model = word2vec.Word2Vec.load(arg_path_to_model)
    for i in range(len(word)):
        arr = np.empty((0, 300), dtype='f')
        word_labels = [word[i]]

        # get close words
        close_words = model.similar_by_word(word[i])

        # add the vector for each of the closest words to the array
        arr = np.append(arr, np.array([model[word[i]]]), axis=0)
        for wrd_score in close_words:
            wrd_vector = model[wrd_score[0]]
            word_labels.append(wrd_score[0])
            arr = np.append(arr, np.array([wrd_vector]), axis=0)

        # find tsne coords for 2 dimensions
        tsne = TSNE(n_components=2, random_state=0)
        np.set_printoptions(suppress=True)
        Y = tsne.fit_transform(arr)

        x_coords = Y[:, 0]
        y_coords = Y[:, 1]
        # display scatter plot
        plt.scatter(x_coords, y_coords)

        for label, x, y in zip(word_labels, x_coords, y_coords):
            plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')

    # Zmiana mnoznika powoduje zmiane 'przyblizenia' wykresu (mniejszy mnoznik = wieksze przyblizenie)
    plt.xlim(x_coords.min()*1, x_coords.max()*1)
    plt.ylim(y_coords.min()*1, y_coords.max()*1)
    plt.show()
