from pydantic import BaseModel, Field


class RequestMenuData(BaseModel):
    name: str
    price: int
    energy: float
    protein: float
    fat: float
    carbohydrates: float
    salt: float
    calcium: float
    vegetable: float
    img_url: str


class APIRequest(BaseModel):
    cafe_file_name: str = Field(None, example='kansita.csv')
    max_budget: int = Field(None, example=500)
    list_include: list[str]
    list_exclude: list[str]


class APIResponse(BaseModel):
    list_selected_menu_data: list[RequestMenuData]
    nutorition_name_map_amount: dict[str, float]
    total_cost: int
