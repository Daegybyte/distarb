import sec_scraper_helpers as helpers

class SEC_Scraper():
    
    Senators = []
    Stocks = []
    Transactions = []
    Dates = []

    # This is where the data csv is filled out
    def populate_columns(data) -> None:
        length = len(data)
        for x in range(length):  
            td = data[x]
            
            senator = helpers.SEC_Scraper_Helpers.get_senator(td)
            SEC_Scraper.Senators.append(senator)
            
            stock = helpers.SEC_Scraper_Helpers.get_stock(td)
            SEC_Scraper.Stocks.append(stock)
            
            transaction = helpers.SEC_Scraper_Helpers.get_transaction_type(td)
            SEC_Scraper.Transactions.append(transaction)

            date = helpers.SEC_Scraper_Helpers.get_purchase_date(data)
            SEC_Scraper.Dates.append(date)
           
    # getter used in main.py. Returns a list of dictionaries
    def get_dicts() -> list:
        dicts = {
            "senators":SEC_Scraper.Senators,
            "stocks":SEC_Scraper.Stocks,
            "buy/sell":SEC_Scraper.Transactions,
            "date":SEC_Scraper.Dates
    }
        return dicts
        
        
if __name__ == "__main__":
        pass