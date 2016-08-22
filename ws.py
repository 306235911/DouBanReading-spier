# -*- coding:utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for
# flask脚本引入 manager shell
from flask_script import Manager, Shell
# 模板
from flask_bootstrap import Bootstrap
# 表单
from flask_wtf import Form
# 字符串表单 提交按钮
from wtforms import StringField, SubmitField
from flask_moment import Moment
# 数据库
from flask_sqlalchemy import SQLAlchemy

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:306235911@localhost/doubanbook?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

TITLENAME = None

# class NameForm(Form):
#     # 不为空
#     index = StringField(u'你想看什么类型的书？', validators=[Required()])
#     submit = SubmitField(u'确定')
    
    
class titles(db.Model):
    __tabelename__ = 'titles'
    identity = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(40) , unique=True)
    
    def __repr__(self):
        return '<title %r>' % self.name
    

class book(db.Model):
    __tablename__ = 'book'
    identity = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(60))
    info = db.Column(db.String(90))
    score = db.Column(db.String(10))
    num = db.Column(db.String(20))
    BookType = db.Column(db.String(40))
    
    
    
# # 用于生成上下文
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context))


# 
# class title(db.Model):
#     __tabelename__ = 'title'
#     id = db.Column(db.Integer , primary_key=True)
#     name = db.Column(db.String(40) , unique=True)
#     
#     def __repr__(self):
#         return '<title %r>' % self.name
# 
# class book

# 404错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    # form = NameForm()
    titleList = []
    # title = titles.select(columns = 'name')
    title = titles.query.all()
    for onetitle in title:
        # print onetitle
        onetitle = onetitle.name
        titleList.append(onetitle)
    return render_template('index.html' , titlelist = titleList)

@app.route('/title/<titlename>')
def title(titlename):
    bookList = []
    books = book.query.filter_by(BookType = titlename).order_by(book.score.desc()).all()
    # for book in books:
    #     bookList.append(book.)
    return render_template('title.html' , books = books)

if __name__ == '__main__':
    manager.run()