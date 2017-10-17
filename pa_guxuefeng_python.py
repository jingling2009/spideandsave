# encoding: utf-8
import urllib2,requests   #引入库名字需要写对，如果不确定，就可以到自己的python安装包里去确认#下，python安装包地址：C:\Python27\Lib\site-packages 如：C:\Python27\Lib\site-packages\bs4
from bs4 import BeautifulSoup
import os
#需要pip install urllib2,requests,beautifulsoup4,lxml  ……windows可以使用pip list查看当前装了哪些库
def download(url): # 没有伪装的下载器
    print("Downloading: %s" % url)
    try:
        result = urllib2.request.urlopen(url, timeout=2).read()
    except urllib.error.URLError as e:
        print("Downloading Error:", e.reason)
        result = None
    return result

def download_browser(url, headers): # 带浏览器伪装的下载器
    opener = urllib2.build_opener() #伪装浏览器
    opener.addheaders = headers #伪装浏览器header
    print("Downloading: %s" % url)
    try:
        result = opener.open(url, timeout=2)
        result = result.read()
        print("Download OK!")
    except urllib2.request.URLError as e:
        print("Downloading error:", e.reason)
        result = None
    return result

# 解析首页，获取url
def bs_parser(html):
    tree = BeautifulSoup(html, 'lxml')
#使用的lxml方式读取，所以需要安装lxml语言里和XML以及HTML工作的功能最丰富和最容易使用库

    data = tree.find('div', class_='x-sidebar-left-content').find_all('a')  #这个结构需要到具体需要爬取的网页#里去自己找。
    print(data[0].attrs['href'])
    urls = []
    titles = []
    grades = []
    for item in data:
        urls.append(item.attrs['href'])
        titles.append(item.get_text())
    return urls, titles

# 解析页面内容
def bs_parser_content(html):
    tree = BeautifulSoup(html, 'lxml')
    data = tree.find('div', class_='x-wiki-content')
    # print(data)
    result = data.get_text()
    return result

# 首页url
url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
root = 'http://www.liaoxuefeng.com'

# header一定是一个元组列表
headers = [
    ('Connection', 'Keep-Alive'),
    ('Accept', 'text/html, application/xhtml+xml, */*'),
    ('Accept-Language', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3'),
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
]
html = download_browser(url, headers) # 下载首页的HTML
urls, titles = bs_parser(html) # 解析首页的HTML，返回URL和标题
i = 0
for item,title in zip(urls, titles):
    if i==5:
        break
    i+= 1
    url=root + item
    html=download_browser(url, headers) # 下载页面html
    result=bs_parser_content(html) # 解析html，获取数据
# 合成文本文件路径
    fileName=str(i)+ '_' +title.replace(r'/',' ') +'.txt'
    fileName= os.path.join('Results/', fileName)
    print("fileName path is %s:" %fileName)
# 将数据写入到文本文件
    with open(fileName,'w') as f:
        f.write(result.encode('utf-8').strip())
