# -*- coding:utf-8 -*-

import requests
import urllib2
import urllib
import re
import time

class spider():
    def __init__(self):
        # self.PageNum = 0
        # self.payload = {'start' : self.PageNum , 'type' : 'T'} 
        self.TitleList = ['小说' , '外国文学']
        # self.title = None
        # 未完成url
        self.BaseUrl = 'https://book.douban.com/tag/'

    def getUrl(self , BookType , PageNum):
        url = self.BaseUrl + BookType + '?start=' + str(PageNum) + '&type=T'
        return url

    def request(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read().decode('utf-8')
        print type(page)
        return page
    
    def getContent(self,page):
        pattern = re.compile('<li.class="subject-item">.+?title=(".+?").+?<div.class="pub">(.+?)</div>.+?class="rating_nums">(.+?)</span>.+?class="pl">(.+?)</span>', re.S)
        match = re.findall(pattern, page)
        TheFile = open(u'豆瓣读书' + '.txt' , 'w+')
        if match:
            for item in match:
                for name in item:
                    TheFile.write(name.encode('utf-8').strip())
        else:
            print u"正则表达式错误"
            
    def main(self):
        PageNum = 0
        for BookType in self.TitleList:
            title = BookType
            while PageNum < 1000:
                # print self.getUrl(BookType,PageNum)
                page = self.request(self.getUrl(BookType,PageNum))
                self.getContent(page)
                PageNum += 20
                time.sleep(2)
            PageNum = 0
        
        # page = self.request()
        # self.getContent(page)
        # 
hah = spider()
hah.main()