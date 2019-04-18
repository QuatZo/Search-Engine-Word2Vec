# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# TODO - Jak wszystko zostanie zrobione, trzeba nadpisac dataset nowym z uzupelnionym ratingiem                        #
# TODO - Jak skonczymy pobieranie danych, trzeba pousuwac wszystkie epizody (Notatnik++; Dawid)                        #
# TODO - Przekazywanie wynikow z search_engine do Django (Dawid)                                                       #
# TODO - Optymalizacja kodu (czesciowo zrobiona)                                                                       #
# Heart of our program

import pandas as pd

import variables as var
import model
import preparation as prep
import search_engine as se
import plot_vocab as pv

# region Logs (datetime)
print(f"{var.line} {var.now()} {var.line}")
# endregion

# region Model & Dataset
if not model.exists(var.path_to_model):
    print(f"Vocabulary {var.path_to_model} doesn't exist. Starting from the scratch.")
    df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0).values  # baza danych (czytamy pliki)
    processed_data = prep.prepare(df_set, var.path_to_stop_words, var.rating_values)  # przygotowywanie danych
    del df_set
    if not model.train(processed_data, var.path_to_model, arg_epochs=20, arg_iter=10):  # arg_iter=50 - nie polecam
        print("Whoops! Something went wrong while training model.")
        exit(-1)
else:
    print("Vocabulary already exists.")
# endregion

# region Input
inp = input("Input: ")
cleaned_data = prep.prepare([[inp]], var.path_to_stop_words, var.rating_values)[0]  # przygotowywanie inputu

ai_words = se.correlations(cleaned_data, var.path_to_model, var.top_n, var.ai_rows)  # korrelacje
df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0)
# endregion

# region Return
cleaned_data = '+'.join(cleaned_data)  # utworz link
print("Searching...")
print(f"Sending search result to {var.website}={cleaned_data}")
res = se.return_data(inp.split(), ai_words, df_set, var.total_rows)  # to bedzie szlo do WWW, czyli to bedzie returnem
del df_set
# endregion

# region Logs (newline)
print(f"{var.line*3}")
# endregion

# region Plot
# print(f"[{var.now()}] Plotting...")
# pv.display_allwords_tsnescatterplot(var.path_to_model)
# pv.display_closestwords_tsnescatterplot(var.path_to_model, ['disney', 'company', 'marvel'])
# print(f"[{var.now()}] Plotting completed.")
# endregion
