# -*- coding: utf-8 -*-
import json
from os import times
from sqlite3 import Timestamp
from typing import List
from urllib import response
from bs4 import BeautifulSoup
import requests
import re
import time


def getHTML(url: str):
    """获取url对应的HTML结构
    """
    response = requests.get(url)
    html = response.content.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def getHrefs() -> List[str]:
    """获取第一个网址的每篇文章链接
    """
    url = 'https://www.understandingwar.org/backgrounder/ukraine-conflict-updates'
    soup = getHTML(url)
    # 找到所有包裹文章链接的a标签
    hrefs_wrapper = soup.find_all(
        href=re.compile('^https://isw.pub/RusCampaign'))
    hrefs = []
    for item in hrefs_wrapper:
        hrefs.append(item.get('href'))
    hrefs_length = removeDuplicates(hrefs)  # 去重
    return hrefs[:hrefs_length]


def getHrefs2() -> List[str]:
    url_prefix = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&start='
    url_suffix = '&cselibv=3e1664f444e6eb06&cx=006703778745328820552:rmncc-_xykg&q=ukraine-conflict-updates&safe=off&cse_tok=AJvRUv0SF3-ShzTvjQjKaq5H-aNR:1651494728609&sort=&exp=csqr,cc,4742719&callback=info'
    urls_nums = 405
    for index in range(1, 2):
        url = url_prefix + str(index) + url_suffix
        response = requests.get(url)
        data = response.json()
        print(data)


def removeDuplicates(arr: List[str]) -> int:
    """数组原地去重
    :param arr 待去重数组
    """
    if len(arr) == 0:
        return 0
    slow_p: int = 0
    for fast_p in range(1, len(arr)):
        if arr[slow_p] != arr[fast_p]:
            slow_p += 1
            arr[slow_p] = arr[fast_p]
    return slow_p + 1


def getArticle(href: str):
    # href = 'https://isw.pub/RusCampaignApr30'
    soup = getHTML(href)

    title = soup.find(id='page-title').string
    type = '报告'

    # get text
    text = soup.select(
        '.field-name-body .field-items .field-item')[0].get_text()
    text_cleaned = cleanData(text)

    # get images
    images = []
    images_wrapper = soup.select('.field-name-body a img')
    for i in images_wrapper:
        images.append(i.get('src'))

    # get timestamp
    time = soup.select('.submitted span')[0].get(
        'content')  # 2022-04-30T18:06:52-04:00
    timestamp = getTimeStamp(time[:19])

    url = href

    res = {
        "title": title,
        "type": type,
        "text": text_cleaned,
        "images": images,
        "timestamp": timestamp,
        "url": url
    }
    # writeData(res)
    return res


def getTimeStamp(date: str) -> int:
    """根据时间文本获取时间戳
    """
    timeArray = time.strptime(date, "%Y-%m-%dT%H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def cleanData(data: str) -> str:
    """清除注释及空行
    """
    t1 = re.sub(r'\[[\d]+\][^\n]*', "", data, flags=re.S)
    # print(repr(t1))
    # t2 = re.sub(r'\\n', "", t1, re.MULTILINE)
    t2 = "".join([s for s in t1.splitlines(True) if s.strip()])
    # print(repr(t2))
    return t2


def writeData(data: dict):
    d = json.dumps(data, ensure_ascii=False)
    with open("./12_reports_UkraineConfilctUpdates_20220502.jl", mode="a+") as f:
        f.write(d)


def main():
    # urls1 = getHrefs()
    # for url in urls1:
    #     data = getArticle(url)
    #     writeData(data)
    urls2 = getHrefs2()


main()
