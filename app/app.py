import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import os
import requests
import json

BACKEND_HOST = os.environ.get('BACKEND_HOST', '127.0.0.1:8000')

image = Image.open('asset/icon.png')
st.set_page_config(
    page_title="Menu Opt",
    page_icon=image,
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://www.google.com",
        'About': """
         # 学食献立最適化
         整数計画問題を解いて栄養バランスを考慮した献立を提案します
         """
    })


# タイトル
st.title('学食の献立最適化')

list_cafe_name = ['図書館下食堂', 'かさね', 'レインボー', 'ファミール']
cafe_name_map_file_name = {
    '図書館下食堂': 'kansita.csv',
    'かさね': 'kasane.csv',
    'レインボー': 'rainbow.csv',
    'ファミール': 'famille.csv'
}

cafe_name = st.selectbox(
    label="食堂を選んでください", options=list_cafe_name)
cafe_file_name = cafe_name_map_file_name[cafe_name]
df = pd.read_csv('../data/' + cafe_file_name)

# 予算と好き嫌いリストを入力
max_budget = st.number_input('予算を教えてください', 100, 2000, 500, step=50)
list_include = st.multiselect("食べたい商品を選択", df['name'])
list_exclude = st.multiselect("食べたくない商品を選択", df['name'])

if st.button('献立を作成'):
    url = f'http://{BACKEND_HOST}/optimize'
    data = {
        'cafe_file_name': cafe_file_name,
        'max_budget': max_budget,
        'list_include': list_include,
        'list_exclude': list_exclude
    }

    ret = requests.post(url, data=json.dumps(data)).json()
    list_menu_data = ret['list_selected_menu_data']
    nutorition_name_map_amount = ret['nutorition_name_map_amount']
    total_cost = ret['total_cost']

    df_menu = pd.DataFrame(list_menu_data)

    st.dataframe(df_menu.iloc[:, :-1])

    for i, row in enumerate(df_menu.itertuples()):
        if i % 3 == 0:
            cols = st.columns(3)
        with cols[i % 3]:
            img_url = row.img_url
            st.text(row.name)
            st.image(img_url, use_column_width=True)
