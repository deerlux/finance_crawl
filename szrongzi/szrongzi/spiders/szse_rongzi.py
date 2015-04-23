# -*- coding: utf-8 -*-
import scrapy


class SzseRongziSpider(scrapy.Spider):
    name = "szse_rongzi"
    allowed_domains = ["www.szse.cn"]
    start_urls = (
        'http://www.www.szse.cn/',
    )

    def parse(self, response):
        pass
