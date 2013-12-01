# -*- coding=UTF-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import WubaItem

import codecs

class WubaSpider(BaseSpider):
    name = "wuba"
    allowed_domains = ["sh.58.com"]
    start_urls = [
        "http://sh.58.com/chengxuyuan/"
    ]

    def parse(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[@id="infolist"]/dl')
        items = []
        file = codecs.open('wuba.json', 'w', 'utf-8')
        for post in posts:
            item = WubaItem()
            item['title'] = post.xpath('dt/a/text()').extract()[0]
            item['link'] = post.xpath('dt/a/@href').extract()[0]
            item['company'] = post.xpath('dd[@class="w271"]/a/text()').extract()[0]
            item['location'] = post.xpath('dd[@class="w96"]/text()').extract()[0]
            items.append(item)
            # print item['title'].encode('utf8')
            output = "{'title': \"%s\", 'link': \"%s\", 'company': \"%s\", 'location': \"%s\"}\n" % (item['title'], item['link'], item['company'], item['location'])
            print output
            file.write(output)
        file.close()
        return items