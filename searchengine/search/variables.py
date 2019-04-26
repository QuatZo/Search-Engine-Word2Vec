# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# Variables for every .py file
import datetime as dt

# region Path
folder = "search/"
path_to_model = folder + "vocab.model"
path_to_dataset = folder + "dataset.csv"
path_to_stop_words = folder + "stop_words.txt"
# endregion

# region Search Engine
top_n = 3  # ilosc wyrazow podobnych przypadajacych na jeden wyraz wejsciowy
ai_rows = 50  # ilosc wierszy dla wyrazow podobnych
total_rows = 100  # ogolna ilosc wierszy
# endregion

# region Main
line = "-"*10
website = "http://localhost:8000/search/table.html?search_text"


def now():
    return dt.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')  # logi
# endregion

