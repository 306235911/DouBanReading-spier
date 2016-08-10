# -*- coding:UTF-8 -*-

import MySQLdb
import douban

class outPut:
    
    def __init__(self):
        self.douban = douban.spider()
        try:
            self.db = MySQLdb.Connect('localhost' , 'root' , '306235911' , 'doubanbook' ,charset="utf8")
            self.cur = self.db.cursor()
            # 设置发送的SQL语句中使用utf8字符集
            self.cur.execute('SET NAMES utf8')
        except MySQLdb.Error , e:
            print "连接数据库失败 ， 原因 %的： %s" % (e.args[0] , e.args[1])
    
    # 从数据库中获取数据        
    def getBook(self, bookType):
        # 从所提供的表中按score从高到低（即倒序）获取前一百条数据
        sql = "SELECT*FROM %s ORDER BY score DESC LIMIT 100" % bookType
        
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            for row in result:
                identify = row[0]
                name = row[1]
                info = row[2]
                score = row[3]
                num = row[4]
                print u"编号 = %s" % identify
                print u"书名 = %s" % name
                print u"相关信息 = %s" % info
                print u"豆瓣评分 = %s" % score
                print u"评分人数 = %s" % num
                
        except MySQLdb.Error , e:
            print "Error:unable to fetch data,reason: %d : %s" % (e.args[0] ,e.args[1])
    
    # 主程序        
    def main(self):
        titleList = self.douban.indexAPI()
        for title in titleList:
            print "%s" % title
        order = str(raw_input("请输入你想要的类型\n")).decode('gbk')
        while not order in titleList:
            order = str(raw_input("请输入你想要的类型\n")).decode('gbk')
        else:
            self.getBook(order)
        # print "%s类型的书在豆瓣排名前100的是" % order
        # order = raw_input().decode('gbk')
        # print [order]
        # self.getBook(order)
        # self.getBook("小说")
        
hah = outPut()
hah.main()