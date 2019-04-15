# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# Variables for every .py file
import datetime as dt
# region Path
path_to_model = "vocab.model"
path_to_dataset = "dataset.csv"
path_to_stop_words = "stop_words.txt"
# endregion

# region Search Engine
top_n = 3
probability_positive = dict()
rows_per_element = dict()
ai_rows = 50
total_rows = 100
# endregion

# region Preparation
rating_values = [round(0.1 * i, 2) for i in range(101)]
# endregion

# region Main
line = "-"*10
website = "http://localhost:8000/search/table.html?search_text"
def now():
    return dt.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
# endregion

