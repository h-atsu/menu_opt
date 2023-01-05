from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import re

driver = webdriver.Chrome()
driver.get('https://west2-univ.jp/sp/menu.php?t=663255')

time.sleep(0.5)
toggle_titles = driver.find_elements(By.CLASS_NAME, "toggleTitle")
toggle_titles_sub = driver.find_elements(By.CLASS_NAME, "open")

print(toggle_titles)
print(toggle_titles_sub)

for v in reversed(toggle_titles):
    if v in toggle_titles_sub:
        continue
    v.click()

time.sleep(0.5)

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
    menu_soup = BeautifulSoup(menu_page.text, 'html.parser').find(id='main')
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

# data frame operations

df = pd.DataFrame(menu_data)


def del_str(S):
    for i, c in enumerate(S):
        if ord('A') <= ord(c) <= ord('z'):
            return S[:i]
    return S


def f1(x): return float(x[:-1])
def f2(x): return float(x[:-2])
def f4(x): return float(x[:-4])


df['name'] = df['name'].map(del_str)
df['price'] = df['price'].map(f1)
df['energy'] = df['energy'].map(f4)
df['protein'] = df['protein'].map(f1)
df['fat'] = df['fat'].map(f1)
df['carbohydrates'] = df['carbohydrates'].map(f1)
df['salt'] = df['salt'].map(f1)
df['calcium'] = df['calcium'].map(f2)
df['vegetable'] = df['vegetable'].map(f1)

df.to_csv('menu.csv', index=False)
