# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import codecs

class WubaSpider(CrawlSpider):
    name = "wuba"
    allowed_domains = ["sh.58.com"]
    start_urls = [
        "http://sh.58.com/chengxuyuan/"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('', ), deny=('\.php', )), callback="parse_items", follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[@id="infolist"]/dl')
        items = []
        # file = codecs.open('wuba.json', 'w', 'utf-8')
        for post in posts:
            item = PostItem()
            item['title'] = post.xpath('dt/a/text()').extract()[0]
            item['url'] = post.xpath('dt/a/@href').extract()[0]
            item['company'] = post.xpath('dd[@class="w271"]/a/text()').extract()[0]
            item['location'] = post.xpath('dd[@class="w96"]/text()').extract()[0]
            item['source'] =  "58.com"
            items.append(item)

        #     output = "{'title': \"%s\", 'url': \"%s\", 'company': \"%s\", 'location': \"%s\"}\n" % (item['title'], item['url'], item['company'], item['location'])
        #     print output
        #     file.write(output)
        # file.close()
        return items