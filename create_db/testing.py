import pandas as pd
import numpy as np
import requests
from DbInit import ISDb

db = ISDb(path_db = 'isdb.db', company_ticker='AAPL', years = 5, create=True)

db.income_statement_df()

print(db)

