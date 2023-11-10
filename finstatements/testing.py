import pandas as pd
import numpy as np
import requests
import sqlite3
from financialdb import FinancialStatementsDB

db = FinancialStatementsDB(path_db = 'new_db.db', create = True)



db.load_data(company_tickers = ['AAPL','TSLA','MSFT'], years = 5)

print(db.get_income_statement_df().columns)

print(db)

sql = '''
SELECT * 
FROM tIncome
JOIN tBalance USING(symbol, calendarYear)
JOIN tCashFlow USING(symbol, calendarYear)

;
'''

#print(db.get_df())

print(db.run_query(sql))

