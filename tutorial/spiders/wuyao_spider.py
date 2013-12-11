# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import re
from datetime import date, timedelta, datetime

class WealinkSpider(CrawlSpider):
    name = "wuyao"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000&keyword=ios",
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000&keyword=android",
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000&keyword=java",
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000&keyword=php",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('job/\d+,c.html', ), deny=('\.php', )), callback="parse_post_detail", follow=True),
        Rule(SgmlLinkExtractor(allow=('list/\d+,.*,\d.html' ), deny=('\.php', )), callback="parse_index", follow=True),
    )
    
    def parse_start_url(self, response):
        pass

    def parse_index(self, response):
        pass
        
    def parse_post_detail(self, response):
        sel = Selector(response)
        post = sel.xpath('//div[contains(@class, "s_txt_jobs")]')
        item = PostItem()

        title_string = ' '.join(post.xpath('.//td[contains(@class, "sr_bt")]/text()').extract())
        item['title'] = title_string.strip(' \t\n\r')

        item['url'] = response.url

        # header section
        for td in post.xpath('table[contains(@class, "jobs_1")]//td'):
            td_text = ' '.join(td.xpath('descendant::text()').extract())

            if re.match("查看公司简介".decode('utf-8'), td_text):
                item['company'] = td.xpath('a/text()').extract()[0]

            if re.match("发布日期".decode('utf-8'), td_text):
                item['posted_date'] = td.xpath('following-sibling::td/text()').extract()[0]
            if re.match("工作地点".decode('utf-8'), td_text):
                item['location'] = td.xpath('following-sibling::td/text()').extract()[0]
            if re.match("学".decode('utf-8')+'\s+'+"历".decode('utf-8'), td_text):
                item['edu_req'] = td.xpath('following-sibling::td/text()').extract()[0]
            if re.match("薪水范围".decode('utf-8'), td_text):
                item['location'] = td.xpath('following-sibling::td/text()').extract()[0]

        # job detail
        td_job_detail = post.xpath('//td[contains(@class,"job_detail")]/descendant::text()')
        item['job_desc'] = '\n'.join(td_job_detail.extract())

        # split into item['job_req']  ?

        item['source'] = "wuyao.com"
        return item