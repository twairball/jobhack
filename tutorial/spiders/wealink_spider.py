# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import codecs

class WealinkSpider(CrawlSpider):
    name = "wealink"
    allowed_domains = ["wealink.com"]
    start_urls = [
        "http://www.wealink.com/zhiwei/shanghai_s/?kw=ios"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('zhiwei/shanghai', ), deny=('\.php', )), callback="parse_items", follow=True),
    )
    
    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[contains(@class,"main job-list")]/div[contains(@class,"section")]')
        items = []
        # file = codecs.open('wealink.json', 'w', 'utf-8')
        for post in posts:
            item = PostItem()
            item['title'] = post.xpath('div[@class="figure-caption"]/div/div[@class="job-title"]/a/text()').extract()[0]
            item['url'] = post.xpath('div[@class="figure-caption"]/div/div[@class="job-title"]/a/@href').extract()[0]
            item['company'] = post.xpath('div[@class="figure-caption"]/div/div[@class="company-name"]/text()').extract()[0]
            item['location'] = post.xpath('div[@class="figure-caption"]/div/div[@class="location-date"]/span[@class="posted-location"]/text()').extract()[0]
            item['source'] = "wealink.com"
            items.append(item)

            # output = "{'title': \"%s\", 'url': \"%s\", 'company': \"%s\", 'location': \"%s\"}\n" % (item['title'], item['url'], item['company'], item['location'])
            # print output
            # file.write(output)
        # file.close()
        return items