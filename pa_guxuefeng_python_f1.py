# encoding: utf-8
import urllib2,requests
from bs4 import BeautifulSoup
import os
def download(url): # 没有伪装的下载器
    print("Downloading: %s" % url)
    try:
        result = urllib2.request.urlopen(url, timeout=2).read()
    except urllib2.error.URLError as e:
        print("Downloading Error:", e.reason)
        result = None
    return result

def download_browser(url, headers): # 带浏览器伪装的下载器
    opener = urllib2.build_opener()
    opener.addheaders = headers
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
    data = tree.find('div', class_='x-sidebar-left-content').find_all('a')
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
    i+= 1
    url=root + item
    html=download_browser(url, headers) # 下载页面html
    result=bs_parser_content(html) # 解析html，获取数据
    # if i==5:
    #     break
# 合成文本文件路径
    fileName=str(i)+ '_' +title.replace(r'/',' ') +'.txt'
    fileName= os.path.join('Results/', fileName)
    print("fileName path is %s:" %fileName)
# 将数据写入到文本文件
    with open(fileName,'w') as f:
        f.write(result.encode('utf-8').strip())