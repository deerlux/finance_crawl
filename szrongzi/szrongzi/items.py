# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SzrongziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ShrongziItem(scrapy.Item):
    trading_day = scrapy.Field()
    market = scrapy.Field()
    rongzi_yue = scrapy.Field()
    rongzi_mairu = scrapy.Field()
    rongquan_yuliang = scrapy.Field()
    rongquan_yuliang_jine = scrapy.Field()
    rongquan_maichu = scrapy.Field()
    
class ShrongziMingxiItem(scrapy.Item):
    trading_day = scrapy.Field()
    market = scrapy.Field()
    stock_code = scrapy.Field()
    rongzi_yue = scrapy.Field()
    rongzi_mairu = scrapy.Field()
    rongzi_changhuan = scrapy.Field()
    rongquan_yuliang = scrapy.Field()
    rongquan_maichu = scrapy.Field()
    rongquan_changhuan = scrapy.Field()
    stock_name = scrapy.Field()
