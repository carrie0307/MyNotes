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
