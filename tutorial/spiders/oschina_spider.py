# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import re
from datetime import date, timedelta, datetime

class OsChinaSpider(CrawlSpider):

    name = "oschina"
    allowed_domains = ["oschina.net"]
    start_urls = [
        "http://www.oschina.net/job?addr_prv=%E4%B8%8A%E6%B5%B7"
    ]  

    rules = (
        Rule(SgmlLinkExtractor(allow=('oschina.net/job/detail/\d+_\d+$', ), deny=('\.php', )), callback="parse_post_detail", follow=True),
        Rule(SgmlLinkExtractor(allow=('oschina.net/job?.*addr_prv=%E4%B8%8A%E6%B5%B7.*&p=\d$', ), deny=('\.php', )), callback="parse_index", follow=True),
    )
    
    def parse_start_url(self, response):
        pass

    def parse_index(self, response):
        pass
        
    def parse_post_detail(self, response):
        item = PostItem()
        sel = Selector(response)
        post = sel.xpath('//div[@id="JobDetail"]')

        # job details
        title_string = ' '.join(post.xpath('.//*[contains(@class,"H1")]/text()').extract())
        item['title'] = title_string.strip(' \t\n\r')

        desc = post.xpath('.//*[contains(@class,"detail")]/descendant::text()')
        item['job_desc'] = 'XOBBQ'.join(desc.extract()).replace('XOBBQ','').strip()

        # company
        company_div = post.xpath('//h3[text()[contains(.,"'+'公司'.decode('utf-8')+'")]]')
        company_name_string = ' '.join(company_div.xpath('a/text()').extract())
        item['company'] = company_name_string.strip(' \t\n\r')

        #sidebar info section
        for li in post.xpath('.//ul[contains(@class,"info")]/li'):
            label = li.xpath('strong/text()').extract()[0]

            if re.match("工作地点".decode('utf-8'),label):
                item['location'] = '-'.join(li.xpath('a/text()').extract()).strip(' \n\r\t').strip()

            if re.match("月薪".decode('utf-8'),label):
                item['salary'] = '-'.join(li.xpath('text()').extract()).strip(' \n\r\t').strip()

            if re.match("发布日期".decode('utf-8'),label):
                item['posted_date'] = i.xpath('text()').extract().strip(' \n\r\t').strip()

        #more detail
        for li in post.xpath('.//ul[contains(@class, "more_detail")]/li'):
            label = li.xpath('strong/text()').extract()[0]

            if re.match("学历要求".decode('utf-8'),label):
                item['edu_req'] = ' '.join(li.xpath('text()').extract()).strip(' \r\n\t').strip()

        item['source'] = "oschina.net"
        item['url'] = response.url
        item['score'] = 1
        return item