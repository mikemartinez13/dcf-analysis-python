import pandas as pd
import numpy as np
import sqlite3
import os
import requests

class ISDb:
    """
    A class to fetch company income statement data and process it into a database. 
    Initializes income statement database based on desired filepath. Also fetches raw income statement data. Powered by FMP API, sqlite, and pandas.

    Attributes:
        path_db (str): desired filepath for database object.
        company_tickers (list): list of companies to query data from. Formatted as listed on U.S. Stock Exchanges (e.g. Apple = 'AAPL').
        years (int): years of past data desired for the company.
        replace (bool, default to False): if True, replace and overwrite database at filepath. If False.
    """

    #Add in balance sheet
 
    def __init__(self,
            path_db: str,
            company_tickers: list,
            years: int,
            replace: bool = False
                ): # Path to the database file # Should we create a new database if it doesn't exist?
        
        full_is_data = []
        full_bs_data = []
        full_cf_data = []
        API_KEY = input("Your FMP API key here:")
        #query company data individually
        for comp in company_tickers:
            income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{comp}?limit={years}&apikey={API_KEY}")
            balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{comp}?limit={years}&apikey={API_KEY}")
            cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{comp}?limit={years}&apikey={API_KEY}")

            income_statement_json = income_statement.json()
            balance_sheet_json = balance_sheet.json()
            cash_flow_json = cash_flow.json()

            full_is_data.extend(income_statement_json)
            full_bs_data.extend(balance_sheet_json)
            full_cf_data.extend(cash_flow_json)

        # Check if the file does not exist
        #if not os.path.exists(path_db):
            # Should we create it?
            #if create:
             #   self.conn = sqlite3.connect(path_db)
            #else:
             #   raise FileNotFoundError(path_db + ' does not exist. Perhaps your file path is incorrect?')

        income_statement_df = pd.DataFrame(full_is_data)
        balance_sheet_df = pd.DataFrame(full_bs_data)
        cash_flow_df = pd.DataFrame(full_cf_data)

        if os.path.exists(path_db):
            if not replace:
                raise Exception("Data already exists in the file! Write to a new filepath.")
            else:
                confirmation = input("WARNING! You are about to overwrite existing data in the table. Would you like to proceed? y/n: ")
                if confirmation == 'y':
                    self.__conn = sqlite3.connect(path_db)
                    income_statement_df.to_sql('tIncome', self.__conn,index = False, if_exists = 'replace')
                    balance_sheet_df.to_sql('tBalance', self.__conn, index = False, if_exists = 'replace')
                    cash_flow_df.to_sql('tCashFlow', self.__conn, index = False, if_exists = 'replace')
                    print('Database successfully created!')
                else: 
                    raise Exception("That was a close one! Next time, write to a new filepath.")
        else:
            self.__conn = sqlite3.connect(path_db)
            income_statement_df.to_sql('tIncome', self.__conn,index = False, if_exists = 'replace')
            balance_sheet_df.to_sql('tBalance', self.__conn, index = False, if_exists = 'replace')
            cash_flow_df.to_sql('tCashFlow', self.__conn, index = False, if_exists = 'replace')
            print('Database successfully created!')

        self.__path_db = path_db #need to fix
        self.__i_s_data = full_is_data
        self.__b_s_data = full_bs_data
        self.__c_f_data = full_cf_data
        self.__years = years
        self.__companies = company_tickers
        #self.__df = income_statement_df #need to fix

        self.__conn.close()

        return
    # Intialize the income_statement request and get the raw data

    def get_rawdata(self):
        '''
        Returns raw income statement data as JSON.
        '''
        return self.__json_data.copy()
    
    def get_df(self): # create database from FMP API income statement data
        '''
        Returns pandas DataFrame created from income statement JSON raw data.
        '''
        return self.__df.copy()

    def get_csv(self):
        '''
        Writes to a csv file created from income statement JSON raw data. Returns none.
        '''
        df = self.income_statement_df()
        # write file_path check for overwriting csv files
        df.to_csv(f"Income_statement_{self.__company}.csv")

        return

    '''def income_statement_db(self, if_exists = {'fail','replace','append'}): # fix this later
        
        Inserts income statement data into empty dataframe. Returns none.
        Parameters:
            if_exists {'fail','replace','append'}: Determines action to be completed if data exists in db. If 'fail', raise error. 
            If 'replace', display warning and then overwrite existing data. If 'append', append data to the end of the table.
        
        df = self.income_statement_df()
        if if_exists == 'fail':
            raise Exception("Data already exists in the file! Write to a new filepath.")
        elif if_exists == 'replace':
            confirmation = input("WARNING! You are about to overwrite existing data in the table. Would you like to proceed? y/n: ")
            if confirmation == 'y':
                df.to_sql('i/s_table', self.connect(),index = False, if_exists = if_exists)
            else: 
                raise Exception("Data already exists in the file! Write to a new filepath.")
        elif if_exists == 'append':
            print("i/s data has been appended to existing table.")
            df.to_sql('i/s_table')
        
        return'''
    
    def connect(self) -> None:
        '''
        Opens connection (for reading) and cursor object (for writing) to database file. Returns none. 
        '''
        self.__conn = sqlite3.connect(self.__path_db)
        self.__curs = self.__conn.cursor()
        return
    
    def close(self) -> None:
        '''
        Closes connection. Returns none.
        '''
        self.__conn.close()
        return
    
    def run_query(self, sql:str):
        """
        Use this method for running SELECT queries only. NO create queries.
        Parameters:
            sql (str): your sql SELECT code
        """
        self.connect()
        results = pd.read_sql(sql, self.__conn)
        self.close()
        return results

    def __str__(self):
        message = (f"The company in the data is {self.__companies}, and the data spans the course of the last {self.__years} years.")
        return message