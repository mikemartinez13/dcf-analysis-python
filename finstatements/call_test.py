import requests
import sqlite3
import pandas as pd

comp = 'AAPL'
years = 5
#API_KEY = input()

'''income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{comp}?limit={years}&apikey={API_KEY}")

income_statement = income_statement.json()

print(income_statement)'''

conn = sqlite3.connect('annual_data.db')

sql = '''SELECT name FROM sqlite_master'''

print(pd.read_sql(sql, conn).size)