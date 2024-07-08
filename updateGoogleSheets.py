from google.oauth2.service_account import Credentials
from portfolio import Portfolio, RothIRA, Primary, Options, Equity
from portfolioDataFetcher import PortfolioDataFetcher

class UpdateGoogleSheets:
    def __init__(self, spreadsheet, worksheetName, portfolios):
        """
        Initialize the UpdateGoogleSheets class with the provided parameters.
        
        Args:
        - spreadsheet: The Google Sheets spreadsheet object.
        - worksheetName: The name of the worksheet to update.
        - portfolios: A dictionary of portfolio objects with their names as keys.
        """
        self.spreadsheet = spreadsheet
        self.worksheetName = worksheetName
        self.portfolios = portfolios
    
    def updateNetWorth(self):
        """
        Update the net worth values in the specified worksheet.
        """
        worksheet = self.spreadsheet.worksheet(self.worksheetName)
        worksheet.update_acell('B2', self.portfolios['Primary'].currentLiquidationValue)
        worksheet.update_acell('B3', self.portfolios['Roth IRA'].currentLiquidationValue)
        worksheet.update_acell('B4', self.portfolios['Options'].currentLiquidationValue)
    
    def updateStockPortfolio(self):
        """
        Update the stock portfolio values in the specified worksheet.
        """
        worksheet = self.spreadsheet.worksheet(self.worksheetName)
        cellRange = "A2:A12"
        values = worksheet.batch_get([cellRange])
        valuesList = values[0]

        # Create a dictionary mapping equity symbols/descriptions to their row numbers
        equity_rows = {row[0]: i + 2 for i, row in enumerate(valuesList) if row}

        # Iterate over each portfolio and update the worksheet with equity data
        for portfolio_name, portfolio in self.portfolios.items():
            for equity in portfolio.listOfEquities:
                if portfolio == self.portfolios['Options']:
                    # For options portfolio, match by equity description
                    if equity.description in equity_rows:
                        currentRow = equity_rows[equity.description]
                        worksheet.update_cell(currentRow, 2, equity.marketValue)
                        worksheet.update_cell(currentRow, 3, equity.longQuantity)
                        worksheet.update_cell(currentRow, 7, equity.longOpenProfitLoss)
                else:
                    # For other portfolios, match by equity symbol
                    if equity.symbol in equity_rows:
                        currentRow = equity_rows[equity.symbol]
                        worksheet.update_cell(currentRow, 2, equity.marketValue)
                        worksheet.update_cell(currentRow, 3, equity.longQuantity)
                        worksheet.update_cell(currentRow, 7, equity.longOpenProfitLoss)