# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'


DEFAULT_ITEM_CLASS = 'tutorial.items.PostItem'

ITEM_PIPELINES = [
    'tutorial.pipelines.RequiredFieldsPipeline',
    'tutorial.pipelines.MySQLStorePipeline',
]

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'jobhack'
MYSQL_USER = 'jobhack'
MYSQL_PASSWD = 'j0bh4ck123'
