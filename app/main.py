"""
Diego Pisciotta MSD 2022 Capstone project, AKA Stupidity Arbitrage, AKA Distance Arbitrage, AKA Distarb

This is an app developed in Python3 using PyQt5 for the GUI, 
Yfinance -- for the stock data,
Clavier -- to get the keyboard edit distances, 
BeautifulSoup -- for webscraping,
Pandas -- for data manipulation,
Urllib -- for web requests,
Pendulum -- for date manipulation,
Among other libraries for minor miscellaneous tasks, 
Coffee -- just lots and lots of coffee for energy.
Wine -- to cap off rough days.
Wine -- to cap off good days.
Whiskey -- when wine just isn't enough.

Special thanks to:
Ben, my advisor, for always being available to answer questions.
Dav for giving me an apprectiation for the wonders of Python, by making me learn C++.
Varun for taking the time to explain for loops to me when I was feeling particularly overwhelmed early on.
Matthew for teaching me how to use git and how to test my code.
My mum for all the support and encouragement.
Doc for being my fuzzy lil' coding buddy.
"""

from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget
import sys
import alignment_helpers as alignment
import graph_helpers as graph
import regex as re
import sec_scraper as scraper
from bs4 import BeautifulSoup as bs
import sec_scraper_helpers as scraper_helpers
import pandas as pd
from pathlib import Path
import pyqtgraph as pg
import time
import os

