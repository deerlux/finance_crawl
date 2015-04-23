#!/usr/bin/env python2
from __future__ import unicode_literals, print_function

import sh
import datetime

from lxq_misc import is_weekend

if __name__ == '__main__':
    baseurl = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/'
    startdate = datetime.date(2014,1,1)
    enddate = datetime.date(2015,3,20)

    curr_date = startdate - datetime.timedelta(1)

    while enddate > curr_date:
        curr_date = curr_date + datetime.timedelta(1)
        if is_weekend(curr_date):
            continue
        urlget = baseurl + 'rzrqjygk' + curr_date.strftime('%Y%m%d') + '.xls'
        print(urlget)
        try:
            sh.wget(urlget)
        except Exception as e:
            print(e.message)
            
    sh.mv('*.xls', 'data/')
