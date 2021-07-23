#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests, json
import pandas as pd

# 設定 Header 
headers = {
    "Accept": "*/*",
    "Accept-Language": 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "DNT": "1",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "cookie": "__cfduid=d8db8ce8747b090ff3601ac6d9d22fb951579718376; _ga=GA1.2.1940993661.1579718377; _gid=GA1.2.1806075473.1579718377; _ga=GA1.3.1940993661.1579718377; _gid=GA1.3.1806075473.1579718377",
    "Content-Type":"application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36",
}

def main():
    r = requests.get("https://anime1.me/", headers = headers)
    soup = BeautifulSoup(r.text, 'lxml') 
    ele_tb = soup.find('tbody')
    ele_tr = ele_tb.find_all('tr')
    for anime in ele_tr:
        ani_name = anime.find('a').text
        data = {
            '動畫名稱': ani_name,
            'ID': anime.find('a')['href'][6:],
            '集數': anime.find('td', class_='column-2').text,
            '年份': anime.find('td', class_='column-3').text, 
            '季節': anime.find('td', class_='column-4').text, 
            '字幕組': anime.find('td', class_='column-5').text
        }
        dict[ani_name] = data

if __name__ == '__main__':
    dict = {}
    main()

    # .JSON
    with open('Anime1 List.json', 'w', encoding = 'utf8') as f:
        f.write(json.dumps(dict, ensure_ascii = False, indent = 2))
        f.flush()
        f.close
    
    # .CSV
    df = pd.json_normalize(dict.values())
    df.to_csv("Anime1 List.csv", index = False)



    