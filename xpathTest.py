import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import chardet
import tldextract

r = requests.get('http://www.fudan.edu.cn/2016/../2016/channels/view/59')
r.encoding = chardet.detect(r.content)['encoding']
data_str = r.text
data = etree.HTML(data_str)
links = data.xpath('.//@href')

# soup = BeautifulSoup(data_str,'html.parser',from_encoding = 'utf-8')
# links = soup.find_all(href = re.compile("fudan.edu.cn"))#查找href属性中含有“elsie”的tag

# links = soup.select('a[href*="fudan.edu.cn"]')
links = filter(lambda x:x !='' and x !='#' and x !='javascript:;',links)
links = list(links)
href = set()
for link in links:#去重操作
	href.add(link)
href_str = str(href)
remove = re.compile("\'")
print (len(href))
print (href)

#获取相对地址
relative_url = []
x = re.sub('\'http:.*?\'', '', href_str)
y = re.findall('\'.*?\'' ,x)
for url in y:
	url = re.sub(remove, '', url)
	if url[:3] == '../':
		url ='http://www.fudan.edu.cn/2016/'+url
	elif url[:1] =='/':
		url ='http://www.fudan.edu.cn'+url
	else:
		url ='http://www.fudan.edu.cn/2016/'+url
	relative_url.append(url)
	
print (len(relative_url))
print (relative_url)

#获取绝对地址
trans =re.findall('\'http:.*?\'' ,href_str)
absolute_url = []
http_url = []
for url in trans:
    http_url.append(re.sub(remove, '', url))
for url in http_url:
	ext = tldextract.extract(url)
	if '.'.join(ext[1:3]) == 'fudan.edu.cn':
		absolute_url.append(url)
print (len(absolute_url))
print (absolute_url)
