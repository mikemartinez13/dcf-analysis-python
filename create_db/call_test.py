import requests

comp = 'AAPL'
years = 5
API_KEY = input()

income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{comp}?limit={years}&apikey={API_KEY}")

income_statement = income_statement.json()

print(income_statement)