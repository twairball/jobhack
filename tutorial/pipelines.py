# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    required_fields = ('title', 'company', 'url')

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing: %r" % (field, item))
        return item


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM job WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE job
                SET title=%s, company=%s, url=%s, location=%s, source=%s, updated=%s
                WHERE guid=%s
            """, (item['title'].encode('utf-8'), item['company'].encode('utf-8'), item['url'].encode('utf-8'), item['location'].encode('utf-8'), item['source'].encode('utf-8'), now, guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:
            conn.execute("""
                INSERT INTO job (guid, title, url, location, source, updated)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (guid, item['title'].encode('utf-8'), item['url'].encode('utf-8'), item['location'].encode('utf-8'), item['source'].encode('utf-8'), now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()
