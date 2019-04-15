# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# TODO - Jak wszystko zostanie zrobione, trzeba nadpisac dataset nowym z uzupelnionym ratingiem                        #
# TODO - Jak skonczymy pobieranie danych, trzeba pousuwac wszystkie epizody                                            #
# TODO - Przekazywanie wynikow z search_engine do Django (Dawid)                                                       #
# TODO - Optymalizacja kodu                                                                                            #
# Heart of our program

import pandas as pd
import variables as var
import model
import preparation as prep
import search_engine as se
import plot_vocab as pv


if not model.exists(var.path_to_model):
    print(f"[{var.now()}] Vocabulary", var.path_to_model, "doesn't exist. Starting from the scratch.")
    print(var.line)
    df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0).values  # baza danych (czytamy pliki)
    processed_data = prep.prepare(df_set, var.path_to_stop_words, var.rating_values)
    df_set = None
    if not model.train(processed_data, var.path_to_model, arg_epochs=20, arg_iter=10):  # arg_iter=50 - nie polecam
        print(f"[{var.now()}] Whoops! Something went wrong while training model.")
        exit(-1)
else:
    print(f"[{var.now()}] Vocabulary already exists.")
    print(var.line)

inp = input(f"[{var.now()}] What are you looking for? ")
print(var.line)

cleaned_data = prep.prepare([[inp]], var.path_to_stop_words, var.rating_values)[0]
print(var.line)

ai_words = se.correlations(cleaned_data, var.path_to_model, var.top_n, var.ai_rows)
df_set = pd.read_csv(var.path_to_dataset, sep=";", index_col=0)
cleaned_data = '+'.join(cleaned_data)
print(f"[{var.now()}] Sending search result to WWW. It should be visible at {var.website}={cleaned_data}")
res = se.return_data(inp.split(), ai_words, df_set, var.total_rows)  # to bedzie szlo do WWW, czyli to bedzie returnem
for row in res:
    print(row)

df_set = None
print(var.line)

print(f"[{var.now()}] Plotting...")
# pv.display_allwords_tsnescatterplot(var.path_to_model)
pv.display_closestwords_tsnescatterplot(var.path_to_model, ['disney', 'company', 'marvel'])
print(f"[{var.now()}] Plotting completed.")
