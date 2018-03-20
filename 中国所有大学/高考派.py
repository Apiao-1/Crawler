# coding:utf-8
import re
import requests
import time
import pandas

# 获取网页内容
start=time.clock()  
name = []
z = []
headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
remove = re.compile('<a href="|">|</a>|（|）')
remove1 = re.compile('<a href="|" target="_blank" class="a1">进入官网</a>|<div class="website">|\n|\t|\r')
remove2 = re.compile('<label>所处城市：</label>[\S\s]*?|</li>|\s')
remove3 = re.compile('<li class="biItem"> <span class="t">学校类型</span>[\S\s]*?<div class="c">|</div>')
remove4 = re.compile('<div class="st">|\s|<img src=".*?" alt="|" title=".*?" />|</div>')

for pages in range(71,80):#117
    r = requests.get('http://www.gaokaopai.com/daxue-0-0-0-1-0-0-0--p-'+str(pages)+'.html',headers=headers)
    data = r.text
    link_list =re.findall('<a href="http://www.gaokaopai.com/daxue-jianjie-\d+.html">[\u4e00-\u9fa5]+</a>|<a href="http://www.gaokaopai.com/daxue-jianjie-\d+.html">[\u4e00-\u9fa5]+（[\u4e00-\u9fa5]+）',data)
#    print(len(link_list))
#    print(link_list)
    y = []
    for url in link_list:
        y.append(re.sub(remove, '',url))
#    print (y)
    classfy =  re.compile('[\u4e00-\u9fa5]')  
    for url in y:
         z.append(re.sub(classfy, '',url))
    for url in y:
         name.append(re.findall(classfy,url))
    count = 0
    while count < len(name):
        name[count] = ''.join(name[count])
        count += 1
#    print (name)
#    print (z)


#    time.sleep(1)
    x = []
    city = []
    species = []
    level = []
    for url in z:
        r = requests.get(url)
    #   print (chardet.detect(r.content))
#        r.encoding = chardet.detect(r.content)['encoding']
    #    r.encoding = 'gb2312'
        data = r.text
#        link_list =re.findall('<a href=.*?>进入官网</a>',data)
        link_list =re.findall('<div class="website">[\S\s]*?<a href="http:[\S\s]*?>进入官网</a>',data)
        link_list1 =re.findall('<label>所处城市：</label>[\S\s]*?</li>',data)
        link_list2 =re.findall('<li class="biItem"> <span class="t">学校类型</span>[\S\s]*?</div>',data)
        link_list3 =re.findall(' <div class="st">[\S\s]*?</div>',data)

#        print (link_list)
        for url1 in link_list:
            x.append(re.sub(remove1, '',url1))
        for url1 in link_list1:
            city.append(re.sub(remove2, '',url1))
        for url1 in link_list2:
            species.append(re.sub(remove3, '',url1))
        for url1 in link_list3:
            level.append(re.sub(remove4, '',url1))


#city = city[:1]
#species = species[:1]
#level = level[:1]
#name = name[:1]

#city = city[:1]+city[2:]
#species = species[:1]+species[2:]
#level = level[:1]+level[2:]
#name = name[:1]+name[2:]

#x.insert(6,'http://www.ouhk.edu.hk/wcsprd/Satellite?pagename=OUHK/tcSubWeb&l=C_OPQA&lid=1385179982300&c=C_OPQA&cid=1385179982324&lang=sim&mid=0')
#x.insert(1,'http://www51.polyu.edu.hk/eprospectus/')
#x.insert(2,'http://ar.hkbu.edu.hk/pros/admiss_schemes/mainland/')
#x.insert(3,'http://www.ln.edu.hk/')


print (len(x))
print (len(city))
print (len(name))
print (len(species))
print (len(level))
#print (level)
#print (species)
#print (name)
#print (x)
#print (city)

#a = {'学校名':name,'首页网址':x,'所在地':city,'种类':species,'荣誉':level}
#df = pd.DataFrame.from_dict(a, orient='index')
#df.transpose()

data = pandas.DataFrame({'学校名':name,'首页网址':x,'所在地':city,'种类':species,'荣誉':level})
#print (data)
data.to_csv("college8.1.csv",index=False)
print ("Success")
end=time.clock()  
print('Runing time.%s Seconds'%(end-start))  