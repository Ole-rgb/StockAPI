from stock.Stock import Stock


class StockManager:
    """
    A class to manage multiple Stock objects.
    """

    def __init__(self):
        self.stocks = {}

    def get_all_tickers(self):
        """
        Get all the stock tickers.
        Returns:
            A list of stock tickers.
        """
        return list(self.stocks.keys())

    def get_stock_json(self, ticker):
        """
        Get a stock from the manager.
        Parameters:
            ticker: The stock ticker symbol.
        Returns:
            The stock object.
        Raises:
            ValueError: If the stock does not exist in the
        """
        return self.get_stock(ticker).to_json()

    def get_stock(self, ticker):
        """
        Get a stock from the manager.
        Parameters:
            ticker: The stock ticker symbol.
        Returns:
            The stock object.
        Raises:
            ValueError: If the stock does not exist in the list.
        """
        stock = self.stocks.get(ticker)
        if not stock:
            raise ValueError(
                f"Stock '{ticker}' not in list, choose from {list(self.stocks.keys())}"
            )
        return stock

    def add_stock(self, ticker, start_date, end_date):
        """
        Add a new stock to the manager.
        Parameters:
            ticker: The stock ticker symbol.
            start_date: The start date of the stock data.
            end_date: The end date of the stock data.
        Raises:
            ValueError: If the stock already exists in list.
        """
        if ticker in self.stocks:
            raise ValueError(f"Stock '{ticker}' already exists.")
        try:
            self.stocks[ticker] = Stock(ticker, start_date, end_date)
        except ValueError as e:
            raise ValueError(str(e))

    def update_stock(self, ticker):
        """
        Update the stock data.
        Parameters:
            ticker: The stock ticker symbol.
        Raises:
            ValueError: If the stock does not exist in the list.
        """
        stock = self.get_stock(ticker)
        if stock:
            stock.update()
        else:
            raise ValueError(f"Stock '{ticker}' not found.")
        return self.get_stock_json(ticker)

    def delete_stock(self, ticker):
        """
        Removes a stock from the manager.
        Parameters:
            ticker: The stock ticker symbol.
        Raises:
            ValueError: If the stock does not exist in the list.
        """
        if ticker in self.stocks:
            del self.stocks[ticker]
        else:
            raise ValueError(
                f"Stock '{ticker}' can't be deleted: choose from {list(self.stocks.keys())}"
            )
