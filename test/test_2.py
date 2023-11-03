import requests
import matplotlib.pyplot as plt

API_KEY = 'nf5clgXrD1RPCtmrlMQf4aACKSuQZBkQ'

company = "EA"
years = 10
period = 'year'

ratios = requests.get(f"https://financialmodelingprep.com/api/v3/ratios/{company}?period={period}&limit={years}&apikey={API_KEY}")

ratios = ratios.json()

print(ratios)

#[print(ratios[i]['calendarYear']) for i in range(len(ratios))]
#[print(ratios[i]['grossProfitMargin']) for i in range(len(ratios))]
[print(f"Net Profit Margin:{ratios[i]['netProfitMargin']} for year: {ratios[i]['calendarYear']}") for i in range(len(ratios))]
[print(f"Gross Profit Margin: {ratios[i]['grossProfitMargin']} for year: {ratios[i]['calendarYear']}") for i in range(len(ratios))]

incomestatementgrowth = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?period={period}&limit={years}&apikey={API_KEY}")
incomestatementgrowth = incomestatementgrowth.json()

[print(f"Net Income Growth: {incomestatementgrowth[i]['growthNetIncome']} for year: {incomestatementgrowth[i]['calendarYear']}") for i in range(len(incomestatementgrowth))]

