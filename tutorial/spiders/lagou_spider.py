# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import re
from datetime import date, timedelta

class LagouSpider(CrawlSpider):
    # get today date for T-7 filtering
    date_filter_str = date.today().strftime('%Y%m%d') + "_" + (date.today() - timedelta(days=7)).strftime('%Y%m%d') + "00"

    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "http://www.lagou.com/jobs/list_iOS?kd=iOS&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_Java?kd=Java&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_PHP?kd=PHP&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_Android?kd=Android&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",    
    ]  

    rules = (
        Rule(SgmlLinkExtractor(allow=('lagou.com/jobs/\d+', ), deny=('\.php', )), callback="parse_post_detail", follow=True),
        Rule(SgmlLinkExtractor(allow=('jobs/\w+?labelWords=label#', ), deny=('\.php', )), callback="parse_index", follow=True),
    )
    
    def parse_start_url(self, response):
        pass

    def parse_index(self, response):
        pass
        
    def parse_post_detail(self, response):
        item = PostItem()
        sel = Selector(response)
        post = sel.xpath('//dl[contains(@class, "job_detail")]')

        # job details
        title_string = ' '.join(post.xpath('dt/h1/text()').extract())
        item['title'] = title_string.strip(' \t\n\r')

        desc = post.xpath('.//dd[contains(@class, "job_bt")]/p/text()')
        item['job_desc'] = '\n'.join(desc.extract())

        # company
        company_div = sel.xpath('//dl[contains(@class, "job_company")]')
        company_name_string = ' '.join(company_div.xpath('dt//h2[contains(@class, "fl")]/text()').extract())
        item['company'] = company_name_string.strip(' \t\n\r')

        # item['location'] = company_div.xpath('dd/div[not(@class)]/text()').extract()[0]


        #job request section
        job_req_string = post.xpath('dd[contains(@class,"job_request")]/text()').extract()[0]
        jr_array = job_req_string.strip().split(' / ')
        item['location'] = jr_array[0]
        item['salary'] = jr_array[2]
        item['edu_req'] = jr_array[4]
        


        # top header
        tag_spans = post.xpath('ul[contains(@class, "tag")]/li/span')
        for span in tag_spans:
            span_text = span.xpath('text()').extract()[0]
            if re.match('天前发布'.decode('utf-8'), span_text):
                days_before = span.xpath('strong/text()').extract()[0]
                date_posted = date.today()- timedelta(days=days_before)
                item['posted_date'] = date_posted.strftime('%Y-%m-%d')
            elif re.match('发布'.decode('utf-8'),span_text):
                #today?
                item['posted_date'] = date.today().strftime('%Y-%m-%d')

        # info section
        posinfo = post.xpath('div[contains(@class, "posinfo")]/div[contains(@class, "xq")]/ul')

        for li in posinfo.xpath('li'):
            label = li.xpath('.//span/text()').extract()[0]


            if re.match("学历要求".decode('utf-8'), label):
                edu_req_string = ' '.join(li.xpath('text()').extract())
                item['edu_req'] = edu_req_string.strip(' \t\n\r')

            if re.match("薪资".decode('utf-8'), label):
                salary_string = ' '.join(li.xpath('span[contains(@class, "salary")]/text()').extract())
                item['salary'] = salary_string.strip(' \t\n\r')

        # item['job_req']...

        item['source'] = "lagou.com"
        item['url'] = response.url
        return item