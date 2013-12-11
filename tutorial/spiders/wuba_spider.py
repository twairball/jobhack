# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import re
from datetime import date, timedelta, datetime

class WubaSpider(CrawlSpider):
    # get today date for T-7 filtering
    date_filter_str = date.today().strftime('%Y%m%d') + "_" + (date.today() - timedelta(days=7)).strftime('%Y%m%d') + "00"

    name = "wuba"
    allowed_domains = ["sh.58.com"]
    start_urls = [
        "http://sh.58.com/tech/?key=ios%E5%BC%80%E5%8F%91&postdate="+date_filter_str,
        "http://sh.58.com/tech/?key=css%E5%BC%80%E5%8F%91&postdate="+date_filter_str,
        "http://sh.58.com/tech/?key=java%E5%BC%80%E5%8F%91&postdate="+date_filter_str,
        "http://sh.58.com/tech/?key=android%E5%BC%80%E5%8F%91&postdate="+date_filter_str,
        "http://sh.58.com/tech/?key=php%E5%BC%80%E5%8F%91&postdate="+date_filter_str,
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('58.com/tech/\d+', ), deny=('\.php', )), callback="parse_post_detail", follow=True),
        Rule(SgmlLinkExtractor(allow=('58.com/tech/pn\d+', ), deny=('\.php', )), callback="parse_index", follow=True),
    )
    
    def parse_start_url(self, response):
        pass

    def parse_index(self, response):
        pass
        
    def parse_post_detail(self, response):
        item = PostItem()
        sel = Selector(response)
        post = sel.xpath('//div[contains(@class, "posCont")]')
        
        # summary section
        posSum = post.xpath('div[contains(@class, "posSum")]')
        title_string = ' '.join(posSum.xpath('h1/text()').extract())
        item['title'] = title_string.strip(' \t\n\r')

        company_name_string = ' '.join(posSum.xpath('dl[contains(@class, "company")]/dt/a/text()').extract())
        item['company'] = company_name_string.strip(' \t\n\r')

        # top header
        tag_spans = post.xpath('ul[contains(@class, "tag")]/li/span')
        for span in tag_spans:
            span_text = ' '.join(span.xpath('text()').extract()).strip(' \n\r\t')
            if re.match('天前发布'.decode('utf-8'), span_text):
                days_before = int(span.xpath('strong/text()').extract()[0])
                date_posted = date.today()- timedelta(days=days_before)
                item['posted_date'] = date_posted.strftime('%Y-%m-%d')
            elif re.match('小时前发布'.decode('utf-8'),span_text):
                hours_before = int(span.xpath('strong/text()').extract()[0])
                date_posted = datetime.now() - timedelta(hours = hours_before)
                item['posted_date'] = date.today().strftime('%Y-%m-%d')
            elif re.match('分钟前发布'.decode('utf-8'),span_text):
                mins_before = int(span.xpath('strong/text()').extract()[0])
                date_posted = datetime.now() - timedelta(minutes = mins_before)
                item['posted_date'] = date.today().strftime('%Y-%m-%d')

        # info section
        posinfo = post.xpath('div[contains(@class, "posinfo")]/div[contains(@class, "xq")]/ul')

        for li in posinfo.xpath('li'):
            label = li.xpath('.//span/text()').extract()[0]

            if re.match("学历要求".decode('utf-8'), label):
                edu_req_string = ' '.join(li.xpath('div[contains(@class, "fl")]/text()').extract())
                item['edu_req'] = edu_req_string.strip(' \t\n\r')

            if re.match("薪资".decode('utf-8'), label):
                salary_string = ' '.join(li.xpath('text()').extract())
                item['salary'] = salary_string.strip(' \t\n\r')

        contents = sel.xpath('//div[contains(@class, "posMsg")]//text()')
        item['job_desc'] = 'XOXOBBQ'.join(contents.extract()).replace('XOXOBBQ', '')
        # item['job_req']...

        location = sel.xpath('//div[contains(@class,"compIntro")]//div[contains(@class,"contact")]//dl/dd/span[contains(@class,"area")]//text()')
        item['location'] = re.sub('\s+', '', ' '.join(location.extract())).strip('(').strip(')')

        item['source'] = "58.com"
        item['url'] = response.url
        return item