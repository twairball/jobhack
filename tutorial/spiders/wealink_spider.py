# -*- coding=UTF-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import codecs

class WealinkSpider(BaseSpider):
    name = "wealink"
    allowed_domains = ["wealink.com"]
    start_urls = [
        "http://www.wealink.com/zhiwei/shanghai_s/?kw=ios"
    ]

    def parse(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[contains(@class,"main job-list")]/div[contains(@class,"section")]')
        items = []
        file = codecs.open('wealink.json', 'w', 'utf-8')
        for post in posts:
            item = PostItem()
            item['title'] = post.xpath('div[@class="figure-caption"]/div/div[@class="job-title"]/a/text()').extract()[0]
            item['link'] = post.xpath('div[@class="figure-caption"]/div/div[@class="job-title"]/a/@href').extract()[0]
            item['company'] = post.xpath('div[@class="figure-caption"]/div/div[@class="company-name"]/text()').extract()[0]
            item['location'] = post.xpath('div[@class="figure-caption"]/div/div[@class="location-date"]/span[@class="posted-location"]/text()').extract()[0]
            items.append(item)

            output = "{'title': \"%s\", 'link': \"%s\", 'company': \"%s\", 'location': \"%s\"}\n" % (item['title'], item['link'], item['company'], item['location'])
            print output
            file.write(output)
        file.close()
        return items