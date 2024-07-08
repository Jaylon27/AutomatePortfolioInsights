class Portfolio:
    """
    A class to represent a portfolio.

    Attributes:
    portfolioName: The name of the portfolio.
    currentLiquidationValue: The current liquidation value of the portfolio.
    listOfEquities: A list to store equities in the portfolio.
    url: The URL to fetch portfolio data.
    """
    def __init__(self, portfolioName, currentLiquidationValue, url):
        self.portfolioName = portfolioName
        self.currentLiquidationValue = currentLiquidationValue
        self.listOfEquities = []
        self.url = url
        
    def addEquity(self, equity):
        """
        Adds an equity to the portfolio.
        
        Parameters:
        equity: The equity to be added to the portfolio.
        """
        self.listOfEquities.append(equity)


# Subclasses representing different types of portfolios.
class RothIRA(Portfolio):
    pass

class Primary(Portfolio):
    pass

class Options(Portfolio):
    pass


class Equity:
    """
    A class to represent an equity.

    Attributes:
    symbol: The symbol of the equity.
    longQuantity: The long quantity of the equity.
    marketValue: The market value of the equity.
    longOpenProfitLoss: The long open profit/loss of the equity.
    description: The description of the equity.
    """
    def __init__(self, symbol, longQuantity, marketValue, longOpenProfitLoss, description):
        self.symbol = symbol
        self.longQuantity = longQuantity
        self.marketValue = marketValue
        self.longOpenProfitLoss = longOpenProfitLoss
        self.description = description
    
    def calculateProfitLossPercentage(self):
        """
        Calculates the profit/loss percentage for the equity.
        
        Returns:
        The profit/loss percentage rounded to two decimal places.
        """
        # Calculate the initial investment by subtracting the open profit/loss from the market value.
        initialInvestment = self.marketValue - self.longOpenProfitLoss

        # Calculate the profit/loss percentage and return it.
        return round((self.longOpenProfitLoss / initialInvestment) * 100, 2)