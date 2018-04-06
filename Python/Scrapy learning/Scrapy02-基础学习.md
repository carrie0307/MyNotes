# Scrapy02-基础学习
---
以爬取[哈工大（威海）](http://news.hitwh.edu.cn/)官网新闻网页为例，实现基础使用

* 创建工程
* 定义要抽取的Item对象
* 编写Spider来爬取所需要的内容
* 使用Pipeline将爬取内容存入数据库


## 创建工程

在要创建工程的目录下执行

``` bash
scrapy startproject hitwh[工程名]
```

将会创建hitwh文件夹，其目录结构如下：
```
hitwh/
    scrapy.cfg            # 部署配置文件

    hitwh/           # Python模块，所有的代码都放这里面
        __init__.py

        items.py          # Item定义文件

        pipelines.py      # pipelines定义文件

        settings.py       # 配置文件

        spiders/          # 所有爬虫spider都放这个文件夹下面
            __init__.py
            ...
            
```

## 定义Item

创建一个scrapy.Item类，并定义它的类型为scrapy.Field的属性，
我们准备将新闻网页的标题、链接、发布员以及发布时间等详细信息爬取下来，因此在**items.py**中定义如下类。

``` python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HitwhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field() # 新闻标题
    detail = scrapy.Field() # 标题下关于发布时间、作者等的说明
    link = scrapy.Field() # 新闻链接
    uploader = scrapy.Field() # 新闻发布员

```

## 爬虫Spider

在蜘蛛类中定义了一个初始化的URL下载列表，以及怎样跟踪链接，如何解析页面内容来提取Item。

定义一个Spider，只需继承`scrapy.Spider`类并定于一些属性：

* name: Spider的名称，运行时据此来运行不同的Spider，因此必须是唯一的
* start_urls: 初始化下载链接URL
* parse(): 用来解析下载后的Response对象，该对象也是这个方法的唯一参数。
它负责解析返回页面数据并提取出相应的Item（返回Item对象），还有其他合法的链接URL（返回Request对象）。

#### 最基础部分

在hitwh/spiders文件夹下面新建`news_spider.py`，内容如下

```python
# -*- coding: utf-8 -*-
import scrapy
from hitwh.items import HitwhItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class HitwhSpider(scrapy.Spider):
    name = "hitwh" # 爬虫名称
    allowed_domains = ["hitwh.edu.cn"]

    # start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=%d&id=1&nid=' % d for d in range(1,5)] # 可以这样控制页数
    start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=1&id=1&nid=' ] # 以一个新闻列表页为起始

    def parse(self, response):
        for sel in response.xpath('//a[@class="size14"]'): # 这里根据XPath语法获取标签及相关内容
            item = HitwhItem()
            link = sel.xpath('@href')[0].extract()
            # 这里提取到具体新闻页面的路径news_detail.asp?id=28023
            news_url = response.urljoin(link) # 根据路径得到完整的新闻网页链接
            item['link'] = news_url
            print item['link']

```

start_urls是列表，当很多页时，可以采用这样的写法
```python
start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=%d&id=1&nid=' % d for d in range(1,5)]

```

#### 运行爬虫
以上以完成了最简单的爬虫。在根目录执行下面的命令即可运行，其中hitwh是你定义的spider名字：

```
scrapy crawl hitwh
```

如果一切正常，应该可以打印出每一个新闻的url

**接下来的问题是，如果要对每一个新闻页面进行具体的处理，将如何实现呢？**

#### 链接处理
可以通过parse()方法中返回一个Request对象，然后注册一个回调函数来解析新闻详情。

对应的`news_spider.py`的内容如下：

```python
# -*- coding: utf-8 -*-
import scrapy
from hitwh.items import HitwhItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class HitwhSpider(scrapy.Spider):
    name = "hitwh"
    allowed_domains = ["hitwh.edu.cn"]
    
    start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=1&id=1&nid=' ]  # 以一个新闻列表页为起始

    # 继承scrapy.Spider,会默认来执行parse函数因此必须有parse函数
    def parse(self, response):
        for sel in response.xpath('//a[@class="size14"]'): # 这里根据XPath语法获取标签及相关内容
            item = HitwhItem()
            link = sel.xpath('@href')[0].extract()
            news_url = response.urljoin(link) # 获取新闻网页链接
            item['link'] = news_url
            print item['link']
            # yield scrapy.Request(news_url, callback=self.parse_article)
        # page = response.xpath('//table/tr/td/a/@href')[0].extract()
        # nextpage = response.urljoin(page)
        # start_urls.append(nextpage)


    def parse_article(self, response):
        # response 就算请求该url所的响应html页面
        item = HitwhItem()
        item['title'] = response.xpath('//div[@class="newsTitle"]/text()')[0].extract()
        item['detail'] = response.xpath('//div[@class="newsNav"]/text()')[0].extract()
        item['uploader'] = response.xpath('//div[@class="newsUname"]/text()')[0].extract()[1:]
        item['link'] = response.url
        print item['title'], item['detail'], item['uploader'], item['link']
        yield item

```

如上可以看到，parse只提取所需要的链接，链接内容的解析交给另外的方parse_article来处理。

#### 保存抓取数据

最简单的保存抓取数据的方式是使用json格式的文件保存在本地，像下面这样运行：
``` bash
scrapy crawl hitwh -o items.json[文件名.json]
```

运行后，即可在根目录下找到`items.json`文件

## 数据库存储

上面用过将抓取的Item导出为json格式的文件，不过最常见的做法还是编写Pipeline将其存储到数据库中。我们在`hiwh/pipelines.py`定义

其中，使用了python中的`SQLAlchemy`来保存数据库，关于此的基本学习，参考于[此文](http://www.jianshu.com/p/0d234e14b5d3)

根据`SQLAlchemy`，首先在`hiwh/models.py`中完成内容如下：

```python

# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root:1234@127.0.0.1:3306/spide?charset=utf8', echo=False)

class Hitwh_News(Base):
    """hitwh新闻网页爬取存储表"""
    __tablename__ = 'hitwh'
    id = Column(Integer, primary_key=True)
    title = Column(String(50)) # 文章标题
    link = Column(String(50)) # 文章链接
    detail = Column(String(100)) # 标题下关于作者、发布时间等的描述
    uploader = Column(String(20)) # 文章发布员


def create_news_table(engine):
    Base.metadata.create_all(engine)


'''关于sqlalchemy使用的一些说明'''
# 数据库连接：数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名?相关设置(e.g.:charset=utf8)

# 下面是MySQLdb/MySQL-Python默认写法
# engine = create_engine('mysql://root:1234@127.0.0.1:3306/spide', echo=True)
# echo=True是开启调试，这样当我们执行文件的时候会提示相应的文字

# 下面是PyMySQL写
# engine = create_engine('mysql+pymysql://root:mysql@127.0.0.1:3306/test', echo=True)

# 如上只是定义了表映射，而数据库里面是没有真实表的，这里我们使用Base类的metadata来帮我们自动创建表
# 创建数据表，如果数据表存在则忽视！！！
# Base.metadata.create_all(engine)

```

然后,在`hiwh/pipelines.py`中内容如下：

```python

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from hitwh.items import HitwhItem
from scrapy.settings import Settings
from hitwh.models import engine, create_news_table
from hitwh.models import Hitwh_News

# sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

class HitwhPipeline(object):
    def __init__(self):
        print 'starting ...'
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        print 'opening ...'

    def process_item(self, item, spider):
        a = Hitwh_News(
            title=item["title"].encode("utf-8"),
            link=item["link"].encode("utf-8"),
            detail=item["detail"].encode("utf-8"),
            uploader=item["uploader"].encode("utf-8")
            )
        self.session.add(a)
        # self.session.commit() #可以在这里commit，也可以在爬虫结束时一次性commit
        return item

    def close_spider(self, spider):
        """This method is called when the spider is closed."""
        self.session.commit()
        print 'finished ...'

```

最后记得在`hiwh/setting.py`中配置相应的内容
```pyhton
ITEM_PIPELINES = {
    'hitwh.pipelines.HitwhPipeline': 300, # 后面的数字表示它的执行顺序，从低到高执行，范围0-1000
                                        # 创建文件时,默认给了300
}

DATABASE = {'drivername': 'mysql',
             'host': '127.0.0.1',
             'port': '3306',
             'username': 'root',
             'password': 'mysql',
             'database': 'spide',
             'query': {'charset': 'utf8'}}

```

再次运行爬虫即可在数据库看到结果。

---
以上是最基础的部分




