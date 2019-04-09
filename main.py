# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# Heart of our program

import pandas as pd

import variables as var
import model
import preparation as prep
import search_engine as se
import plot_vocab as pv


if not model.exists(var.path_to_model):
    print("Vocabulary", var.path_to_model, "doesn't exist. Starting from the scratch.")
    df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0).values  # baza danych (czytamy pliki)
    processed_data = prep.prepare(df_set, var.path_to_stop_words, var.rating_values)
    df_set = None
    if not model.train(processed_data, var.path_to_model, arg_epochs=20, arg_iter=10):  # arg_iter=50 - nie polecam
        print("Whoops! Something went wrong while training model.")
        exit(-1)
else:
    print("Vocabulary already exists.")

inp = input("What are you looking for? ")

cleaned_data = prep.prepare([[inp]], var.path_to_stop_words, var.rating_values)[0]
print("-"*10)
print(se.correlations(cleaned_data, var.path_to_model, top_n=var.top_n, amount_of_rows=var.amount_of_rows))
df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0)
# print(se.return_data(0, {'marvel': 10, 'floor': 7}, df_set))
se.return_data(0, {'marvel': 10, 'floor': 7}, df_set)
print("-"*10)
print("Plotting...")
# pv.display_allwords_tsnescatterplot(var.path_to_model)
pv.display_closestwords_tsnescatterplot(var.path_to_model, ['disney', 'company', 'movie'])
print("Plotting completed.")
