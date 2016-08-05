# -*- coding:utf-8 -*-

import requests
import urllib2
import urllib
import re

PageNum = 20
title = "小说"
payload = {'start' : PageNum , 'type' : 'T'} 
TitleList = ['小说' , '外国文学']
BaseUrl = 'https://book.douban.com/tag/' + str(title)
# print BaseUrl


# request = requests.get(BaseUrl,params = payload)
# print request.url
# if int(request.status_code) <= 400:
request = urllib2.Request(BaseUrl)
response = urllib2.urlopen(request)
page = response.read().decode('utf-8')
# else:
#     print u"请求失败"
# # except:
#     print u'请求过程有错误'

pattern = re.compile('<li.class="subject-item">.+?title=(".+?").+?<div.class="pub">(.+?)</div>.+?class="rating_nums">(.+?)</span>.+?class="pl">(.+?)</span>', re.S)
# pattern = re.compile('<div.class="info".+?title="(.+?)"', re.S)
match = re.findall(pattern, page)
if match:
    for item in match:
        for name in item:
            print name.strip()
else:
    print u"正则表达式错误"
    
# TheFile = open(u"豆瓣读书" + ".txt" , "w+")
# if match:
#     for item in match:
#         for name in item:
#             TheFile.write(name.encode('utf-8').strip())
print "done"
