import os
import pandas as pd
from model.make_input_data import make_optimize_input_data
from model.cbc_model import CBC_Model

FILE_PATH = '../data/kansita.csv'


def main(FILE_PATH: str, max_budget: int, list_include: list[str], list_exclude: list[str]):
    menu_df = pd.read_csv(FILE_PATH)
    optimize_input_data = make_optimize_input_data(
        menu_df, max_budget, list_include, list_exclude)

    # model定義 & 実行
    model = CBC_Model(optimize_input_data)
    model.add_variable()
    model.add_constraint()
    model.add_objective()
    model.optimize()
    optimize_output_data = model.get_result()

    return optimize_input_data, optimize_output_data


if __name__ == '__main__':
    main(FILE_PATH, 500, ['ライス'], ['牛乳'])
