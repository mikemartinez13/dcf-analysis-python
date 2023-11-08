import pandas as pd
import numpy as np
import requests
import sqlite3
from DbInit import ISDb

db = ISDb(path_db = 'annual_data.db', company_tickers=['AAPL','MSFT','TSLA','NVDA','META','GOOGL','AMZN'], years = 5, replace=True)


db.connect()
sql = '''
SELECT * 
FROM tIncome
JOIN tBalance USING(symbol, calendarYear)
JOIN tCashFlow USING(symbol, calendarYear)

;
'''
#print(db.get_rawdata())

#print(db.get_df())

print(db.run_query(sql))


db.close()