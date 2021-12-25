import requests
from bs4 import BeautifulSoup

prefix = 'https://car.yiche.com/web_api/car_model_api/api/v1/'
url1 = 'serial/search_hot_serials?cid=508&param=%7B%22adCigdcid%22%3A%2277ef0987d7d23057ae8e4db10a321397%26page%3DmJrtaCNwzyQAjcBzWQYSF3EKA3z8448i1638178888342%22%2C%22type%22%3A5%2C%22adTime%22%3A%222021-11-29%22%2C%22advertPage%22%3A%22mJrtaCNwzyQAjcBzWQYSF3EKA3z8448i1638178888342%22%2C%22num%22%3A20%7D'

headers = {
    'x-platform': 'pc',
    'x-sign': res,
    'x-city-id': '201',
    'x-timestamp': str(timestamp)
}

s = requests.get(url1, headers=headers)
print(res)
