# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime, timedelta
import lxml, re

from szrongzi import settings
from szrongzi.items import ShrongziItem, ShrongziMingxiItem
from lxq_misc import is_weekend, str2float

class SzseRongziSpider(scrapy.Spider):
    name = "szse_rongzi"
    allowed_domains = ["www.szse.cn"]
    start_urls = []
    
    def __init__(self, category=None, *args, **kwargs):
        super(SzseRongziSpider, self).__init__(*args, **kwargs)
        
        start_date = settings.START_DATE
        end_date = settings.END_DATE
        
        curr_date = start_date
        
        self.start_urls = []
        
        urlbase1 = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab1&txtDate='
        urlbase2 = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2&txtDate='
        
        while curr_date <= end_date:
            if not is_weekend(curr_date):                
                self.start_urls.append(urlbase1+curr_date.strftime('%Y-%m-%d'))
                self.start_urls.append(urlbase2 + curr_date.strftime('%Y-%m-%d'))
            curr_date += timedelta(1)
        
   
    def parse(self, response):
        self.log(response.url, level = scrapy.log.INFO)
        if response.url.find('TABKEY=tab1') != -1:
            item = ShrongziItem()

            doc = lxml.html.fromstring(response.body)
        
            item['rongzi_mairu'] = str2float(doc.xpath('//tr/td[1]/text()')[1])
            item['rongzi_yue'] = str2float(doc.xpath('//tr/td[2]/text()')[1])
            item['rongquan_maichu'] = str2float(doc.xpath('//tr/td[3]/text()')[1])
            item['rongquan_yuliang'] = str2float(doc.xpath('//tr/td[4]/text()')[1])
            item['rongquan_yuliang_jine'] = str2float(doc.xpath('//tr/td[5]/text()')[1])
        
            date_str = re.findall('txtDate=([\d-]+)', response.url)[0]
        
            item['trading_day'] = datetime.strptime(date_str, '%Y-%m-%d').date()
            item['market'] = 'sz'
            yield item
        elif response.url.find('TABKEY=tab2') != -1:
            
            doc = lxml.html.fromstring(response.body)

            for k, sel in enumerate(doc.xpath('//tr')):
                if k == 0:
                    continue
                try:
                    item = ShrongziMingxiItem()
                    item['stock_code'] = sel.xpath('./td[1]/text()')[0]
                    item['stock_name'] = sel.xpath('./td[2]/text()')[0]
                    item['rongzi_mairu'] = str2float(sel.xpath('./td[3]/text()')[0])
                    item['rongzi_yue'] = str2float(sel.xpath('./td[4]/text()')[0])
                    item['rongquan_maichu'] = str2float(sel.xpath('./td[5]/text()')[0])
                    item['rongquan_yuliang'] = str2float(sel.xpath('./td[6]/text()')[0])
                    item['rongquan_yue'] = str2float(sel.xpath('./td[7]/text()')[0])               
                    item['rongquan_changhuan'] = None
                    item['rongzi_changhuan'] = None
                    
                    item['market'] = 'sz'
                    date_str = re.findall('txtDate=([\d-]+)', response.url)[0]        
                    item['trading_day'] = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                except IndexError:
                    continue
                yield item
