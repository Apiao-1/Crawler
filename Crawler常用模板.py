import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import chardet

'''
爬虫解析页面三种方法
'''
#请求头设置
headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#正则表达式
r = requests.get('http://www.gaokaopai.com/daxue-0-0-0-0-0-0-0--p-'+str(pages)+'.html',headers=headers)
data_str = r.text
link_list =re.findall('<a href="http://www.gaokaopai.com/daxue-jianjie-\d+.html">[\u4e00-\u9fa5]+</a>' ,data_str)
remove = re.compile('<a href="|">|</a>')#清洗数据
y = []
for url in link_list:@
    y.append(re.sub(remove, '',url))

#lxml的xpath解析
r = requests.get('http://www.gaokaopai.com/daxue-0-0-0-0-0-0-0--p-'+str(pages)+'.html',headers=headers)
data_str = r.text
data = etree.HTML(data_str)
href = data.xpath('.//@href')[0].enconde('utf-8')#编码可加可不加
title = data.xpath('.//@title')[0]

#BeautifulSoup解析-find_all()方法搜索文档树
r = requests.get('http://www.fudan.edu.cn/2016/index.html')
r.encoding = chardet.detect(r.content)['encoding']#页面编码
data_str = r.text
soup = BeautifulSoup(data_str,'html.parser',from_encoding = 'utf-8')
print (soup.find_all('b'))#查找文档中的所有<b>标签
print (soup.find_all(["a", "b"]))#查找文档中的所有<a>和<b>标签
for tag in soup.find_all(re.compile("^b")):
	print (tag.name)#查找文档中的所有以字母b开头的标签
print (soup.find_all(href = re.compile("elsie")))#查找href属性中含有“elsie”的tag
print (soup.find_all(href = re.compile("elsie")， id = 'link1'))#可指定多个参数过滤
#text参数和recursive参数见P121

#BeautifulSoup解析中——css选择器法
r = requests.get('http://www.fudan.edu.cn/2016/index.html')
r.encoding = chardet.detect(r.content)['encoding']#页面编码
data_str = r.text
soup = BeautifulSoup(data_str,'html.parser',from_encoding = 'utf-8')
links = soup.select('a[href*="fudan.edu.cn"]')
new_url = set()#去重操作
for link in links:
	new_url.add(link['href'])

#解决页面编码问题
r = requests.get('http://www.fudan.edu.cn/2016/index.html')
r.encoding = chardet.detect(r.content)['encoding']
data_str = r.text