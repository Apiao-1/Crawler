# coding:utf-8
import re
import requests
import chardet

import pandas

#获取所有大学所在地域的一级链接
x = []
y = []
z = []
name = []
r = requests.get('http://www.hao123.com/edu/')
data = r.text
#link_list =re.findall('http://www.hao123.com/eduhtm/.*?[^d]\b.htm' ,data)——错误
#link_list = re.findall('http://www.hao123.com/eduhtm/[^\d]+.htm' ,data)
link_list = re.findall('http://www.hao123.com/eduhtm/.*?04.htm' ,data)
#link_list = link_list[:-1]
#print (len(link_list))
#print (link_list)

#一级链接跳转获取每个大学的首页及名称
remove = re.compile('<a href="|</a></p></td>|">')
for url in link_list:
    r = requests.get(url)
#   print (chardet.detect(r.content))
    r.encoding = chardet.detect(r.content)['encoding']
#    r.encoding = 'gb2312'
    data = r.text
    link_list =re.findall('<a href=".*?</a></p></td>',data)
#    print(link_list)
    for url in link_list:
        y.append(re.sub(remove, '',url))
#print(len(set(y)))

classfy =  re.compile('[\u4e00-\u9fa5]|（|）')  
for url in y:
     z.append(re.sub(classfy, '',url))
for url in y:
     name.append(re.findall(classfy,url))
count = 0
while count < len(name):
    name[count] = ''.join(name[count])
    count += 1
#print (name)
data = pandas.DataFrame({'学校名':name,'首页网址':z})
#print (data)
data.to_csv("college3.csv",index=False)
#csvFile = open('college.csv','w') # 设置newline，否则两行之间会空一行
#writer = csv.writer(csvFile)
#writer.writerow(z)
#csvFile.close()
print ("Success")