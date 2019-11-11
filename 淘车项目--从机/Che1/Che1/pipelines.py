# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class Che1Pipeline(object):
    def __init__(self):
        print("--------------------------------------------------------")
        self.count = 1
        # 客户端对象
        self.client = pymongo.MongoClient(host='10.10.86.253',port=27017)

        # 链接名为‘maoyandb’数据库
        self.db =self.client['TaocheDB']
    def process_item(self, item, spider):
        print(self.count, dict(item))
        self.count +=1
        # 获取名为'cinema_name'的表，并插入一条信息
        self.db['vehicles'].insert(dict(item))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*2")
        return item

