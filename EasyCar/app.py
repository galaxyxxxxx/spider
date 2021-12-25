import requests
from bs4 import BeautifulSoup

# 我们想爬取的页面 的链接 的前缀
URL_PREFIX = 'https://car.yiche.com/xuanchegongju/?g=1&page='

# 用于保存结果的变量
res = ''

# 对55页数据 依次爬取
for index in range(1, 55):

    # 每一页的url； 前缀加上页号
    url = URL_PREFIX + str(index)

    # 基于requests包 模拟网络请求
    # (类似于你在浏览器里输入url 服务器会返回给你信息 浏览器把信息展示在界面上)
    # (这里只是没有可视化展现出来 而是保存下来服务器返回的信息；这些信息里就有我们要的数据)
    s = requests.get(url)

    # 基于BeautifulSoup 将拿到的服务器发回的信息 转换成html格式
    soup = BeautifulSoup(s.content, "html.parser")

    # 对刚刚转换好的html 进行标签查找
    # 因为网页上车型的名称 在class=’cx-name‘的标签里 因此我们获取所有对应数据 存到names里
    names = soup.findAll("p", {"class": "cx-name"})

    # 此时names里存了当前页面所有车型的名称 我们一一取出 添加到第8行定义好的结果里
    for name in names:
        res += (name.string + ';')

# 结束循环后 我们拿到了55页数据 存在res里
# 此时我们把它打印到控制台里 即可查看到结果
print(res)
