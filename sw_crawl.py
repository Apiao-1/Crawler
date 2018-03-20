import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import chardet

num = "hdu6059"
headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
r = requests.get('https://www.baidu.com/s?wd='+num, headers=headers)
r.encoding = chardet.detect(r.content)['encoding']
data_str = r.text
data = etree.HTML(data_str)
urls = data.xpath('.//*[@class="result c-container "]/h3/a//@href')
remove = re.compile('\[\\u4e00-\\u9fa5\]+')#清洗数据
# file = open('sw.txt','w')
for url in urls:
	r = requests.get(url, headers=headers)
	r.encoding = chardet.detect(r.content)['encoding']
	data_str = r.text
	link_list =re.findall('题意[\S\s]*?<p>[\S\s]*?</p>' ,data_str)
	result = re.findall('[\u4e00-\u9fa5].*?' ,str(link_list))
	print (	''.join(result))
	# for i in result:
 #   		file.write(i)
	# print ("result")


