# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from hashlib import md5

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
from utils.compress_hash import compress_hash


class PostsPipeline(object):
    def process_item(self, item, spider):
        # print item['url']

        return item


class SQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='cnbeta',
                                            user='cnbeta', passwd='cnbeta',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread

        url_hash = md5(item['url']).hexdigest()

        tx.execute("SELECT * FROM post WHERE hash = '" + url_hash + "' ")

        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item['title'][0], level=log.DEBUG)
        else:
            tx.execute(
                "insert into post (link, title,hash ,created,statue,introduction,content,post_time) "
                "values (%s, %s, %s, %s,%s, %s,%s,%s)",
                (item['url'],
                 item['title'][0],
                 url_hash,
                 datetime.datetime.now(),
                 'done',
                 item['introduction'][0],
                 item['content'][0],
                 datetime.datetime.strptime(item['post_time'][0], '%Y-%m-%d %H:%M:%S')
                 )
            )
            # 2015-02-02 16:51:33
            # log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
