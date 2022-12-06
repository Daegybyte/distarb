import pendulum
import alignment_helpers as alignment
import yfinance as yf
import logging
import pyqtgraph as pg


class Graph_Helpers():
    def __init__(self, window):
        TICKERS = alignment.Helpers.get_TICKERS()
        self.TICKERS = TICKERS
        COMPANIES = alignment.Helpers.get_COMPANIES()
        self.COMPANIES = COMPANIES
        # DROPDOWN_ITEMS = TICKERS
    
    # enumerate r,g,b values
    # @classmethod
    def set_colour(i):        # i is sets the color of the graph line to rgb
        colours = ['r', 'g', 'b', 'w']
        return colours[i]
                
        
    def graph_it(window, ticker, company, i, date):
        # window.graph_widget.setMouseEnabled(x=False, y=False)                          # make graph unadjustable
        print(f"ticker: {ticker}")
        if date is None:
            price_history = yf.Ticker(ticker).history( period='1y',                    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                                        interval='1wk', actions=False) # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo 
        else: 
            t = Graph_Helpers.convert_date_to_epoch(date)
            window.graph_widget.addLine(x=t, pen='b', name='Transaction Date')                      # place a vertical line on the graph to show the date of the transaction

            date = Graph_Helpers.make_four_weeks_earier(date)                                       # make the date 4 weeks earlier to give the graph some context
            price_history = yf.Ticker(ticker).history(start=date, interval='1d', actions=False)
        
        opens = list(price_history['Open'])  # get open price for each day
        
        # normalise the data beyond 0-1 to keep stocks of different prices on the same graph
        max_price = max(opens)
        min_price = min(opens)
        try:
            opens = [(x-min_price)/(max_price-min_price) for x in opens]
        except ZeroDivisionError:
            logging.error(f"ZeroDivisionError: {ticker}")
            print("ZeroDivisionError")
             
        dt_list = [pendulum.parse(str(dt)).float_timestamp for dt in list(price_history.index)]      # convert pandas datetime to float timestamp
        converted_dates = Graph_Helpers.convert_epoch_to_date(dt_list)                               # convert float timestamp to date string
        zipped = Graph_Helpers.zip_lists_to_dict(dt_list, converted_dates)                           # zip the dates and prices together into a dictionary
        
        colour = Graph_Helpers.set_colour(i) # set the colour of the graph line
        print(f"colour: {i}\n type: {type(i)}")
        
        # format the graph
        plt = window.graph_widget.plot(dt_list, opens, name=company, symbolSize=5, pen=colour, symbolBrush=colour, lineStyle='dashed')
        window.graph_widget.setLabel('left', 'Normalised Price, 0-1')
        window.graph_widget.setLabel('bottom', 'Date', units='Date')
        window.graph_widget.setXRange(dt_list[0], dt_list[-1])

        # set the ticks on the x axis to be the date
        try:
            window.graph_widget.getAxis('bottom').setTicks([list(zipped.items())[4:-1:len(converted_dates)//3]]) # start is adjusted to fit the graph window better
        except ValueError:
            window.output_box.appendPlainText(f"\nIt is likely that {ticker} is a side issuing of a stock. That is why one or more of the graph lines is not showing up, because the price data would be identical, but the privilieges i.e. voting rights would be different.")
            logging.error(f"ValueError: {ticker}")
            print("ValueError")
        
        window.graph_widget.setYRange(min(opens), max(opens))
        window.graph_widget.showGrid(x=True, y=True)
        
        print ("\nplotting...")
        window.graph_widget.addItem(plt)
        print ("done plotting...")

    # clear the graph
    def reset_graph(self):
        print("resetting graph...")
        self.graph_widget.clear()
        self.graph_widget.setTitle("")
        self.graph_widget.setLabel('left', 'Normalised Price, 0-1', units='$')
        self.graph_widget.setLabel('bottom', 'Date', units='Date')
        self.graph_widget.setXRange(0, 1)
        self.graph_widget.setYRange(0, 1)
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.addLegend()
        self.graph_widget.show()
        
    #returns a date string 4 weeks earlier than the date string passed in format "YYYY-MM-DD"
    def make_four_weeks_earier(date) -> str:
        date = pendulum.parse(date)
        date = date.subtract(weeks=4)
        return date.to_date_string()
        
    # convert a list of epoch floats to a list of strings in the format of "YYYY-MM-DD"
    def convert_epoch_to_date(epoch_list) -> list:
        date_list = []
        for epoch in epoch_list:
            date = pendulum.from_timestamp(epoch).to_date_string()
            date_list.append(date)
        return date_list
    
    # convert a string in the format of "YYYY-MM-DD" to a float in the format of epoch time
    def convert_date_to_epoch(date) -> float:
        date = pendulum.parse(date)
        epoch = date.float_timestamp
        return epoch
    
    # zip two lists together and return a dictionary
    def zip_lists_to_dict(list1, list2) -> dict:
        return dict(zip(list1, list2))
 
if __name__ == "__main__":
    pass