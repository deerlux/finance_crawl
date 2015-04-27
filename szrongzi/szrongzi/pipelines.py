# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log

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
            log.msg(e, log.ERROR)

        return item

        
class ShrongziMingxiPipeline(object):
    def process_item(self, item, spider):
        if type(item) != ShrongziMingxiItem:
            return item
        db = FinanceDB()

        stock_codes = [x.stock_code for x in db.query(db.Stock_info).all()]
        if not (item["stock_code"] in stock_codes):
            db_item = db.Stock_info(stock_code = item["stock_code"],
                                    stock_name = item["stock_name"])
            db.add(db_item)
            db.commit()
            log.msg("Added to stock_info table: {0}".format(item["stock_code"]),
                    level = log.INFO)
            
        db_item = db.Rongzi_mingxi(trading_day = item["trading_day"],
                                   market = "sh",
                                   stock_code = item["stock_code"],
                                   rongzi_yue = item["rongzi_yue"],
                                   rongzi_mairu = item["rongzi_mairu"],
                                   rongzi_changhuan = item["rongzi_changhuan"],
                                   rongquan_yuliang = item["rongquan_yuliang"],
                                   rongquan_changhuan = item["rongquan_changhuan"])
        try:
            db.add(db_item)
            db.commit()
        except Exception as e:
            log.msg(e, log.ERROR)

        return item
            
        
        
            
