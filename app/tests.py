import unittest
import alignment_helpers as alignment
import pandas as pd
from pathlib import Path
import main as main

class DA_Tests(unittest.TestCase):
    REAL_TICKER = 'aapl'
    FAKE_TICKER = 'vvvvv'
    
    base_path = Path(__file__).parent
    file_path = (base_path / 'src/stock_list.csv').resolve()
    with open(file_path, 'r') as f:
        df_tickers = pd.read_csv(f)
   
    TICKERS = df_tickers['ticker_symbol'].values.tolist()       # list of tickers
    TICKERS_LOWER = df_tickers['tickers_lower'].values.tolist()
    COMPANIES = df_tickers['company_name'].values.tolist()      # list of company names
    CLEAN_COMPANIES = df_tickers['clean_companies'].values.tolist()   
    
    # Running tests start after this commented out block
    # Commented out because having this fake company name in the csv file causes yfinance to freak out and also throws off the alignments. 
    # These can be added back as later for testing purposes as long as the fake company name is then removed from the csv file when the test is done.
    
    # def test_get_CLEAN_COMPANY(self):
    #     company = alignment.Helpers.get_clean_name('Appl3 .Banana _PEAR!@#')
    #     self.assertEqual(company, 'appl3bananapear')
    
    # def test_get_ticker_from_clean_name(self):
    #     ticker = alignment.Helpers.get_ticker_from_clean_name('appl3bananapear')
    #     self.assertEqual(ticker, 'ABPABP')
    
    # def test_get_company_from_clean_name(self):
    #     company = alignment.Helpers.get_company_from_clean_name('appl3bananapear')
    #     self.assertEqual(company, 'Appl3 .Banana _PEAR!@#')
    
    # def test_split_and_strip(self):
    #     company = main.UI_MainWindow.split_and_strip(self,'Appl3 .Banana _PEAR!@#')
    #     self.assertEqual(company, ['Appl3', 'Banana', 'PEAR'])
     
    
    # get the first row of the dataframe
    def test_first_row(self):
        df = self.df_tickers
        self.assertEqual(df.iloc[0, 0], 'A')
        self.assertEqual(df.iloc[0, 1], 'Agilent Technologies Inc. Common Stock')
        self.assertEqual(df.iloc[0, 2], 'agilenttechnologiesinccommonstock')
        self.assertEqual(df.iloc[0, 3], 'a')

    def test_ticker_getter_type_list(self):
        tickers = alignment.Helpers.get_TICKERS()
        # assert that the tickers are not empty
        self.assertTrue(tickers)
        # assert that the tickers are a list
        self.assertIsInstance(tickers, list)
        
    def test_company_getter_type_list(self):
        companies = alignment.Helpers.get_COMPANIES()
        # assert that the companies are not empty
        self.assertTrue(companies)
        # assert that the companies are a list
        self.assertIsInstance(companies, list)
        
    def test_clean_company_getter_type_list(self):
        companies = alignment.Helpers.get_CLEAN_COMPANIES()
        # assert that the companies are not empty
        self.assertTrue(companies)
        # assert that the companies are a list
        self.assertIsInstance(companies, list)
        
    def test_alignents_type_str(self):        
        alignments, _,is_business = alignment.Helpers.get_alignments(self.REAL_TICKER, False)
        self.assertIsInstance(alignments, str)
        
    def test_len_alignments(self):
        _, alignments, is_business= alignment.Helpers.get_alignments(self.REAL_TICKER, False)
        self.assertTrue(alignments)
        self.assertIsInstance(alignments, str)
        self.assertEqual(len(alignments.splitlines()), 10)
        
    def test_is_business_false(self):
        x, y, is_business = alignment.Helpers.get_alignments(self.FAKE_TICKER, False)
        self.assertFalse(is_business)
        
    def test_is_business_true(self):
        x, y, is_business = alignment.Helpers.get_alignments(self.REAL_TICKER, True)
        self.assertTrue(is_business)
           
    def test_alignments(self):
        distances, tickers, is_business= alignment.Helpers.get_alignments(self.REAL_TICKER, False)
        # assert that the alignments are not empty
        self.assertTrue(tickers)
        # assert that the alignments are a string
        self.assertIsInstance(tickers, str)
        # assert that the alignments are a string
        self.assertEqual(len(tickers.splitlines()), 10)
        # check the alignment values in the lines
    
        self.assertEqual(tickers.splitlines()[0], 'aapl')
        self.assertEqual(tickers.splitlines()[1], 'aal') 
        self.assertEqual(tickers.splitlines()[2], 'aap')
        self.assertEqual(tickers.splitlines()[3], 'aa')
        self.assertEqual(tickers.splitlines()[4], 'al') 
        self.assertEqual(tickers.splitlines()[5], 'ap') 
        self.assertEqual(tickers.splitlines()[6], 'ampl')
        self.assertEqual(tickers.splitlines()[7], 'adal')
        self.assertEqual(tickers.splitlines()[8], 'adap')
        self.assertEqual(tickers.splitlines()[9], 'aplt')
        
    def test_alignments_non_existent(self):
        alignments, tickers, is_business = alignment.Helpers.get_alignments(self.FAKE_TICKER, False)
        # assert that the alignments are not empty
        self.assertTrue(tickers)
        # assert that the alignments are a string
        self.assertIsInstance(tickers, str)
        # assert that the alignments are a string
        self.assertEqual(len(tickers.splitlines()), 10)
        # check the alignment values in the lines
        self.assertEqual(tickers.splitlines()[0], 'vvv')
        self.assertEqual(tickers.splitlines()[1], 'v')
        self.assertEqual(tickers.splitlines()[2], 'vcv')
        self.assertEqual(tickers.splitlines()[3], 'vvx')
        self.assertEqual(tickers.splitlines()[4], 'vvr')
        self.assertEqual(tickers.splitlines()[5], 'vvi')
        self.assertEqual(tickers.splitlines()[6], 'vev')
        self.assertEqual(tickers.splitlines()[7], 'viv')
        self.assertEqual(tickers.splitlines()[8], 'vpv')
        self.assertEqual(tickers.splitlines()[9], 'vc')
             
if __name__ == '__main__':
    unittest.main()
    