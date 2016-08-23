# -*- coding:utf-8 -*-

import requests
import urllib2
import urllib
import re
import time
import mysql

class spider:
    
    # 初始化豆瓣读书的标签为空列表，以及基本的URL，和连接MySQL
    def __init__(self):
        # self.PageNum = 0
        # self.payload = {'start' : self.PageNum , 'type' : 'T'} 
        self.TitleList = ['小说']
        # self.title = None
        self.BaseUrl = 'https://book.douban.com/tag/'
        self.mysql = mysql.Mysql()
    
    # 通过传入书分类名以及当前的页码生成一个完整的URL
    def getUrl(self , BookType , PageNum):
        url = self.BaseUrl + BookType + '?start=' + str(PageNum) + '&type=T'
        return url
    
    # 该函数中URl为分类的页面，通过爬虫爬下全部分类的标题生成一个列表
    def getIndex(self):
        url = "https://book.douban.com/tag/?icn=index-nav"
        page = self.request(url)
        pattern = re.compile('<a.href="/tag.+?>(.+?)<', re.S)
        match = re.findall(pattern,page)
        for title in match:
            self.TitleList.append(title.strip())
        
    # 获得页面html代码
    def request(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read().decode('utf-8')
        return page
    
    # 通过正则表达式获得书名，相关信息，得分，以及评分人数，并写入数据库
    def getContent(self,page,identity,BookType):
        # 加上图片url以及书本连接的正则表达式
        pattern = re.compile('<li.class="subject-item">.+?href=(".+?").+?src=(".+?").+?title="(.+?)".+?<div.class="pub">(.+?)</div>.+?class="rating_nums">(.+?)</span>.+?class="pl">(.+?)</span>', re.S)
        # pattern = re.compile('<li.class="subject-item">.+?title="(.+?)".+?<div.class="pub">(.+?)</div>.+?class="rating_nums">(.+?)</span>.+?class="pl">(.+?)</span>', re.S)
        match = re.findall(pattern, page)
        if match:
            for item in match:
                bookUrl = item[0].strip()
                imgUrl = item[1].strip()
                name = item[2].strip()
                info = item[3].strip()
                score = item[4].strip()
                num = item[5].strip()
                if self.mysql.insertData(BookType, identity, name , info , score , num, bookUrl , imgUrl):
                    print u"保存书目成功"
                else:
                    print u"保存书目失败"
                identity += 1
                # for name in item:
                #     TheFile.write(name.encode('utf-8').strip())
        else:
            print u"正则表达式错误"
    
    # 这是供获得数据库中数据进行输出的重用代码的一个接口        
    def indexAPI(self):
        self.getIndex()
        return self.TitleList
    
    # 主函数        
    def main(self):
        identity = 0
        PageNum = 0
        self.mysql.createTable()
        for BookType in self.TitleList:
            # self.mysql.createTable(BookType)
            # title = BookType
            
            # 据分析得，各分类中书目到1000以后为无效页面，故只到1000
            while PageNum < 1000:
                # print self.getUrl(BookType,PageNum)
                page = self.request(self.getUrl(BookType,PageNum))
                self.getContent(page , identity , BookType)
                PageNum += 20
                identity += 20
                # 防止爬取过快被封ip
                time.sleep(2)
            PageNum = 0
        
        # page = self.request()
        # self.getContent(page)
        
hah = spider()
hah.main()