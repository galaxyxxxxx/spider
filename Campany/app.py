# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlrd

URL_PREFIX = 'https://www.tianyancha.com/search?key='


def read_excel():
  data = xlrd.open('data.xlsx')
  sheet = data.sheet_by_index(3)
  
  for i in range(sheet.nrows):
    row = sheet.row_values(i) 
    name_cn = row[0] #get campany chinese name
    name_en = get_name_en(name_cn)
  
def get_name_en(name_cn):
  