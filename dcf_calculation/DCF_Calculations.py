# Imports
import pandas as pd


class DCF_Calculations:
    """
    A class for building a discounted cash flow evaluation for a given company.

    Leading class for project creation. All related classes and routines will be performed from within this class, 
    such as calls to database, scraping, calculation methods, etc.

    Attributes:
        ticker (str): target company for model construction
        years (int, default to 5): model forecasting period
        three_point (boolean, default to False): if True, estimate optimistic and pessimitic case models
        chart (boolean, default to False): if True, present graph with model forecasts
    """

    def __init__(self,
                 ticker: str,
                 years: int = 5,
                 three_point: bool = False,
                 chart: bool = False
                 ) -> None:
            pass
    
    # Expect storage object to be JSON 
    
    # Some statements to pull data from DB
    # Some statements to perform analysis on DB data
    # Some statements to plug-and-chug into DCF calculations
    # Return DCF calculations
    