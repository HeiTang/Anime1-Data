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
    r = requests.get("https://anime1.me/animelist.json", headers = headers)
    r.raise_for_status()
    anime_list = json.loads(r.text)

    for i in range(len(anime_list)):
        anime_id = anime_list[i][0]
        anime_name = anime_list[i][1]

        # ID 為 0 代表 anime1.pw 條目，名稱欄位存的是 <a> 標籤，
        # 且其 cat 編號會與 anime1.me 的 ID 撞號，故加上前綴區隔
        if anime_id:
            key = anime_id
        else:
            link = BeautifulSoup(anime_name, 'html.parser').a
            anime_name = link.text
            key = f"pw{link['href'].split('cat=')[1]}"

        data = {
            '動畫名稱': anime_name,
            'ID': anime_id,
            '集數': anime_list[i][2],
            '年份': anime_list[i][3], 
            '季節': anime_list[i][4], 
            '字幕組': anime_list[i][5]
        }
        dict[key] = data

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



    
