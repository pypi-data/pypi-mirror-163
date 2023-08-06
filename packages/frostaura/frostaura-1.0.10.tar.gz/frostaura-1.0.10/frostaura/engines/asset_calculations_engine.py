'''This module defines calculations engine components.'''
from frostaura.models import ProfitCalculationResult
import pandas as pd

class IAssetCalculationsEngine:
    '''Component to perform functions related to asset calculations.'''

    def interpolate_holdings_profits(self, holdings: pd.DataFrame) -> pd.DataFrame:
        '''Determine individual asset profit ratio & profit USD and interpolate them into a copy of the given holdings.'''

        raise NotImplementedError()

    def calculate_holdings_profit(self, holdings: pd.DataFrame) -> ProfitCalculationResult:
        '''Determine the holdings profit percentage & profit USD, given the holdings.'''

        raise NotImplementedError()

    def calculate_holdings_ratios(self, holdings: pd.DataFrame) -> pd.DataFrame:
        '''Determine the ratios that each asset makes up of the overall portfolio, adding up to 1.'''

        raise NotImplementedError()
