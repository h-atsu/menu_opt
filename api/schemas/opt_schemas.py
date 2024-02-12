from pydantic import BaseModel, Field


class OptQuery(BaseModel):
    cafe_file_name: str = Field(None, example='kansita.csv')
    max_budget: int = Field(None, example=500)
    list_include: list[str]
    list_exclude: list[str]


class OptRet(BaseModel):
    list_selected_menu_name: list[str]
