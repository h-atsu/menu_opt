from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import re


def del_str(S):
    for i, c in enumerate(S):
        if ord('A') <= ord(c) <= ord('z'):
            return S[:i]
    return S


def get_data(url, save_path):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)
    toggle_titles = driver.find_elements(By.CLASS_NAME, "toggleTitle")
    toggle_titles_sub = driver.find_elements(By.CLASS_NAME, "open")

    for v in reversed(toggle_titles):
        if v in toggle_titles_sub:
            continue
        v.click()
    time.sleep(5)
    html = driver.page_source.encode("utf-8")  # HTMLのエンコード
    bsObj = BeautifulSoup(html, "html.parser")

    driver.close()
    driver.quit()

    cont = bsObj.find(class_='area')
    all_menu_links = cont.find_all('a')

    base_url = 'https://west2-univ.jp/sp/'

    columns = ['price', 'energy', 'protein', 'fat',
               'carbohydrates', 'salt', 'calcium', 'vegetable']

    menu_data = []

    for link in all_menu_links:
        time.sleep(0.5)
        print(base_url + link.get('href'))
        menu_page = requests.get(base_url + link.get('href'))
        menu_soup = BeautifulSoup(
            menu_page.text, 'html.parser').find(id='main')
        menu_name = menu_soup.find('h1')
        menu_detail = menu_soup.find(class_="detail")
        menu_detail_list = menu_detail.find_all("li")

        # 各栄養素を記入
        menu_dic = {'name': menu_name.text}
        for i, col in enumerate(columns):
            menu_dic[f'{col}'] = menu_detail_list[i].find(
                'span', class_='price').text
        # menu画像のurl
        menu_dic['img_url'] = menu_soup.find('img')['src']

        menu_data.append(menu_dic)

    def fi(i):
        return lambda x: x[:-i]
    # def f2(x): return float(x[:-2])
    # def f4(x): return float(x[:-4])

    # data frame operations
    df = pd.DataFrame(menu_data)
    df['name'] = df['name'].map(del_str)
    print(len(df))
    # 単位を削除
    df['price'] = df['price'].map(fi(1))
    df['energy'] = df['energy'].map(fi(4))
    df['protein'] = df['protein'].map(fi(1))
    df['fat'] = df['fat'].map(fi(1))
    df['carbohydrates'] = df['carbohydrates'].map(fi(1))
    df['salt'] = df['salt'].map(fi(1))
    df['calcium'] = df['calcium'].map(fi(2))
    df['vegetable'] = df['vegetable'].map(fi(1))

    # 数値変換
    cols = ['price', 'energy', 'protein', 'fat',
            'carbohydrates', 'salt', 'calcium', 'vegetable']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    df = df.dropna()

    df.to_csv(save_path, index=False)
    print(f"menu size is {len(df)}")


if __name__ == '__main__':
    cafeteria_dict = {
        'rainbow': 'https://west2-univ.jp/sp/menu.php?t=663251',
        'kansita': 'https://west2-univ.jp/sp/menu.php?t=663252',
        'famille': 'https://west2-univ.jp/sp/menu.php?t=663255',
        'kasane': 'https://west2-univ.jp/sp/menu.php?t=663258',
    }

    for k, v in cafeteria_dict.items():
        print(f'===== {k} scraping start =====')
        get_data(v, 'data/' + k + '.csv')
        print('===== finish =====')
