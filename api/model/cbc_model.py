from model.dataclass import OptimizeOutputData
from mip import Model, xsum, maximize, BINARY, MINIMIZE, CBC


class CBC_Model:
    def __init__(self, optimize_input_data):
        # Data
        self._max_budget = optimize_input_data.max_budget
        self._list_include = optimize_input_data.list_include
        self._list_exclude = optimize_input_data.list_exclude
        self._list_menu_name = optimize_input_data.list_menu_name
        self._list_nutorition_name = optimize_input_data.list_nutorition_name
        self._nutorition_name_map_require_amount = optimize_input_data.nutorition_name_map_require_amount
        self._menu_name_map_menu_data = optimize_input_data.menu_name_map_menu_data

        self._menu_name_nutorition_name_map_val = {}
        for s in self._list_menu_name:
            menu_data = self._menu_name_map_menu_data[s]
            for n in self._list_nutorition_name:
                self._menu_name_nutorition_name_map_val[s, n] = getattr(
                    menu_data, n)

        self._menu_name_map_menu_price = {s: getattr(
            self._menu_name_map_menu_data[s], 'price') for s in self._list_menu_name}

        self._model = Model(solver_name=CBC)
        # decision variable
        self._x_s = {}  # for menu set S
        self._z_n = {}  # for nutorition set N

        # intermediate variable
        self._nutorition_sum_n = {}  # selected menu's total nutorition amount

    def add_variable(self):
        for s in self._list_menu_name:
            self._x_s[s] = self._model.add_var(f'{s}', var_type=BINARY)

        for n in self._list_nutorition_name:
            self._z_n[n] = self._model.add_var(f'{n}', lb=0)

    def add_constraint(self):
        # max budget
        self._model += xsum(self._x_s[s] * self._menu_name_map_menu_price[s]
                            for s in self._list_menu_name) <= self._max_budget

        # slack constraint
        for n in self._list_nutorition_name:
            self._nutorition_sum_n[n] = xsum(
                self._menu_name_nutorition_name_map_val[s, n]*self._x_s[s] for s in self._list_menu_name)

            self._model += self._nutorition_sum_n[n] - \
                self._nutorition_name_map_require_amount[n] <= self._z_n[n] * \
                self._nutorition_name_map_require_amount[n]
            self._model += self._nutorition_name_map_require_amount[n] - \
                self._nutorition_sum_n[n] <= self._z_n[n] * \
                self._nutorition_name_map_require_amount[n]

        # preference constraint
        for s in self._list_menu_name:
            assert not (s in self._list_include and s in self._list_exclude)
            if s in self._list_include:
                self._model += self._x_s[s] == 1
            if s in self._list_exclude:
                self._model += self._x_s[s] == 0

    def add_objective(self):
        self._model += xsum(self._z_n[n] for n in self._list_nutorition_name)

    def optimize(self):
        self._model.optimize()

    def get_result(self):
        list_selected_menu_name = [
            s for s in self._list_menu_name if self._x_s[s].x >= 0.5]

        nutorition_name_map_amount = {
            n: self._nutorition_sum_n[n].x for n in self._list_nutorition_name}

        total_cost = sum(
            self._menu_name_map_menu_price[s]*self._x_s[s].x for s in self._list_menu_name)

        return OptimizeOutputData(
            list_selected_menu_name=list_selected_menu_name,
            nutorition_name_map_amount=nutorition_name_map_amount,
            total_cost=total_cost
        )
