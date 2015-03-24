#!/usr/bin/env python2
# -*- coding=utf8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import requests
import lxml.etree as ET
import datetime

from FinanceDBAPI import FinanceDB

from lxq_misc import is_weekend
import logging, re

class InstrumentCrawler:
    

    def __init__(self):
        self.urlbase= 'http://www.cffex.com.cn/fzjy/mrhq/'
        self.db = FinanceDB()
        self.xml_str = ''
        self.data_dicts = []
        self.error_pat =re.compile('.*<title>.+</title>')
        

    def parse_xml(self):
        doc = ET.fromstring(self.xml_str)
        instrument_id = doc.xpath('//instrumentid/text()')
        open_price = doc.xpath('//openprice/text()')
        highest_price = doc.xpath('//highestprice/text()')
        lowest_price = doc.xpath('//lowestprice/text()')
        close_price = doc.xpath('//closeprice/text()')
        presettlement_price = doc.xpath('//presettlementprice/text()')
        settlement_price = doc.xpath('//settlementprice/text()')
        open_interest = doc.xpath('//openinterest/text()')
        volume = doc.xpath('//volume/text()')
        turnover = doc.xpath('//turnover/text()')
    
        self.data_dicts = []
        for k,v in enumerate(instrument_id):
            item = {}
            for x in ['instrument_id', 
                'open_price',
                'highest_price',
                'lowest_price',
                'close_price',
                'presettlement_price',
                'settlement_price',
                'open_interest',
                'volume',
                'turnover']:
                try:
                    item[x] = eval(x)[k].strip()
                except IndexError as e:
                    logging.warn('[WARNING] IndexError!')
                    item[x] = None
            self.data_dicts.append(item)
    
    def date2db(self, curr_date):        
        for item_dict in self.data_dicts:
            item = self.db.Instrument()
            for k,v in item_dict.iteritems():
                exec('item.'+k + '= v')
            item.trading_day = curr_date
            self.db.add(item)

        self.db.commit()
    

    def crawl_data(self, startdate, 
        enddate = datetime.datetime.now().date() - datetime.timedelta(1)):
        curr_date = startdate - datetime.timedelta(1)
        
        while enddate > curr_date:
            curr_date = curr_date + datetime.timedelta(1)
            if is_weekend(curr_date):
                continue
            urlget = self.urlbase + curr_date.strftime('%Y%m/%d/index.xml')
            logging.info('[INFO] crawling: ' + urlget)
            self.xml_str = requests.get(urlget).content

            if self.error_pat.search(self.xml_str):
                continue

            self.parse_xml()
            self.date2db(curr_date)
            logging.info('[INFO] data is saved to database')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        filename = 'log.txt',
        filemod ='w')
    startdate = datetime.date(2014,1,1)
    enddate = datetime.date(2015,3,22)
    crawler = InstrumentCrawler()
    crawler.crawl_data(startdate,enddate)
