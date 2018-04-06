# Scrapy03-各类Spider
---

## CrawlSpider

链接爬取蜘蛛，专门为那些爬取有特定规律的链接内容而准备的。


它除了从`scrapy.Spider`类继承的属性外，还有一个新的属性`rules`,它是一个`Rule`对象列表，每个`Rule`对象定义了某个规则，如果多个`Rule`匹配一个连接，那么使用第一个，根据定义的顺序。

一个详细的例子：
``` python
t.asp?page=2&id=1&nid="]
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
        yidle item

```

还有其他的Spider,之后更新补充

---
2017.08.23




