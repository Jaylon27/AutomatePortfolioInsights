import requests
import json

from portfolio import Portfolio, RothIRA, Primary, Options, Equity

class PortfolioDataFetcher:
    def __init__(self, apiKey):
        """
        Initialize the PortfolioDataFetcher with the given API key.
        
        :param apiKey: API key for authentication with the data provider.
        """
        self.apiKey = apiKey

    def fetchData(self, url):
        """
        Fetch data from the provided URL using the API key for authorization.
        
        :param url: The URL to fetch data from.
        :return: Parsed JSON data from the response.
        :raises Exception: If the request fails or returns a non-200 status code.
        """
        headers = {'Authorization': f'Bearer {self.apiKey}', 'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")
        return json.loads(response.content)

    @staticmethod
    def createPortfolio(portfolioType, name, url, dataFetcher):
        """
        Create a portfolio of the specified type using data fetched from the provided URL.
        
        :param portfolioType: The class/type of the portfolio to create.
        :param name: The name of the portfolio.
        :param url: The URL to fetch portfolio data from.
        :param dataFetcher: An instance of PortfolioDataFetcher to fetch data.
        :return: An instance of the specified portfolio type populated with fetched data.
        """
        # Fetch data from the provided URL
        data = dataFetcher.fetchData(url)
        
        # Extract current liquidation value from the fetched data
        currentLiquidationValue = data["aggregatedBalance"]["currentLiquidationValue"]
        
        # Create an instance of the portfolio type with the fetched data
        portfolio = portfolioType(name, currentLiquidationValue, url)
        
        # Loop through the positions in the fetched data to add equities to the portfolio
        for position in data["securitiesAccount"]["positions"]:
            symbol = position["instrument"]["symbol"]
            description = position["instrument"].get("description", "No description available")
            longQuantity = position["longQuantity"]
            marketValue = position["marketValue"]
            longOpenProfitLoss = position["longOpenProfitLoss"]

            # Create an Equity instance for each position and add it to the portfolio
            equity = Equity(symbol, longQuantity, marketValue, longOpenProfitLoss, description)
            portfolio.addEquity(equity)
        
        return portfolio