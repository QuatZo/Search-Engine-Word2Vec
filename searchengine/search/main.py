import pandas as pd

from .variables import path_to_model, path_to_stop_words, path_to_dataset, top_n, ai_rows, total_rows, line, \
    website, now
from .model import exists, train
from .preparation import prepare
from .search_engine import correlations, return_data


def search(inp):
    print(f"\n{line} {now()} {line}")
    if not exists(path_to_model):
        print(f"Vocabulary {path_to_model} doesn't exist. Starting from the scratch.")
        df_set = pd.read_csv(path_to_dataset, sep=";", index_col=0).values  # baza danych (czytamy pliki)
        processed_data = prepare(df_set, path_to_stop_words)
        del df_set
        if not train(processed_data, path_to_model, now(), arg_epochs=30, arg_iter=10, arg_size=300, arg_sample=6e-5,
                     arg_min_count=3):
            print("Whoops! Something went wrong while training model.")
            exit(-1)
    else:
        print("Vocabulary already exists.")

    cleaned_data = prepare([[inp]], path_to_stop_words)[0]
    ai_words = correlations(cleaned_data, path_to_model, top_n, ai_rows)
    df_set = pd.read_csv(path_to_dataset, sep=";", index_col=0)
    cleaned_data_link = '+'.join(cleaned_data)
    print("Searching...")
    print(f"Sending search result to {website}={cleaned_data_link}")
    res = return_data(cleaned_data, ai_words, df_set, total_rows)  # to bedzie szlo do WWW, czyli to bedzie returnem

    del df_set

    print(f"{line*3}\n")

    return res
