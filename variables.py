# ----------------------------------------- DON'T TOUCH -------------------------------------------------------------- #
# Variables for every .py file

# region Path
path_to_model = "vocab.model"
path_to_dataset = "dataset.csv"
path_to_stop_words = "stop_words.txt"
# endregion

# region Search Engine
top_n = 3
probability_positive = dict()
rows_per_element = dict()
amount_of_rows = 30
# endregion

# region Preparation
rating_values = [round(0.1 * i, 2) for i in range(101)]


# endregion
