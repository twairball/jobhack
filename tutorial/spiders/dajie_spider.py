# -*- coding=UTF-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import DajieItem

# import codecs

class DajieSpider(BaseSpider):
    name = "dajie"
    allowed_domains = ["job.dajie.com"]
    start_urls = [
        "http://job.dajie.com/search/index?keyword=ios%E5%B7%A5%E7%A8%8B%E5%B8%88&statType=button&city=310000"
    ]

    def parse(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[@class="search-list-con"]')
        items = []
        # file = codecs.open('dajie.json', 'w', 'utf-8')
        for post in posts:
            item = DajieItem()
            item['title'] = post.xpath('div[@class="jst-title-wrap"]/h3/a/text()').extract()[0]
            item['link'] = post.xpath('div[@class="jst-title-wrap"]/h3/a/@href').extract()[0]
            item['company'] = post.xpath('a[@class="search-company"]/text()').extract()[0]
            item['location'] = post.xpath('p[@class="search-more-info"]/span/text()').extract()[0]
            items.append(item)
            # file.write(output)
        # file.close()
        return items