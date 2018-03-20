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
result = []
r = requests.get('http://www.unjs.com/')
data = r.text
link_list = re.findall('<a Class="daxueright".*?http://www.unjs.com/daxue/.*?/' ,data)
#print (len(link_list))
#print (link_list)
remove = re.compile('<a Class="daxueright" href=\'')
for url in link_list:
     y.append(re.sub(remove, '',url))
#print (y)

#一级链接跳转获取每个大学的首页及名称
remove = re.compile('<td class="tdbg_title"><a href=\'|\' target=_blank><h4>|</h4></a></td>')
for url in y:
    r = requests.get(url)
#   print (chardet.detect(r.content))
    r.encoding = chardet.detect(r.content)['encoding']
#    r.encoding = 'gb2312'
    data = r.text
    link_list = re.findall('<td class="tdbg_title"><a href=\'.*?\' target=_blank><h4>.*?</h4></a></td> ' ,data)
#    print(link_list)
    for url in link_list:
        z.append(re.sub(remove, '',url))
#print (z)

classfy =  re.compile('[\u4e00-\u9fa5]')  
for url in z:
     result.append(re.sub(classfy, '',url))
for url in z:
     name.append(re.findall(classfy,url))
count = 0
while count < len(name):
    name[count] = ''.join(name[count])
    count += 1
print (len(name))
#print (result)
#for url in result:
#    r = requests.get(url)
#data = pandas.DataFrame({'学校名':name,'首页网址':z})

#data.to_csv("college3.csv",index=False)
##csvFile = open('college.csv','w') # 设置newline，否则两行之间会空一行
##writer = csv.writer(csvFile)
##writer.writerow(z)
##csvFile.close()
#print ("Success")