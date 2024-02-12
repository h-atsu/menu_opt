import pandas as pd
from model.dataclass import OptimizeInputData, MenuData


def make_optimize_input_data(menu_df: pd.DataFrame,  max_budget: int, list_include: list[str], list_exclude: list[str]) -> OptimizeInputData:
    list_menu_name = menu_df['name'].tolist()
    list_nutorition_name = menu_df.columns[2:-1].tolist()

    menu_name_map_menu_data = {}
    for row in menu_df.itertuples():
        menu_name_map_menu_data[row.name] = MenuData(
            price=row.price,
            energy=row.energy,
            protein=row.protein,
            fat=row.fat,
            carbohydrates=row.carbohydrates,
            salt=row.salt,
            calcium=row.calcium,
            vegetable=row.vegetable,
            img_url=row.img_url
        )
        nutorition_name_map_require_amount = {
            'energy': 2650 / 3,
            'protein': 65 / 3,
            'fat': 60 / 3,
            'carbohydrates': 300 / 3,
            'salt': 7.5 / 3,  # 以下
            'calcium': 800 / 3,
            'vegetable': 350 / 3  # 以上
        }

    return OptimizeInputData(
        max_budget=max_budget,
        list_include=list_include,
        list_exclude=list_exclude,
        list_menu_name=list_menu_name,
        list_nutorition_name=list_nutorition_name,
        nutorition_name_map_require_amount=nutorition_name_map_require_amount,
        menu_name_map_menu_data=menu_name_map_menu_data,
    )
