from bs4 import BeautifulSoup
import requests
# import urllib.request as requests
import os
from io import BytesIO

def GetPixivAuthorThumbnail(SauceNaoResult):

    url = SauceNaoResult[0].urls[0]

    # 確認圖片網址
    print(url)

    html = requests.get(url=url)
    html.encoding = "utf-8"

    soup = BeautifulSoup(html.text,"html.parser")

    print(soup)

    # 開始搜尋作者頭貼
    results = soup.find_all("img")
    # print(results)
    # 取得圖片來源連結
    image_links = [result.get("src") for result in results]
    print(image_links)

def GetWebsitePic(url):
    return requests.get(url)