# -*- coding:utf-8 -*-

import MySQLdb

class Mysql:
    
    def __init__(self):
        try:
            self.db = MySQLdb.Connect('localhost' , 'root' , '306235911' , 'doubanbook')
            self.cur = self.db.cursor()
        except MySQldb.Error , e:
            print "连接数据库错误，原因 %d : %s" % (e.args[0] ,e.args[1])
            
    def insertData(self, BookType, identity, name, info , score, num):
        # sql = "INSERT INTO book VALUES (%d,%s,%s,%s,%s)" % (identity , name , info , score , num)
        sql = "INSERT INTO %s VALUES " % BookType + "(%s,%s,%s,%s,%s)"
        try:
            self.db.set_character_set('utf8')
            # result = self.cur.execute(sql)
            result = self.cur.execute(sql,(identity , name , info , score , num))
            insert_id = self.db.insert_id()
            self.db.commit()
            if result:
                return True
            else:
                return False
        except MySQLdb.Error , e:
            self.db.rollback()
            if "'key'PRIMARY" in e.args[1]:
                print u"数据已存在，未插入数据"
            else:
                print "插入数据失败，原因 %d : %s" % (e.args[0] ,e.args[1])
                
    def createTable(self , table):
        sql = """CREATE TABLE %s (
        identity INT UNSIGNED NOT NULL PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        info VARCHAR(65) NOT NULL,
        score VARCHAR(15) NOT NULL,
        num VARCHAR(20) NOT NULL);""" %  table
        # drop = "DROP TABLE IF EXISTS %s" % table
 
        try:
            # self.cur.execute(drop)
            self.cur.execute(sql)
            print u"创建数据库表成功"
        except MySQLdb.Error,e:
            self.db.rollback()
            print "创建数据库表失败,原因 %d : %s" % (e.args[0] , e.args[1])
        except:
            print u"数据库语言错误"
            
            
        
        