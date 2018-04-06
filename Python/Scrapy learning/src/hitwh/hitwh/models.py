# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root:1234@127.0.0.1:3306/spide?charset=utf8', echo=False)

class Hitwh_News(Base):
    """hitwh新闻网页爬取存储"""
    __tablename__ = 'hitwh'
    id = Column(Integer, primary_key=True)
    title = Column(String(50)) # 文章标题
    link = Column(String(50)) # 文章链接
    detail = Column(String(100)) # 标题下关于作者、发布时间等的描述
    uploader = Column(String(20)) # 文章发布员


def create_news_table(engine):
    Base.metadata.create_all(engine)


# 下面是MySQLdb/MySQL-Python默认写法
# echo=True是开启调试，这样当我们执行文件的时候会提示相应的文字
# 数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名
# engine = create_engine('mysql://root:1234@127.0.0.1:3306/spide', echo=True)

# 下面是PyMySQL写
# engine = create_engine('mysql+pymysql://root:mysql@127.0.0.1:3306/test', echo=True)

# 现在只是定义了表映射，而数据库里面是没有真实表的，这里我们使用Base类的metadata来帮我们自动创建表
#创建数据表，如果数据表存在则忽视！！！
# Base.metadata.create_all(engine)

# conn = engine.connect()

# Session = sessionmaker(bind=engine)
