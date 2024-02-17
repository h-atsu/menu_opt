from fastapi import APIRouter
from scripts.run_optimize import main as opt_main
from schemas.api_schemas import APIRequest, APIResponse, RequestMenuData

router = APIRouter()


@router.post("/optimize", response_model=APIResponse)
async def optimize_menu(req: APIRequest):
    optimize_input_data, optimize_output_data = opt_main(
        f'../data/{req.cafe_file_name}', req.max_budget, req.list_include, req.list_exclude)

    menu_name_map_menu_data = optimize_input_data.menu_name_map_menu_data
    list_selected_menu_name = optimize_output_data.list_selected_menu_name
    nutorition_name_map_amount = optimize_output_data.nutorition_name_map_amount
    total_cost = optimize_output_data.total_cost

    selected_menu_name_map_menu_data = {
        s: menu_name_map_menu_data[s] for s in list_selected_menu_name}

    list_selected_menu_data = []
    for s in list_selected_menu_name:
        menu_data = RequestMenuData(
            name=s,
            **dict(menu_name_map_menu_data[s])
        )
        list_selected_menu_data.append(menu_data)

    api_response = APIResponse(
        list_selected_menu_data=list_selected_menu_data,
        nutorition_name_map_amount=nutorition_name_map_amount,
        total_cost=total_cost
    )

    return api_response
