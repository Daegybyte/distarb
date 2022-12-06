import urllib.request
from pathlib import Path
import pyqtgraph as pg


# This class contains functions that scrape the SEC website and parse through the data
class SEC_Scraper_Helpers():

    def get_html():
        html = ""
        tmp = ""
        url = "https://sec.report/Senate-Stock-Disclosures"
        request = urllib.request.Request(url)
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582")
        with urllib.request.urlopen( request ) as response:
            tmp = response.read()
            html = tmp.decode( 'utf-8' )
            print(f"scraping {url}")

        # save html to file
        base_path = Path(__file__).parent
        file_path = (base_path / "src/sec_filing.html").resolve()
        print(f"\nfile path: {file_path}")


        with open( file_path, 'w' ) as f:
            print( f"\nwriting HTML" )
            f.write(html)
     
    # blocks the sec website into usable data. They only use rows and senator data takes up two rows that are not labeled. 
    # This results in something that visually is different,
    # but programatically requires forcing a difference.
    def parse_html(soup) -> list:
        rows = soup.find_all("tr")
        # ticker = soup.find_all(href="/Ticker")
        row_num = 0
        combined_rows = []
        for tr in rows:
            if(row_num%2 != 0):
                combined_rows.append("ROW")                     # privide a split point for later, combining the two SEC rows
            for td in tr:
                data = td.text
                combined_rows.append(data)
            row_num += 1

        tmp = ""
        for row in combined_rows:
            tmp += str(row) + " "
            
        data = tmp.split("ROW") 
        data = data[1:len(data)] # strip headers
        return data

    def get_senator(data) -> str:
        senator = ""
        data = str(data)
        start = data.rfind("[") + 1
        end = data.rfind("]")
        data = data[start:end]
        data = ''.join(c if c.isalpha() else ' ' for c in data)
        data = data.split()
        if len(data) != 2:                                      # Mitch McConnell requires a special case due to his middle name
            if len(data) == 4:
                if "Mitch" in data[2]:
                    data[2] = "Mitch"
                    senator += data[2]
                    senator += " "
                    senator += data[0] 
            elif len(data) == 3:
                senator += data[1]
                senator += " "
                senator += data[0]    
        else:
            senator += data[1]
            senator += " "
            senator += data[0]    
        
        return senator

    # returns buy or sell
    def get_transaction_type(data) -> str:
        var = ""
        if "Purchase" in data:
            var = "bought"
        else:
            var = "sold"
        return var

    def is_mutual_fund(data) -> bool:
        var = False
        if "Fund-" in data:
            var = True
        return var

    def is_security(data) -> bool:
        var = False
        if "Rate/Coupon" in data:
            var = True
        return var

    def is_stock(data) -> bool:
        var = False
        if "Common Sto" in data:
            var = True
        if "Common" in data:
            var = True
        if "Ordinary Shares" in data:
            var = True
        if "Series C" in data:
            var = True
        if "Series B" in data:
            var = True
        if "Series A" in data:
            var = True
        return var

    def get_asset_type(data) -> str:
        type_ = "" # type is a reserved word, so I had to use type_ instead
        if "Bond" in data:
            type_ = "Bond"
        elif SEC_Scraper_Helpers.is_stock(data):
            type_ = "Stock"
        elif "Ordinary Sha" in data:
            type_ = "Ordinary Shares"
        elif SEC_Scraper_Helpers.is_mutual_fund(data):
            type_ = "Mutual Fund"
        elif SEC_Scraper_Helpers.is_security(data):
            type_ = "Fixed Income Security"
        elif "Short Sale" in data:
            type_ = "Short"
        elif "ETF" in data:
            type_ = "ETF"
        else:
            type_ = "MISSING ASSET TYPE"
        return type_

    def get_stock(data) -> str:
        if "Bond" in SEC_Scraper_Helpers.get_asset_type(data):
            return "Bond"
        data = str(data)
        start = data.find("[") + 1
        end = data.find("]")
        data = data[start:end]
        if len(data) > 7: # I don't think there are any stocks that are longer than 5 characters, but I had to make a choice here and this seemed reasonable
            data = "INVALID STOCK"
        return data

    def get_purchase_date(data) -> str:
        date = ""
        data = data[2]
        data = str(data)
        data = data.split()
        date = data[1][1:]
        return date

    # Used when scraper was repeatedly scraping the SEC website to prevent hitting the SEC website too many times in a short period of time
    # def set_timer(time, unit ) -> int:
    #     unit = unit.lower()
    #     if "sec" in unit:
    #         return time
    #     elif "min" in unit:
    #         return time * 60
    #     elif "hour" in unit:
    #         return time * 3_600
    #     else: return -1
        
if __name__ == "__main__":
    pass