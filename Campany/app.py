# -*- coding: utf-8 -*-
from time import sleep
import requests
from bs4 import BeautifulSoup
import xlrd

URL_ID_PREFIX = 'https://www.tianyancha.com/search/ola1?key='
URL = 'https://www.tianyancha.com/company/'

class Spider():

  def __init__(self, url):

    self.url = url

    # 请求头
    self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Cookie": "aliyungf_tc=ecd5a1a6258583bcd7a9103a342a90ecd6a4d6e417416cee8d32fc22ea0b158b; csrfToken=Pcx284mJr97p1z7nXkNStdF8; TYCID=5cacb2a0666311ecbd56b3f1629e32d6; ssuid=1272995846; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1640533752; _gid=GA1.2.1916516821.1640533752; _ga=GA1.2.1258158379.1640533752; _bl_uid=wIkLkxyen0wfqyi8a0CnfIe1es42; RTYCID=10029018432546da8ad8993d25c5c432; CT_TYCID=f3ea6174bd87480eb8bda0c5ace3018e; creditGuide=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218801035020%22%2C%22first_id%22%3A%2217df76e7390f43-0add5bdeced20f-4303066-2621440-17df76e739110e1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217df76e7390f43-0add5bdeced20f-4303066-2621440-17df76e739110e1%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2218801035020%22}; tyc-user-info-save-time=1640536325154; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgwMTAzNTAyMCIsImlhdCI6MTY0MDUzNjMyNCwiZXhwIjoxNjcyMDcyMzI0fQ.kRTAk14LeTiST_F0a8EALGafvi2kBZWmzTo8Iq1Zqs_-6Z1w_vdV5WIa6sBuWDrZQtK8T8KuMROEO14R1zvJOA; tyc-user-phone=%255B%252218801035020%2522%255D; searchV6CompanyResultCid=15632220; searchV6CompanyResultCid.sig=zVzDeKM8xP10ww8kasoKEeKRwAAFRCOUbAtjSQH-9CU; searchV6CompanyResultName=%E5%8D%8E%E9%83%BD%E9%85%92%E4%B8%9A; searchV6CompanyResultName.sig=TfpxBV-lqUg_uk7--pmVzixHNHKuXGG-Hl0MDXm3Y0M; cloud_token=db6fc194ca0d4b668dba268491c90f45; searchSessionId=1640540689.01997150; relatedHumanSearchGraphId=2342298832; relatedHumanSearchGraphId.sig=e5LNurm60IFxQUYRpTkRTzIxHXIIl3OmjoDokNejBdI; acw_tc=707c9f6316405414708283194e450268c083aeb6cd83c2da49c2ba040c4703; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1640541484",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
    }

    self.item_list = {} # 存储队列


  def read_excel(self):
    data = xlrd.open_workbook('data.xlsx')
    sheet = data.sheet_by_index(3)

    

    for i in range(sheet.nrows):
      row = sheet.row_values(i) 
      name_cn = row[0] #get campany chinese name
      name_en = self.get_name_en(name_cn)

      res_txt = open('res.txt','a+')
      res_txt.write(name_en + '\n')
      res_txt.close()

      sleep(1)
    
    
    return 0

  def get_id(self, name_cn):
    s = requests.get(url = self.url + name_cn, headers =self.headers)
    soup = BeautifulSoup(s.content, 'html.parser')

    campany = soup.find(class_='search-result-single')
    id = campany['data-id']
    return id

  def format(self, text):
    
    str = text.title() #首字母大写
    suffix = [',Ltd',',Ltd.'] #检查后缀
    if str.endswith(suffix[0]) or str.endswith(suffix[1]):
      str_arr = str.split(' ')
      str_arr.pop()
      str_arr.append('Co., Ltd.')
      str=' '.join(str_arr)
    
    return str
  
  def get_name_en(self,name_cn):
    id = self.get_id(name_cn)
    s = requests.get(url = URL + id, headers =self.headers)
    soup = BeautifulSoup(s.content, 'html.parser')

    name_wrapper = soup.find(class_='_englishname')
    if name_wrapper:
      name_en_raw = name_wrapper.get_text()
      name_en = self.format(name_en_raw)
      # print(name_en)
      return name_en
    else:
      res = name_cn + '获取英文名失败 请尝试访问链接：' + URL + id
      # print(res)
      return id

  

if __name__ == '__main__':
  spider = Spider(URL_ID_PREFIX)
  spider.read_excel()