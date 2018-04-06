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
