import pandas as pd
import sqlite3
import os
import requests

class DbInit:
    """
    A class using FMP API to fetch company income statement data and process it into a database.

    Attributes:
        path_db (str): desired filepath for database object.
        company_ticker (str): company ticker as listed on U.S. Stock Exchanges (e.g. Apple = 'AAPL').
        years (int): years of past data desired for the company.
        create (bool, default to False): if True, create a new database if path_db does not exist.
    """
    def __init__(self,
            path_db: str,
            company_ticker: str,
            years: int,
            create: bool = False
                ): # Path to the database file # Should we create a new database if it doesn't exist?
        """
        Initializes an empty database object based on desired filepath and fetches raw income statement data. 
        Parameters:
            path_db (str): desired filepath for database object.
            company_ticker (str): company ticker as listed on U.S. Stock Exchanges (e.g. Apple = 'AAPL').
            years (int): years of past data desired for the company.
            create (bool, default to False): if True, create a new database if path_db does not exist.
        """
        # Check if the file does not exist
        if not os.path.exists(path_db):
            # Should we create it?
            if create:
                self.conn = sqlite3.connect(path_db)
                self.conn.close()
            else:
                raise FileNotFoundError(path_db + ' does not exist. Perhaps your file path is incorrect?')
        
        API_KEY = input("Your FMP API key here:")
        income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company_ticker}?limit={years}&apikey={API_KEY}")

        income_statement_json = income_statement.json()
        
        self.__path_db = path_db
        self.__json_data = income_statement_json
        self.__years = years
        self.__company = company_ticker

        return
    # Intialize the income_statement request and get the raw data

    def get_rawdata(self):
        return self.__json_data.copy()
    
    def get_info(self):
        message = f"The company in the data is: {self.__company} and the data spans the course of the last {self.__years} years."
        return message
    
    def income_statement_df(self): # create database from FMP API income statement data
        """
        Converts JSON object data into DataFrame.
        
        """
        df = pd.DataFrame(data = self.__json_data.copy())
        return df
        '''
        
        CONVERT ALL DATA FROM JSON INTO A DATAFRAME
        
        '''

    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.__path_db)
        self.curs = self.conn.cursor()
        return
    
    def close(self) -> None:
        self.conn.close()
        return
    
    def run_query(self, sql:str):
        '''Use this method for running SELECT queries only'''
        self.connect()
        results = pd.read_sql(sql, self.conn)
        self.close()
        return results