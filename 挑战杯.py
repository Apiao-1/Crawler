#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:10:38 2017

@author: a_piao
"""
import requests
from lxml import etree

"""
模拟登陆
"""
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'}
postUrl = 'http://2017.tiaozhanbei.net/d37/accounts/login/'
r = requests.get(postUrl,headers = agent)
dataStr = r.text
data = etree.HTML(dataStr)
#获取csrf值并由此构造cookie
csrf = list(set(data.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
cookies = 'csrftoken='+csrf + '; __utma=267190673.1958060066.1507020351.1507020351.1507530196.2; __utmz=267190673.1507020351.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);tzb_session=qgade9dq9wjsv5xc91ijp10kepnvy5rz'
#构造请求头
headers = {
        'Host': '2017.tiaozhanbei.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding' : 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length' : '96',        
        'Connection' : 'Keep-Alive',
        'Referer': 'http://2017.tiaozhanbei.net/d37/accounts/login/',
        'cookie' : cookies,
        'Upgrade-Insecure-Requests' : '1',
        }
session = requests.session()
postData = {
        'csrfmiddlewaretoken' : csrf,
        'username' : '2017zwh01',
        'password' : '205028045',
        'next' : '',
        }
loginPage = session.post(postUrl, data = postData, headers = headers) 
#loginCode = loginPage.text
print (loginPage.status_code)#显示200说明连接成功

'''
#登陆成功后继续解析页面
'''
url = 'http://2017.tiaozhanbei.net/m139/matchflow/pendding_projects/58468/?page=2'
corehtml = session.get(url,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'})
#print (corehtml.request.headers)#确认头信息
data = corehtml.text
print (data)
