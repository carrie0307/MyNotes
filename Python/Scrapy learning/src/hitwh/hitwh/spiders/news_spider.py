# -*- coding: utf-8 -*-
import scrapy
from hitwh.items import HitwhItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class HitwhSpider(scrapy.Spider):
    name = "hitwh"
    allowed_domains = ["hitwh.edu.cn"]

    # start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=%d&id=1&nid=' % d for d in range(1,5)] # 可以这样控制页数
    start_urls=[u'http://news.hitwh.edu.cn/news_list.asp?page=2&id=1&nid=' ] # 以一个新闻列表页为起始

    def parse(self, response):
        print response.url
        print "\n\n\n"
        for sel in response.xpath('//a[@class="size14"]'): # 第三个ul
            item = HitwhItem()
            link = sel.xpath('@href')[0].extract()
            news_url = response.urljoin(link) # 获取新闻网页
            item['link'] = news_url
            yield scrapy.Request(news_url, callback=self.parse_article)
        '''以下是获取新的新闻列表页码，并继续爬取的代码'''
        # pages = response.xpath('//table/tr/td/a/@href')
        # page = pages[2].extract() if len(pages.extract()) == 4 else pages[0].extract()
        # nextpage = response.urljoin(page)
        # if "page=5" not in nextpage: # 爬取i前4页
        #     yield scrapy.Request(nextpage, callback=self.parse)

    def parse_article(self, response):
        # response 就算请求该url所的响应html页面
        item = HitwhItem()
        item['title'] = response.xpath('//div[@class="newsTitle"]/text()')[0].extract()
        item['detail'] = response.xpath('//div[@class="newsNav"]/text()')[0].extract()
        item['uploader'] = response.xpath('//div[@class="newsUname"]/text()')[0].extract()[1:]
        item['link'] = response.url
        # print item['title'], item['detail'], item['uploader'], item['link']
        yield item
