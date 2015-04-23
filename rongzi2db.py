#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from __future__ import print_function, unicode_literals

from pandas.io import excel
import pandas as pd
import numpy as np

from FinanceDBAPI import FinanceDB

import datetime, os, os.path, re

def sh_rongzi2db(excel_path='./data'):
    temp = os.listdir(excel_path)
    excel_files = [os.path.join(excel_path,x) for x in temp if x.endswith('.xls') ]
     
    date_pat =re.compile('\d+')

    db = FinanceDB()

    for file1 in excel_files:
        print('The file is processing: ' + file1)
        data1 = excel.read_excel(file1)

        data1.columns = ['rongzi_yue','rongzi_mairu', 
        'rongquan_yuliang','rongquan_yuliang_jine',
        'rongquan_maichu','rongziquan_yue']

        trading_day = datetime.datetime.strptime(date_pat.findall(file1)[0], 
        '%Y%m%d')
        
        td_df = pd.DataFrame({'trading_day':[trading_day], 'market':['sh']})
        data = data1.drop('rongziquan_yue', axis=1).join(td_df)

        data.to_sql('rongzi', db.engine, if_exists = 'append', index=False)
         
        data1 = excel.read_excel(file1, 1)
        data1.columns = ['stock_code_int', 'stock_name', 'rongzi_yue',
        'rongzi_mairu', 'rongzi_changhuan', 'rongquan_yuliang', 
        'rongquan_maichu', 'rongquan_changhuan']
       
        # if the stock is not in the stock_info table then insert the stock
        commit_needed = False
        for k, v in data1['stock_code_int'].iteritems():
            if db.query(db.Stock_info.stock_code).filter(db.Stock_info.stock_code==str(v)).all():
                continue
            item = db.Stock_info(stock_code = str(v),
                stock_name = data1['stock_name'].ix[k])
            db.add(item)
            commit_needed = True
        
        if commit_needed:
            db.commit()
        
        lens = len(data1['stock_code_int'])

        td_df = pd.DataFrame({'trading_day':np.repeat(trading_day, lens),
            'stock_code':[str(x) for x in data1['stock_code_int']],
            'market':np.repeat('sh',lens)})

        data = data1.drop(['stock_code_int','stock_name'], axis=1).join(td_df)       
        data.to_sql('rongzi_mingxi', db.engine, if_exists='append', index=False)

if __name__ == '__main__':
    sh_rongzi2db()
