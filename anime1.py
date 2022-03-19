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
    # r = requests.get("https://anime1.me/", headers = headers)
    r = requests.get("https://d1zquzjgwo9yb.cloudfront.net")
    ani_cloudfront = json.loads(r.text)

    for i in range(len(ani_cloudfront)):
        ani_name = ani_cloudfront[i][1]
        data = {
            '動畫名稱': ani_cloudfront[i][1],
            'ID': ani_cloudfront[i][0],
            '集數': ani_cloudfront[i][2],
            '年份': ani_cloudfront[i][3], 
            '季節': ani_cloudfront[i][4], 
            '字幕組': ani_cloudfront[i][5]
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



    
