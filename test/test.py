import requests
import matplotlib.pyplot as plt
import sqlite3 
import pandas as pd

conn = sqlite3.connect('databases/dcf.db')
curs = conn.cursor()

API_KEY = input()

company = "EA"
years = 4

income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={years}&apikey={API_KEY}")

income_statement = income_statement.json()
#small change
revenues = list(reversed([income_statement[i]['revenue'] for i in range(len(income_statement))]))

profits = list(reversed([income_statement[i]['grossProfit'] for i in range(len(income_statement))]))
net_income = list(reversed([income_statement[i]['netIncome'] for i in range(len(income_statement))]))
time = list(reversed([income_statement[i]['calendarYear'] for i in range(len(income_statement))]))
d = {'revenues':revenues, 'profits':profits, 'net income':net_income, 'time':time}
dcf_df = pd.DataFrame(data = d)
sql_clear = '''
DROP TABLE IF EXISTS dcf_table
;

'''
#print(dcf_df)
curs.execute(sql_clear)

dcf_df.to_sql('dcf_table',
         conn,
         index = False)

sql = '''
SELECT *
FROM dcf_table
;
'''
print(pd.read_sql(sql, conn))

plt.plot(pd.read_sql(sql, conn)['time'],pd.read_sql(sql, conn)['revenues'] )
plt.show()
'''
plt.plot(revenues, label = "Revenue")
plt.plot(profits, label = "Profit")
plt.plot(net_income, label  = "netIncome")
plt.legend(loc = 'upper left')
plt.show()
'''

conn.close()
# automate pulling from the API, populate the database
# Once it's built up, we can mess around with it as needed