# -*- coding: utf-8 -*-
import scrapy
from hitwh.items import HitwhItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class LinkSpider(CrawlSpider):
    name = "link"
    allowed_domains = ["hitwh.edu.cn"]
    start_urls = ["http://news.hitwh.edu.cn/news_list.asp?page=2&id=1&nid="]
    rules = (
    # 并且会递归爬取(如果没有定义callback，默认follow=True).
         Rule(LinkExtractor(allow=('news_detail\.asp\?id=\d+')), callback='parse_url'),
         # 提取匹配'/article/\d+/\d+.html'的链接，并使用parse_item来解析它们下载后的内容，不递归
    )


    def parse_url(self, response):
        item = HitwhItem()
        item['title'] = response.xpath('//div[@class="newsTitle"]/text()')[0].extract()
        item['detail'] = response.xpath('//div[@class="newsNav"]/text()')[0].extract()
        item['uploader'] = response.xpath('//div[@class="newsUname"]/text()')[0].extract()[1:]
        item['link'] = response.url
        print item['title'], item['detail'], item['uploader'], item['link']
