from fastapi import APIRouter
from scripts.run_optimize import main as opt_main
from schemas.opt_schemas import OptRet, OptQuery

router = APIRouter()


@router.post("/optimize", response_model=OptRet)
async def optimize_menu(opt_query: OptQuery):
    optimize_input_data, optimize_output_data = opt_main(
        f'../data/{opt_query.cafe_file_name}', opt_query.max_budget, opt_query.list_include, opt_query.list_exclude)
    return {'list_selected_menu_name': optimize_output_data.list_selected_menu_name}
