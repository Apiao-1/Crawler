# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:43:48 2017

@author: 张朴平
"""

import re
import requests
import time
import pandas
from lxml import etree


#with open('专科.csv','r') as csvfile:
##    reader = csv.reader(csvfile)
##    column = [row[5] for row in reader]
#    reader = csv.DictReader(csvfile)
#    column = [row['首页网址'] for row in reader]
#print (column)

# 获取网页内容
#result = []
#name =[]
#link =[]
start=time.clock()  
headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
remove = re.compile('<TD><A href="|</A></TD>|">')
r = requests.get('http://www.360doc.com/content/12/0128/07/4310958_182232219.shtml')
data = etree.HTML(r.text)
link_list = data.xpath('.//*[@id=\'artContent\']/table/tbody/tr[.]/td[.]/a/@href')
name = data.xpath('.//*[@id=\'artContent\']/table/tbody/tr[.]/td[.]/a/text()')
print (len(link_list))
print (len(name))
name.append('')
print (link_list)
print (name)
#for url in link_list:
#    result.append(re.sub(remove, '',url))
#print (len(result))
#for url in result:
#    link.append(re.sub('[\u4e00-\u9fa5]', '',url))
#
#for url in link_list:
#    name.append(re.findall('[\u4e00-\u9fa5]',url))
#count = 0
#while count < len(name):
#    name[count] = ''.join(name[count])
#    count += 1
#print (len(name))
#
#data = pandas.DataFrame({'媒体名':name,'首页网址':link_list})
##print (data)
#data.to_csv("媒体.csv",index=False)
#print ("Success")
#end=time.clock()  
#print('Runing time.%s Seconds'%(end-start))  