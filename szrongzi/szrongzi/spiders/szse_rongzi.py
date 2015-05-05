# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime
import lxml

class SzseRongziSpider(scrapy.Spider):
    name = "szse_rongzi"
    allowed_domains = ["www.szse.cn"]
    start_urls = []
    
    def __init__(self, category=None, *args, **kwargs):
        super(SzseRongziSpider, self).__init__(*args, **kwargs)
        
        start_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
        end_date = datetime.strptime(END_DATE, '%Y-%m-%d').date()
        curr_date = start_date
        
        self.start_urls = []
        urlbase = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1837_xxpl&tab2PAGENUM=1&ENCODE=1&TABKEY=tab1&txtDate='
        
        while curr_date < end_date:
            if not is_weekend(curr_date):                
                self.start_urls.append(urlbase+curr_date.strftime('%Y-%m-%d'))
            curr_date += timedelta(1)

#        print(self.start_urls)
   
    
    def parse(self, response):
        self.log(response.url, level = scrapy.log.INFO)
        if response.url.search('TABKEY=tab1') != -1:
            item = SzrongziItem()

            doc = lxml.html.fromstring(response.body)
        
            item['rongzi_mairu'] = doc.xpath('//tr/td[1]/text()')[1]
            item['rongzi_yue'] = doc.xpath('//tr/td[2]/text()')[1]
            item['rongquan_maichu'] = doc.xpath('//tr/td[3]/text()')[1]
            item['rongquan_yuliang'] = doc.xpath('//tr/td[4]/text()')[1]
            item['rongquan_yuliang_jine'] = doc.xpath('//tr/td[5]/text()')[1]
        
            date_str = re.findall('txtDate=([\d-]+)', response.url)[0]
        
            item['trading_day'] = datetime.strptime(date_str, '%Y-%m-%d').date()
            item['market'] = 'sz'
        elif response.url.search('TABKEY=tab2') != -1:
            
            doc = lxml.html.fromsting(response.body)

            for k, sel in enumerate(doc.xpath('//tr')):
                if k == 0:
                    continue
                item = SzrongziMingxiItem()
                item['stock_code'] = sel.xpath('td/text()')[0]
      
        yield item
