import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import gspread
from google.oauth2.service_account import Credentials
from portfolio import Options, Primary, RothIRA
from portfolioDataFetcher import PortfolioDataFetcher
from updateGoogleSheets import UpdateGoogleSheets

def get_secret(vaultUrl, secretName):
    # Authenticate using Azure Default Credential and retrieve secret from Key Vault
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vaultUrl, credential=credential)
    return client.get_secret(secretName).value

# URL of the Azure Key Vault
vaultUrl = "https://fnapp33hyke36k2bsw.vault.azure.net/"

# Retrieve sensitive information from Key Vault
primaryAccountId = get_secret(vaultUrl, "primaryAccountId")
optionsAccountId = get_secret(vaultUrl, "optionsAccountId")
rothIRAAccountId = get_secret(vaultUrl, "rothIRAAccountId")
sheetId = get_secret(vaultUrl, "sheetId")

# Google Sheets authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Open the Google Sheets document by its ID
spreadsheet = client.open_by_key(sheetId)

# Create an instance of the Function App
app = func.FunctionApp()

@app.schedule(schedule="0 30 9 * * 6", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def myTrigger(myTimer: func.TimerRequest) -> None:
    # Check if the timer is past due
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    # API key for data fetching
    apiKey = ""
    dataFetcher = PortfolioDataFetcher(apiKey)

    # URLs for different portfolio accounts
    urls = {
        "Roth IRA": f"https://api.schwabapi.com/trader/v1/accounts/{rothIRAAccountId}?fields=positions",
        "Options": f"https://api.schwabapi.com/trader/v1/accounts/{optionsAccountId}?fields=positions",
        "Primary": f"https://api.schwabapi.com/trader/v1/accounts/{primaryAccountId}?fields=positions%20"
    }

    # Create Portfolio instances for each account type
    rothIRAPortfolio = PortfolioDataFetcher.createPortfolio(RothIRA, "Roth IRA", urls["Roth IRA"], dataFetcher)
    primaryPortfolio = PortfolioDataFetcher.createPortfolio(Primary, "Primary", urls["Primary"], dataFetcher)
    optionsPortfolio = PortfolioDataFetcher.createPortfolio(Options, "Options", urls["Options"], dataFetcher)

    portfolios = {
        "Roth IRA": rothIRAPortfolio,
        "Primary": primaryPortfolio,
        "Options": optionsPortfolio
    }
    
    # Update the Net Worth worksheet in Google Sheets
    worksheetName = "Net Worth"
    spreadsheetupdate = UpdateGoogleSheets(spreadsheet, worksheetName, portfolios)
    spreadsheetupdate.updateNetWorth()

    # Update the Stock Portfolio worksheet in Google Sheets
    worksheetName = "Stock Portfolio"
    spreadsheetupdate = UpdateGoogleSheets(spreadsheet, worksheetName, portfolios)
    spreadsheetupdate.updateStockPortfolio()

    logging.info('Python timer trigger function executed.')