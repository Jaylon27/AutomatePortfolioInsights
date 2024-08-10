![System Design Diagram](System%20Design%20Diagram.png)


## Background

As a passionate investor, managing and tracking my investment portfolio progress every week was a time-consuming task. Every Saturday, I manually gathered data from my Charles Schwab accounts, calculated various metrics such as ROI and total profit, and updated a Google Sheets spreadsheet to track my portfolio's performance. This process was not only repetitive and time-consuming but also prone to errors.

To streamline this process and ensure accuracy, I developed this automation tool. By leveraging Azure Functions, Python, and various APIs, the application fetches data from my Charles Schwab accounts, processes it, and updates specific worksheets in Google Sheets. This automation has significantly reduced the manual effort required and allowed me to focus on more strategic activities.

## Features

- **Automated Data Fetching**: Retrieves portfolio data from Charles Schwab using API calls.
- **Data Processing**: Calculates various investment metrics such as ROI, total profit, and portfolio weights.
- **Google Sheets Integration**: Updates specified worksheets with the latest portfolio data.
- **Azure Key Vault Integration**: Securely stores and retrieves sensitive information such as API keys and account IDs.
- **Scheduled Execution**: Runs automatically every Saturday when the stock market is officially closed.

## Technologies Used

### Python 3.11
Python 3.11 is the programming language used to develop the function app and associated scripts. Python's rich ecosystem of libraries and frameworks makes it an ideal choice for handling data processing, API interactions, and Google Sheets integration.

### Azure Functions
Azure Functions is used to create a serverless function app that handles the scheduled execution and data processing logic for the portfolio automation. It allows the app to run automatically every Saturday and process the data efficiently without requiring a dedicated server.

### Azure Key Vault
Azure Key Vault is employed to securely store and manage sensitive information such as API keys and account IDs. This ensures that credentials are protected and can be accessed securely by the function app during execution.

### Bicep
Bicep is an infrastructure as code (IaC) tool that is used to provision and manage Azure resources. The project uses Bicep templates to deploy the necessary infrastructure, such as the function app and key vault, in a consistent and repeatable manner.

### Google Sheets API
The Google Sheets API is utilized to interact with Google Sheets programmatically. The project uses this API to update specified worksheets in a Google Sheets document with the latest portfolio data, ensuring accurate and up-to-date tracking.

### Charles Schwab API
The Charles Schwab API is used to fetch portfolio data from Charles Schwab accounts. This data includes details about different types of investments, such as equities and options, which are then processed and updated in Google Sheets.

### gspread
gspread is a Python library used to interact with Google Sheets. It simplifies the process of authenticating with Google, accessing spreadsheets, and updating cells with new data, making it a crucial part of the project's data integration.

## Usage

- The function app is scheduled to run every Saturday at 9:30 AM UTC.
- Logs can be monitored via Azure Monitor and Application Insights.
- Manually trigger the function if needed using Azure Functions' interface.
