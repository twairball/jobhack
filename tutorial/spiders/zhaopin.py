# -*- coding=UTF-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import codecs

class ZhaopinSpider(BaseSpider):
    name = "zhaopin"
    allowed_domains = ["sou.zhaopin.com"]
    start_urls = [
        "http://sou.zhaopin.com/Jobs/SearchResult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=ios"
    ]

    def parse(self, response):
        sel = Selector(response)
        posts = sel.xpath('//tr[contains(@class,"showTR")]')
        items = []
        file = codecs.open('zhaopin.json', 'w', 'utf-8')
        for post in posts:
            item = PostItem()
            item['title'] = post.xpath('td[contains(@class,"Jobname")]/a/text()').extract()[0]
            item['url'] = post.xpath('td[contains(@class,"Jobname")]/a/@href').extract()[0]
            item['company'] = post.xpath('td[contains(@class,"Companyname")]/a/text()').extract()[0]
            item['location'] = post.xpath('td[contains(@class,"Companyaddress")]/text()').extract()[0]
            item['source'] =  "zhaopin.com"
            items.append(item)

            output = "{'title': \"%s\", 'url': \"%s\", 'company': \"%s\", 'location': \"%s\"}\n" % (item['title'], item['url'], item['company'], item['location'])
            print output
            file.write(output)
        file.close()
        return items