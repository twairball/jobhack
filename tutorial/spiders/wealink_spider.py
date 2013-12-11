# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import codecs
import re

class WealinkSpider(CrawlSpider):
    name = "wealink"
    allowed_domains = ["wealink.com"]
    start_urls = [
        "http://www.wealink.com/zhiwei/shanghai_t7_s/?kw=ios",
        "http://www.wealink.com/zhiwei/shanghai_t7_s/?kw=java",
        "http://www.wealink.com/zhiwei/shanghai_t7_s/?kw=css",
        "http://www.wealink.com/zhiwei/shanghai_t7_s/?kw=android",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('zhiwei/view/\d+', ), deny=('\.php', )), callback="parse_post_detail", follow=True),
        Rule(SgmlLinkExtractor(allow=('zhiwei/shanghai_t7_p\d+_s/', ), deny=('\.php', )), callback="parse_index", follow=True),
    )
    
    def parse_start_url(self, response):
        pass

    def parse_index(self, response):
        pass
        
    def parse_post_detail(self, response):
        sel = Selector(response)
        post = sel.xpath('//div[contains(@class, "job-description")]')
        item = PostItem()

        title_string = ' '.join(post.xpath('div[contains(@class, "header")]/div[contains(@class,"job-title")]/h1/text()').extract())
        item['title'] = title_string.strip(' \t\n\r')

        item['url'] = response.url

        job_vitals = post.xpath('ul[contains(@class, "job-vitals")]')
        company_name_string = ' '.join(job_vitals.xpath('li[contains(@class, "company-name")]/text()').extract())
        item['company'] = company_name_string.strip(' \t\n\r')

        for li in job_vitals.xpath('li'):
            label = li.xpath('span[contains(@class,"txt-holder")]/text()').extract()[0]

            if re.match("工作地点".decode('utf-8'), label):
                location_string = ' '.join(li.xpath('a/text()').extract())
                item['location'] = location_string.strip(' \t\n\r')

            if re.match("学历要求".decode('utf-8'), label):
                edu_req_string = ' '.join(li.xpath('text()').extract())
                item['edu_req'] = edu_req_string.strip(' \t\n\r')

            if re.match("月薪".decode('utf-8'), label):
                salary_string = ' '.join(li.xpath('span[contains(@class, "salary")]/text()').extract())
                if salary_string.strip(' \t\n\r'):
                    item['salary'] = salary_string.strip(' \t\n\r')

            if re.match("发布".decode('utf-8'), label):
                posted_date_string = ' '.join(li.xpath('text()').extract())
                item['posted_date'] = posted_date_string.strip(' \t\n\r')

        contents = post.xpath('div[contains(@class, "content")]')
        for content in contents:
            content_title = content.xpath('.//h3/text()').extract()[0]
            
            if re.match("职责描述".decode('utf-8'), content_title):
                content_string = ' '.join(content.xpath('text()').extract())
                item['job_req'] = content_string.strip(' \t\n\r')
            if re.match("任职要求".decode('utf-8'), content_title):
                content_string = ' '.join(content.xpath('text()').extract())
                item['job_desc'] = content_string.strip(' \t\n\r') 

        item['source'] = "wealink.com"
        return item