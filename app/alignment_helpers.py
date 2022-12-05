import pandas as pd
import clavier
from pathlib import Path
import os
import pyqtgraph as pg


# This is a helper class used to generate the alignments of the ticker symbols
class Helpers():
    base_path = Path(__file__).parent
    file_path = (base_path / "src/stock_list.csv").resolve()
    # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app/src/stock_list.csv'))
    print(f"\nfile path: {file_path}")
    with open(file_path, "r") as f:
        df_tickers = pd.read_csv(f)
   
    TICKERS = df_tickers["ticker_symbol"].values.tolist()           # list of tickers
    COMPANIES = df_tickers["company_name"].values.tolist()          # list of company names
    CLEAN_COMPANIES = df_tickers["clean_companies"].values.tolist() #clean indicates a string that has been stripped of all non-alphanumeric characters and converted to lowercase
    
    def __init__(self, TICKERS, COMPANIES):
        self.TICKERS_LIST = TICKERS
        self.COMPANIES = COMPANIES
     
    # returns a thruple of the distance, tickers, and whether it is from the business list 
    @classmethod
    def get_alignments(cls, search_item, is_business): # get the alignment of the search_item
        keyboard = clavier.load_qwerty(staggering=[0.5, 0.25, 0.5]) # load the qwerty keyboard with standard keyboard staggering
        search_item = search_item.lower()
        alignment_list = []
       
        if is_business == False:
            # print("is_business is False")       
            for ticker in cls.TICKERS:
                ticker = ticker.lower()
                distance = keyboard.word_distance(search_item, ticker, deletion_cost=.001, insertion_cost=.001)     # get the alignment of the search item and the ticker symbol in TICKER_LIST  
                key_distance = keyboard.typing_distance(ticker)   
                # This includes the initial search item and the ticker symbol for graphing  
                if distance <= 1 and key_distance <= 50:                                                            # Got visually reasonable looking visual results with 50. This would need to change for further exploratory analysis
                    alignment_list.append((ticker, distance, key_distance))                                         # append the ticker and alignment score to the alignment_list
        
            alignment_list.sort(key=lambda x: (x[1], x[2]), reverse=False)
            distances = ""                                                                                          # create a single string of the top 10 alignments [0] == ticker, [1] == distance 
            tickers = "".join([f"{item[0]}\n" for i, item in enumerate(alignment_list[:10])])[:-1]                  # create a single string of the top 10 tickers
        
        elif is_business == True:
            # print("is_business is True")
            # get the start company distance
            for company in cls.CLEAN_COMPANIES:
                company = company.lower()
                distance = keyboard.word_distance(search_item, company, deletion_cost=.001, insertion_cost=.001)     # get the alignment of the search item and the ticker symbol in TICKER_LIST  
                distance = float(f"{distance:.7f}")                                                                  # round the distance to 7 decimal places, seven was chosen based on visual inspection of distances
                key_distance = keyboard.typing_distance(company)
                # print(f"\n{company} {distance} {key_distance}")
                if distance <= .05 and key_distance <= 100: 
                    alignment_list.append((company, distance, key_distance)) 
            
            alignment_list.sort(key=lambda x: (x[1], x[2]), reverse=False)                                            # sort the alignment_list by alignment score
            distances = ""
            # create a list of strings of the top 3 companies
            tickers = []
            for item in alignment_list[:3]:
                tickers.append(f"{item[0]}")
                         
        return (distances, tickers, is_business) 
    
    # Getter functions are self explanatory, mostly. "clean" means that the company name has been cleaned of punctuation and special characters including spaces
    @classmethod                                                                                                 
    def get_TICKERS(cls):
        return cls.TICKERS
    
    @classmethod
    def get_COMPANIES(cls):
        return cls.COMPANIES
    
    @classmethod
    def get_CLEAN_COMPANIES(cls):
        return cls.CLEAN_COMPANIES
 
    @classmethod
    def get_ticker_from_name(self, company_name) -> str:
        return self.TICKERS[self.COMPANIES.index(company_name)]
    
    @classmethod
    def get_name_from_ticker(self, ticker_name) -> str:
        return self.COMPANIES[self.TICKERS.index(ticker_name)] 
    
    @classmethod
    def get_clean_name(self, company_name) -> str:
        return self.CLEAN_COMPANIES[self.COMPANIES.index(company_name)]
    
    @classmethod
    def get_ticker_from_clean_name(self, clean_company_name) -> str:
        return self.TICKERS[self.CLEAN_COMPANIES.index(clean_company_name)]
    
    @classmethod
    def get_company_from_clean_name(self, clean_company_name) -> str:
        return self.COMPANIES[self.CLEAN_COMPANIES.index(clean_company_name)]
    
if __name__ == "__main__":
    pass
        
    