# This is class for the main window of the app, it contains the GUI elements as well as the logic for user interaction
class UI_MainWindow(object):       
    def __init__(self, window):
        TICKERS = alignment.Helpers.get_TICKERS()
        self.TICKERS = TICKERS
        COMPANIES = alignment.Helpers.get_COMPANIES()        
        self.COMPANIES = COMPANIES
        DROPDOWN_ITEMS = TICKERS
        self.CLEAN_COMPANIES = alignment.Helpers.get_CLEAN_COMPANIES()
        self.count = 0
        # instantiate pg
        pg.setConfigOption('background', "black")
        self.base_path_html = Path(__file__).parent
        self.file_path_html = (self.base_path_html / "src/sec_filing.html").resolve()

        
        ######################### START GUI SETUP #####################################
        # main window
        window.setObjectName("window")
        window.resize(850, 523)
        window.setMinimumSize(QtCore.QSize(850, 523))
        window.setMaximumSize(QtCore.QSize(850, 523))
        window.setAutoFillBackground(False)
        window.setStyleSheet("background-color: grey; border-color: darkgrey; border-style: solid; border-width: 1px; border-radius: 2px;")
        
        # create a central widget to hold all the other widgets
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget = QtWidgets.QFrame(self.centralwidget)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 850, 500))
        self.centralwidget.setStyleSheet("background-color: grey; border-color: darkgrey; border-style: solid; border-width: 1px; border-radius: 5px;")
        self.centralwidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.centralwidget.setFrameShadow(QtWidgets.QFrame.Raised)
        
        # create a widget for the graph
        self.graph_widget = PlotWidget(self.centralwidget)
        self.graph_widget.setObjectName("graph_widget")
        self.graph_widget.setGeometry(QtCore.QRect(0, 1, 551, 495))
        self.graph_widget.setAutoFillBackground(False)
        self.graph_widget.setStyleSheet("background-color: lightgrey;")
        self.graph_widget.setMouseEnabled(x=False, y=False)         # make the graph unadjustable by the user

       
        
        # create a frame for the search box, the search button, and the ticker list
        self.search_box_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.search_box_groupBox.setGeometry(QtCore.QRect(550, 1, 300, 495))
        self.search_box_groupBox.setStyleSheet("background-color: rgb(69, 69, 69)")
        self.search_box_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.search_box_groupBox.setObjectName("search_box_groupBox")
        self.search_box_groupBox.raise_()
        
        # create the search box
        self.search_box = QtWidgets.QLineEdit(self.search_box_groupBox)
        self.search_box.setGeometry(QtCore.QRect(5, 460, 235, 30))
        self.search_box.setStyleSheet("background-color: lightgrey;")
        self.search_box.setText("")
        self.search_box.setObjectName("search_box")
        self.search_box.setPlaceholderText("Enter a ticker or company name")
        
        # create the search button
        self.btn_search = QtWidgets.QPushButton(self.search_box_groupBox)
        self.btn_search.setGeometry(QtCore.QRect(245, 460, 50, 30))
        self.btn_search.setStyleSheet("background-color: lightgrey;")
        self.btn_search.setObjectName("btn_search")
        self.btn_search.clicked.connect(self.do_it)                   # connect the search button to the do_it method on click    
        self.search_box.returnPressed.connect(self.btn_search.click)  # connect the enter key to the search button
                
        # Create a frame in the top right corner of the window, this is to keep the dropdown list bounded
        self.dropdown_frame = QtWidgets.QFrame(self.search_box_groupBox)
        self.dropdown_frame.setGeometry(QtCore.QRect(3, 1, 294, 140))
        self.dropdown_frame.setStyleSheet("border-style: none; border-radius: 2px;")
        self.dropdown_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropdown_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropdown_frame.setObjectName("dropdown_frame")

        # create a dropdown list and populate it with the tickers 
        self.ticker_drop_down = QtWidgets.QComboBox(self.dropdown_frame)                                                              
        self.ticker_drop_down.setGeometry(QtCore.QRect(1, 5, 292, 30))
        self.ticker_drop_down.setStyleSheet("background-color: lightgrey;")
        self.ticker_drop_down.setObjectName("company_drop_down")
        self.ticker_drop_down.addItems(TICKERS)                                                                                         # add the company names to the drop down list
        self.ticker_drop_down.currentIndexChanged.connect(lambda: self.search_box.setText(self.ticker_drop_down.currentText()))         # set the value of the search box to the selected company name
        self.ticker_drop_down.setLineEdit(QtWidgets.QLineEdit(self.dropdown_frame))
        self.ticker_drop_down.lineEdit().setReadOnly(True)
        
         # create a dropdown list and populate it with the company names
        self.company_drop_down = QtWidgets.QComboBox(self.dropdown_frame)  
        self.company_drop_down.setGeometry(QtCore.QRect(1, 40, 292, 30))
        self.company_drop_down.setStyleSheet("background-color: lightgrey;")
        self.company_drop_down.setObjectName("company_drop_down")
        self.company_drop_down.addItems(COMPANIES)                                                                                      # add the company names to the drop down list
        self.company_drop_down.currentIndexChanged.connect(lambda: self.search_box.setText(self.company_drop_down.currentText()))       # set the value of the search box to the selected company name
        self.company_drop_down.setLineEdit(QtWidgets.QLineEdit(self.dropdown_frame))
        self.company_drop_down.lineEdit().setReadOnly(True)
      
        # create a radio button to select the edit distance algorithm to sort the tickers
        self.btn_align = QtWidgets.QRadioButton(self.search_box_groupBox)
        self.btn_align.setChecked(True)                                      # set the default radio to the edit distance option

        self.btn_align.setGeometry(QtCore.QRect(5, 435, 125, 20))
        self.btn_align.setStyleSheet("background-color: lightgrey;")
        self.btn_align.setObjectName("btn_align")
        
        # create a radio button to select the SEC senate scraper
        self.btn_scrape = QtWidgets.QRadioButton(self.search_box_groupBox)
        self.btn_scrape.setGeometry(QtCore.QRect(170, 435, 125, 20))
        self.btn_scrape.setStyleSheet("background-color: lightgrey")
        self.btn_scrape.setObjectName("btn_scrape")
        
        # create a box to write text to
        self.output_box = QtWidgets.QPlainTextEdit(self.search_box_groupBox)
        self.output_box.setStyleSheet("""
                                      background-color: lightgrey;
                                      color: black;
                                      border-style: solid; 
                                      font-size: 15px; 
                                      border-width: 1px; 
                                      border-radius: 2px; 
                                      border-color: darkgrey;
                                      """)
        self.output_box.setGeometry(QtCore.QRect(5, 234, 290, 195))
        self.output_box.setObjectName("output_box")
        self.output_box.setReadOnly(True)                # make the output box read only to prevent user input making a mess of the text >:(
        
        window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)     
        ######################### END GUI SETUP #####################################

    def get_search_box_text(cls):
        return cls.search_box.text()
    
    # Basic format for the error message box popup
    def error_boilerplate(self, error, description) -> None:
            self.popup = QtWidgets.QMessageBox()
            self.popup.setWindowTitle("Error")
            self.popup.setText(error)
            self.popup.setIcon(QtWidgets.QMessageBox.Critical)
            self.popup.setInformativeText(description)
            self.popup.exec_()
            self.clear_all()
    
    def clear_all(self) -> None:
        self.search_box.clear()
        self.output_box.clear()
        self.btn_align.setChecked(False)
        self.btn_scrape.setChecked
    
    # This is easteregg
    def call_bugs_bunny(self) -> None:
        base_path = Path(__file__).parent
        file_path = (base_path / "src/egg.txt").resolve()
        with open( file_path, 'r' ) as f:
            text = f.read()
        
        self.error_boilerplate("You found the easter egg!", text)
        self.count = 0
        self.clear_all()
     
    # Workhorse method called when the search button is clicked   
    def do_it(self) -> None:
        if self.has_errors():
            return
        # if self.count == 2:
        #     self.call_bugs_bunny()    
                   
        # LOGIC FOR ALIGN BUTTON SELECTED
        if self.btn_align.isChecked():
            print("alignment selected")
            self.search_box.setEnabled(True)
            graph.Graph_Helpers.reset_graph(self)                                       # empty the graph
            self.count += 1                                                             # increment the count for the easter egg
            self.output_box.clear()
            text  = self.get_search_box_text()
            text = self.sanitise_search_box_text(text)
            print(f"\nTEXT: {text}")
            
            # if the text in the search box is in the list of clean names
            if text in self.CLEAN_COMPANIES:
                print("\ntext in clean names")
                _ , C, is_business = alignment.Helpers.get_alignments(text, True)     # get the alignments for the search box text
            else:
                _ , T, is_business= alignment.Helpers.get_alignments(text, False)     # get the alignments for the search box text
   
            # if is_business is true, then the search box text is a business name
            if is_business:
                X = []
                for t in C:
                    print(type(t))
                    c = alignment.Helpers.get_company_from_clean_name(t)
                    x = alignment.Helpers.get_ticker_from_clean_name(t)
                    X.append(x)
                    
                    self.output_box.appendPlainText(c)
                    
                print("Graphing alignments")
                print(f"\nX: {X}")            
                for i in range(3):
                    ticker_name = X[i]                       
                    graph.Graph_Helpers.graph_it(ui, ticker_name, str(ticker_name), i=i, date=None)
            
            if is_business == False:
                self.output_box.appendPlainText(T)
                self.search_box.clear()
                
                T = self.split_and_strip(T)
                print(f"\nclean text: {T}\n")
                # print(T)

                # graph the first three alignments using graph_helpers, i is the rgb color value
                print("Graphing alignments")            
                for i in range(3):
                    ticker_name = T[i]                       
                    graph.Graph_Helpers.graph_it(ui, ticker_name, str(ticker_name), i=i, date=None)
                    # print(f"Graphed {i}")
            
        # LOGIC FOR THE WEB SCRAPER BUTTON
        if self.btn_scrape.isChecked():
            print("scraper selected")
            self.output_box.clear()             
            graph.Graph_Helpers.reset_graph(self)
            
            
            # base_path_html = Path(__file__).parent
            # file_path_html = (base_path_html / "src/sec_filing.html").resolve()
            
            # if file does not exist, create it
            if not os.path.exists(self.base_path_html):
                with open(self.file_path_html, 'w') as f:
                    f.write("")
            

            with open (self.file_path_html, "r") as f:
                html = str(f.readlines())

            # parse the html
            soup = bs( html, 'html.parser' )
            data = scraper_helpers.SEC_Scraper_Helpers.parse_html(soup=soup)

            scraper.SEC_Scraper.populate_columns(data=data)

            data = scraper.SEC_Scraper.get_dicts()
                
            scraper_helpers.SEC_Scraper_Helpers.get_html()
            df = pd.DataFrame(data)
           
            # get the scraped data from the the csv  
            base_path = Path(__file__).parent
           
            file_path = (base_path / "src/data.csv").resolve()
            df.to_csv(file_path, index=False)
            df_CSV = pd.read_csv(file_path)
            df_CSV.reindex(columns=data.keys())
            
            # sleep for .5 seconds to allow the csv to be written
            time.sleep(.5)
            
            # skip to the most recent stock transaction. Limited to 1 because the SEC filings are not always in chronological order and sometimes
            # back and forth buys and sells between the same stock based on stock options from the same senator.
            # not a lot of intersting info could easily be gleaned from additional data
            iloc = 0  
            while df_CSV.iloc[iloc]['stocks'] == 'Invalid Stock' or df_CSV.iloc[iloc]['stocks'] == 'Bond' and iloc < len(df_CSV):
                current_trade = df_CSV.iloc[iloc]
                iloc += 1
            current_trade = df_CSV.iloc[iloc].values 
            senator = current_trade[0]
            stock = current_trade[1]
            buy_sell = current_trade[2]
            date = current_trade[3]
            
            print(f"ticker: {stock}")
            company_name = alignment.Helpers.get_name_from_ticker(stock)
            print(f"\ncompany name: {company_name}")
            
            # build the output box text senator x bought/sold y shares of z on date
            output = f"Senator {senator} {buy_sell} shares of {company_name} ({stock}) on {date}"
            self.output_box.appendPlainText(output)
            # print(f"stock: {stock}\ndate: {date}")
            
            # specifies red or green for the graph based on sell or buy respectively
            if "sold" in buy_sell.lower():
                i = 0
            else:
                i = 1
                
            graph.Graph_Helpers.graph_it(ui, stock, stock, i, date=date)
        
        # on the 10th click, the easter egg is called. This should be enough times to not be annoying and pop up too often.
        if self.count == 10:
            self.call_bugs_bunny()  
    
    # split T into a list of strings and remove punctuation, numbers, and spaces
    def split_and_strip(self, T) -> list:
        T = T.split()
        T = [re.sub(r'[^\w\s]','',x) for x in T]
        T = [x.replace("_", "") for x in T]
        T = [x for x in T if x != '']
        return T
    
    # clean the search box text and remove spaces, numbers, and punctuation
    def sanitise_search_box_text(self, text) -> str:
        text = self.get_search_box_text()
        text = re.sub(r'[^\w\s]','',text)
        text = text.replace(" ", "")
        text = text.replace("_", "")
        text = text.lower()
        return text
            
    # this code is generated by Qt Designer
    def retranslateUi(self, window): 
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Diego's Capstone Project MSD 2022"))
        self.btn_search.setText(_translate("window", "Search"))
        self.btn_align.setText(_translate("window", "Ticker Distance"))
        self.btn_scrape.setText(_translate("window", "Senate Scraper"))
    
     # Return true if there is an error    
    def has_errors(self) -> bool:
        try: 
            if self.search_box.text() == "" and self.btn_align.isChecked():                                                                                                                # if the searchbox is empty, create an error popup window
                self.error_boilerplate("Error - Search Term", "You have not entered a search term.")
                return True
            #search box is not iterable, so cannot use `if " " in search_box`
            if self.search_box.text() == " " or self.search_box.text() == "  " or self.search_box.text() == "   " or self.search_box.text() == "    ":    
                self.error_boilerplate("Error - Search Term", "Your search cannot contain spaces.")
                return True       
            else:   # no errors, return false
                return False
        except:
            e = sys.exc_info()[0]
            print(f"exception in has errors: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow(MainWindow)   # create an instance of the UI_MainWindow class
    MainWindow.show()
    sys.exit(app.exec_())
    
