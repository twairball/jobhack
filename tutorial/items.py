# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PostItem(Item):
    title = Field()
    url = Field()
    company = Field()
    location = Field()
    source = Field()
    salary = Field()
    edu_req = Field()
    job_desc = Field()
    job_req = Field()
    posted_date = Field()

    