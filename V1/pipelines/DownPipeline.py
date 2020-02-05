# -*- coding: utf-8 -*-
import sys
from V1.util.DBUtil import *

from V1.util.sqlFactory import *
import threading

class spidersPipeline(object): #1、入库
    pool = None
    # 开启爬虫时链接数据库
    def __init__(self):
        self.pool = MysqlUtil()
        self.lock = threading.Lock()

    def process_item(self, item):
        sql = getInsertSql(item["table"], item)
        print(sql)
        try:
            self.lock.acquire()
            self.pool.insert_one(sql)
            self.pool.end("commit")
            self.lock.release()
        except Exception as errinfo:
            traceback.print_exc()
            self.pool.end("rollback")
        return item


