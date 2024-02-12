from pydantic import BaseModel


class MenuData(BaseModel):
    price: int
    energy: float
    protein: float
    fat: float
    carbohydrates: float
    salt: float
    calcium: float
    vegetable: float
    img_url: str


class OptimizeInputData(BaseModel):
    max_budget: int
    list_include: list[str]
    list_exclude: list[str]
    list_menu_name: list[str]
    list_nutorition_name: list[str]
    nutorition_name_map_require_amount: dict[str, float]
    menu_name_map_menu_data: dict[str, MenuData]


class OptimizeOutputData(BaseModel):
    list_selected_menu_name: list[str]
    nutorition_name_map_amount: dict[str, float]
    total_cost: int
