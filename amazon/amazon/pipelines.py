# -*- coding: utf-8 -*-
import pymysql
from pymysql import connections
class AmazonPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='imooc')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = item['book_name']
        kws = item['kindle_price']
        jin = item['jin_price']
        pin = item['pin_price']
        sql = "insert into t_amazon(BookName,KindlePrice,JinPrice,PinPrice) VALUES(%s,%s,%s,%s)"
        self.cursor.execute(sql, (name, kws, jin,pin,))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
