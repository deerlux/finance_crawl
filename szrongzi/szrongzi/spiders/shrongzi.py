# -*- coding: utf-8 -*-
import scrapy

from szrongzi.settings import END_DATE, START_DATE
from szrongzi.items import ShrongziItem, ShrongziMingxiItem

from datetime import timedelta, datetime
import os.path, re

# module to read xls file
import xlrd

from lxq_misc import is_weekend
from finance_crawl.FinanceDBAPI import FinanceDB

class ShrongziSpider(scrapy.Spider):
    name = "shrongzi"
    allowed_domains = ["www.sse.com.cn"]
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ShrongziSpider, self).__init__(*args, **kwargs)
        baseurl = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/'
        
        db = FinanceDB()
        holidays = [x[0] for x in db.query(db.Holidays.holiday_date).all()]

        curr_date = START_DATE
        while curr_date <= END_DATE:
            if is_weekend() or (curr_date in holidays) :
                curr_date += timedelta(1)
                continue
            urlget = baseurl + \
                    'rzrqjygk' \
                    + curr_date.strftime('%Y%m%d') + '.xls'
            self.start_urls.append(urlget)
            curr_date += timedelta(1)

    def parse(self, response):
        self.log("Crawled url: {0}".format(response.url), scrapy.log.INFO)
        
        tmpfile = os.path.join('/tmp',os.path.basename(response.url))        
        with open(tmpfile, 'wb') as f:
            f.write(response.content)
        
        xls = xlrd.open_workbook(tmpfile)
        sheet1 = xls.sheet_by_index(0)
        sheet2 = xls.sheet_by_index(1)
        
        datestr = re.findall('\d+', os.path.basename(response.url))[0]
        trading_day = datetime.strptime(datestr, "%Y%m%d")
            
        for k in range(sheet1.nrows):
            if k == 0:
                continue
            item = ShrongziItem()
            item["item.trading_day"] = trading_day
            item["item.market"] = "sh"
            item["item.rongzi_yue"] = float(sheet1.row_values(k)[0])
            item["item.rongzi_mairu"] = float(sheet1.row_values(k)[1])
            item["item.rongquan_yuliang"] = float(sheet1.row_values[k][2])
            item["item.rongquan_yuliang_jine"] = float(sheet1.row_values[k][3])
            item["item.rongquan_maichu"] = float(sheet1.row_values[k][4])
            yield item

        for k in range(sheet2.nrows):
            if k == 0:
                continue
            mingxi_item = ShrongziMingxiItem()
            mingxi_item["item.trading_day"] = trading_day
            mingxi_item["item.market"] = "sh"
            mingxi_item["item.stock_code"] = sheet1.row_values[k][0]
            mingxi_item["item.stock_name"] = sheet1.row_values[k][1]
            mingxi_item["item.rongzi_yue"] = float(sheet1.row_values[k][2])
            mingxi_item["item.rongzi_mairu"] = float(sheet1.row_values[k][3])
            mingxi_item["item.rongzi_changhuan"] = float(sheet1.row_values[k][4])
            mingxi_item["item.rongquan_yulian"] = float(sheet1.row_values[k][5])
            mingxi_item["item.rongquan_maichu"] = float(sheet1.row_values[k][6])
            mingxi_item["item.rongquan_changhuan"] = float(sheet1.row_values[k][7])

            yield mingxi_item
            
            
