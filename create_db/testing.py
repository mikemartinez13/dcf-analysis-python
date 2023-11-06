import pandas as pd
import numpy as np
import requests
import sqlite3
from DbInit import ISDb

db = ISDb(path_db = 'isdb.db', company_tickers=['AAPL','MSFT','TSLA','NVDA','META','GOOGL','AMZN'], years = 5, replace=False)


db.connect()
sql = '''
SELECT * 
FROM i_s_table 
;
'''
print(db.get_rawdata())

print(db.get_df())

print(db.run_query(sql)['symbol'].value_counts())