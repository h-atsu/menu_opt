import pandas as pd
import pulp


class MenuProblem():
    """学生の乗車グループ分け問題を解くクラス"""

    def __init__(self, menu_df, max_price, T_plus, T_minus, require_dic, name='MenuProblem'):
        # 初期化メソッド
        self.menu_df = menu_df
        self.max_price = max_price
        self.T_plus = T_plus
        self.T_minus = T_minus
        self.require_dic = require_dic
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        # 栄養素のリスト
        nutrition_list = ['energy', 'protein', 'fat',
                          'carbohydrates', 'salt', 'calcium', 'vegetable']
        # 商品集合
        S = list(range(len(self.menu_df)))
        #
        S_to_name = self.menu_df['name'].to_dict()
        name_to_S = {v: k for k, v in S_to_name.items()}

        # 問題インスタンス
        problem = pulp.LpProblem(self.name, pulp.LpMinimize)
        # 決定変数
        xs = pulp.LpVariable.dicts('x', S, 0, 1, 'Integer')
        # スラック変数
        zs = pulp.LpVariable.dict(
            'z', nutrition_list, lowBound=0, cat='Continuous')

        # 問題定義 #####################3
        # 目的関数　slack変数z
        problem += pulp.lpSum(zs)

        # 制約式
        # 好き嫌い制約
        for val in self.T_plus:
            problem += xs[name_to_S[val]] == 1
        for val in self.T_minus:
            problem += xs[name_to_S[val]] == 0

        # 金額制約
        problem += pulp.lpSum(self.menu_df['price'][i] * xs[s]
                              for i, s in enumerate(S)) <= self.max_price

        # 栄養制約
        for nut in nutrition_list:
            if nut == 'salt':
                problem += pulp.lpSum(self.menu_df[nut][i] * xs[s] for i, s in enumerate(
                    S)) - self.require_dic[nut] <= zs[nut] * self.require_dic[nut]
            if nut == 'vegetable':
                problem += pulp.lpSum(self.menu_df[nut][i] * xs[s] for i, s in enumerate(
                    S)) - self.require_dic[nut] >= -zs[nut] * self.require_dic[nut]
            else:
                problem += pulp.lpSum(self.menu_df[nut][i] * xs[s] for i, s in enumerate(
                    S)) - self.require_dic[nut] <= zs[nut] * self.require_dic[nut]
                problem += pulp.lpSum(self.menu_df[nut][i] * xs[s] for i, s in enumerate(
                    S)) - self.require_dic[nut] >= -zs[nut] * self.require_dic[nut]

        return {'problem': problem, 'variable': {'xs': xs, 'zs': zs}, 'list': {'S': S}}

    def solve(self):
        # 最適化問題を解くメソッド
        # 問題を解く
        status = self.prob['problem'].solve()

        # 最適化結果を格納
        xs = self.prob['variable']['xs']
        zs = self.prob['variable']['zs']
        S = self.prob['list']['S']

        solution_df = self.menu_df.iloc[[
            i for i, v in enumerate(xs.values()) if v.value() == 1]]

        return solution_df
