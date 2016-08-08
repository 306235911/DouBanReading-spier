# -*- coding:utf-8 -*-

# import requests
import urllib2
import urllib
import re
import time
import mysql

class spider:
    def __init__(self):
        # self.PageNum = 0
        # self.payload = {'start' : self.PageNum , 'type' : 'T'} 
        self.TitleList = []
        # self.title = None
        # 未完成url
        self.BaseUrl = 'https://book.douban.com/tag/'
        self.mysql = mysql.Mysql()

    def getUrl(self , BookType , PageNum):
        url = self.BaseUrl + BookType + '?start=' + str(PageNum) + '&type=T'
        return url

    def getIndex(self):
        url = "https://book.douban.com/tag/?icn=index-nav"
        page = self.request(url)
        pattern = re.compile('<a.href="/tag.+?>(.+?)<', re.S)
        match = re.findall(pattern,page)
        for title in match:
            self.titleList.append(title.strip())
        

    def request(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read().decode('utf-8')
        return page
    
    def getContent(self,page,identity,BookType):
        pattern = re.compile('<li.class="subject-item">.+?title=(".+?").+?<div.class="pub">(.+?)</div>.+?class="rating_nums">(.+?)</span>.+?class="pl">(.+?)</span>', re.S)
        match = re.findall(pattern, page)
        if match:
            for item in match:
                name = item[0].strip()
                info = item[1].strip()
                score = item[2].strip()
                num = item[3].strip()
                if self.mysql.insertData(BookType, identity, name , info , score , num):
                    print u"保存书目成功"
                else:
                    print u"保存书目失败"
                identity += 1
                # for name in item:
                #     TheFile.write(name.encode('utf-8').strip())
        else:
            print u"正则表达式错误"
            
    def main(self):
        identity = 0
        PageNum = 0
        for BookType in self.TitleList:
            self.mysql.createTable(BookType)
            # title = BookType
            while PageNum < 1000:
                # print self.getUrl(BookType,PageNum)
                page = self.request(self.getUrl(BookType,PageNum))
                self.getContent(page , identity , BookType)
                PageNum += 20
                identity += 20
                time.sleep(2)
            PageNum = 0
        
        # page = self.request()
        # self.getContent(page)
        # 
hah = spider()
hah.main()