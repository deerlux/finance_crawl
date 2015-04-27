# -*- coding: utf-8 -*-

# Scrapy settings for szrongzi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from datetime import date
from scrapy import log

BOT_NAME = 'szrongzi'

SPIDER_MODULES = ['szrongzi.spiders']
NEWSPIDER_MODULE = 'szrongzi.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'szrongzi (+http://www.yourdomain.com)'

START_DATE = date(2015,4,20)
END_DATE = date(2015,4,20)

LOG_LEVEL = log.WARNING
LOG_FILE = "rongzi_crawl.log"

ITEM_PIPELINES = {"szrongzi.pipelines.ShrongziPipeline":200,
    "szrongzi.pipelines.ShrongziMingxiPipeline":300}

