import streamlit as st
from problem import MenuProblem
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('menu.csv')

# 　一食の栄養必要量を入れた辞書
require_dic = {
    'energy': 2650 / 3,
    'protein': 65 / 3,
    'fat': 60 / 3,
    'carbohydrates': 300 / 3,
    'salt': 7.5 / 3,  # 以下
    'calcium': 800 / 3,
    'vegetable': 350 / 3  # 以上
}

# タイトル
st.title('学食の献立最適化')
# 純粋なテキスト
max_price = st.number_input('予算を教えてください', 100, 2000, 500, step=50)
T_plus = st.multiselect("食べたい商品を選択", df['name'])
T_minus = st.multiselect("食べたくない商品を選択", df['name'])


if st.button('献立を作成'):
    problem = MenuProblem(df, max_price, T_plus, T_minus, require_dic)
    solution_df = problem.solve()

    st.subheader(f"合計金額 : {solution_df['price'].sum():.0f}円")

    df_show = solution_df.drop('img_url', axis=1)
    df_show.loc['合計'] = df_show.sum(numeric_only=True)
    df_show['name']['合計'] = ""
    df_show.loc['目標量'] = df_show.loc['合計']
    df_show['price']['目標量'] = max_price
    for k, v in require_dic.items():
        df_show[k]['目標量'] = v

    st.dataframe(df_show)

    for i in range(len(solution_df)):
        if i % 3 == 0:
            cols = st.columns(3)
        with cols[i % 3]:
            img_url = solution_df['img_url'].iloc[i]
            st.text(solution_df['name'].iloc[i])
            st.image(img_url, use_column_width=True)
