# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ChePipeline(object):

    def __init__(self):
        # 连接mongo数据库
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        # 选择数据库
        self.db = self.client["taocheDB"]
        self.count = 1

    def process_item(self, item, spider):
        print(self.count, dict(item))
        # 插入mongo数据库
        self.db["cars"].insert(dict(item))
        self.count += 1

        return item
