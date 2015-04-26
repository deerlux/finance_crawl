# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from szrongzi.items import ShrongziItem, ShrongziMingxiItem
from finance_crawl.FinanceDBAPI import FinanceDB

class SzrongziPipeline(object):
    def process_item(self, item, spider):
        return item

class ShrongziPipeline(object):
    def process_item(self, item, spider):
        if type(item) != ShrongziItem:
            return item
        
        db = FinanceDB()
        db_item = db.Rongzi(trading_day = item["item.trading_day"],
                            market = item["item.market"],
                            rongzi_yue = item["item.rongzi_yue"],
                            rongzi_mairu = item["item.rongzi_mairu"],
                            rongquan_yuliang = item["item.rongquan_yuliang"],
                            rongquan_yuliang_jine = item["item.rongquan_yuliang_jine"],
                            rongquan_maichu = item["item.rongquan_maichu"])
        db.add(db_item)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print("Error when added a row")
        


class ShrongziMingxiPipeline(object):
    def process_item(self, item, spider):
        if type(item) = ShrongziMingxiItem:
            return item
        db = FinanceDB()

        db_item = db.Rongzi_mingxi(
        
            
