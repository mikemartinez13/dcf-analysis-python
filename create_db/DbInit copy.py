import pandas as pd
import numpy as np
import sqlite3
import os
import requests

class FinancialStatementsDB:
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
            #company_tickers: list,
            #years: int,
            create: bool = False
                ): # Path to the database file # Should we create a new database if it doesn't exist?
        
        if not os.path.exists(path_db):
            if not create:
                raise FileNotFoundError("Database does not exist! Check your filepath.")
            else:
                self.__conn = sqlite3.connect(path_db)
                print('Database connected.')
                self.__conn.close()
        else:
            self.__conn = sqlite3.connect(path_db)
            print('Created a new database.')
            self.__conn.close()

        self.__path = path_db
        self.__i_s_data = []
        self.__b_s_data = []
        self.__c_f_data = []
        self.__years = None
        self.__companies = None

    def load_data(self, company_tickers: list, years: int):
        #
        # load data from FMP API
        #

        # full_is_data = []
        # full_bs_data = []
        # full_cf_data = []
        API_KEY = input("Your FMP API key here:")
        #query company data individually
        for comp in company_tickers:
            income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{comp}?limit={years}&apikey={API_KEY}")
            balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{comp}?limit={years}&apikey={API_KEY}")
            cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{comp}?limit={years}&apikey={API_KEY}")

            income_statement_json = income_statement.json()
            balance_sheet_json = balance_sheet.json()
            cash_flow_json = cash_flow.json()

            self.__i_s_data.extend(income_statement_json)
            self.__b_s_data.extend(balance_sheet_json)
            self.__c_f_data.extend(cash_flow_json)

        income_statement_df = pd.DataFrame(self.__i_s_data)
        balance_sheet_df = pd.DataFrame(self.__b_s_data)
        cash_flow_df = pd.DataFrame(self.__c_f_data)

        #
        # Load dataframes into database
        #
        self.connect()

        sql_check = '''SELECT name FROM sqlite_master'''
        query = self.run_query(sql_check)

        if query.size > 0:
            confirmation = input("WARNING! You are about to overwrite existing data in the database. Would you like to proceed? y/n: ")
            if confirmation == 'y':
                self.__conn = sqlite3.connect(self.__path_db)
                income_statement_df.to_sql('tIncome', self.__conn,index = False, if_exists = 'replace')
                balance_sheet_df.to_sql('tBalance', self.__conn, index = False, if_exists = 'replace')
                cash_flow_df.to_sql('tCashFlow', self.__conn, index = False, if_exists = 'replace')
                print('Database successfully created!')
            else: 
                raise Exception("That was a close one! Next time, write to a new filepath.")
        else:
            self.__conn = sqlite3.connect(self.__path_db)
            income_statement_df.to_sql('tIncome', self.__conn,index = False, if_exists = 'replace')
            balance_sheet_df.to_sql('tBalance', self.__conn, index = False, if_exists = 'replace')
            cash_flow_df.to_sql('tCashFlow', self.__conn, index = False, if_exists = 'replace')
            print('Database successfully created!')

        self.close()
        #Data is successfully loaded

        # self.__i_s_data = full_is_data
        # self.__b_s_data = full_bs_data
        # self.__c_f_data = full_cf_data
        self.__years = years
        self.__companies = company_tickers
        #self.__df = income_statement_df #need to fix


        return
    # Intialize the income_statement request and get the raw data

    def get_rawdata(self):
        '''
        Returns full raw financial statement data as JSON.
        '''
        full_json_data = self.__i_s_data + self.__b_s_data + self.__c_f_data
        return full_json_data.copy()
    
    def get_income_statement_df(self): # create database from FMP API income statement data
        '''
        Returns pandas DataFrame created from income statement JSON raw data.
        '''

        return pd.DataFrame(self.__i_s_data.copy())
    
    
    def get_balance_sheet_df(self):
        '''
        Returns pandas DataFrame created from balance sheet JSON raw data.
        '''
        return pd.DataFrame(self.__b_s_data.copy())
    
# Create a class inheriting Exception to handle DataNotLoadedError

    def get_cash_flow_df(self):
        '''
        Returns pandas DataFrame created from statement of cash flows JSON raw data.
        '''
        return pd.DataFrame(self.__c_f_data.copy())
    

    def get_csv(self):
        '''
        Writes to a csv file created from income statement JSON raw data. Returns none.
        '''
        pass
        # isdf = self.income_statement_df()
        # # write file_path check for overwriting csv files
        # df.to_csv(f"Income_statement_{self.__company}.csv")


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
        if self.__companies is not None and self.__years is not None:
            message = (f"The companies in the data are {self.__companies}, and the data spans the course of the last {self.__years} years.")
        else:
            message = "You haven't loaded in any data yet! Try using .load_data() first."
        return message