# -*- coding=UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import PostItem

import re
from datetime import date, timedelta, datetime

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
        "http://www.lagou.com/jobs/list_UI?kd=UI&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?kd=%E5%89%8D%E7%AB%AF&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86?kd=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_ruby?kd=ruby&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_python?kd=python&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE?kd=%E6%95%B0%E6%8D%AE&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
        "http://www.lagou.com/jobs/list_C++?kd=C%2B%2B&st=%E4%B8%80%E5%91%A8%E5%86%85&city=%E4%B8%8A%E6%B5%B7",
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

        date_text = jr_array[5]
        days_before = re.search('(\d+)天前发布'.decode('utf-8'), date_text)
        posted_time_today = re.search('(\d+:\d+)发布'.decode('utf-8'), date_text)
        if days_before:
            date_posted = date.today()- timedelta(days=int(days_before.groups(0)[0]))
            item['posted_date'] = date_posted.strftime('%Y-%m-%d')
        elif posted_time_today:
            date_posted = datetime.datetime.strptime(str(posted_time_today.groups(0)[0]), "%H:%M")
            date_posted.replace(date.today().year, date.today().month, date.today().day)
            item['posted_date'] = date_posted.strftime('%Y-%m-%d')


        item['source'] = "lagou.com"
        item['url'] = response.url
        item['score'] = 1
        return item