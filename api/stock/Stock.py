import yfinance as yf
import pandas as pd
from datetime import datetime
import glob
from pathlib import Path
import os


class Stock:
    """
    A class to represent a stock and manage its historical data.

    Attributes:
        ticker (str): The ticker symbol of the stock.
        start_date (str): The start date for the stock data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the stock data in 'YYYY-MM-DD' format.
        data (pd.DataFrame): The historical stock data.

    Methods:
        update():
            Updates the stock data to the latest available data.

        __str__():
            Returns a string representation of the stock with its ticker, start date, and end date.
    """

    def __init__(self, ticker, start_date, end_date):
        self.__valid_ticker(ticker)
        self.ticker = ticker

        self.__valid_date(start_date)
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        self.__valid_date(end_date)
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if start_date_dt >= end_date_dt:
            raise ValueError("Start date must be before end date.")
        self.start_date = start_date
        self.end_date = end_date

        # Dont download, if dataframe exists, with maximum date being greater then the end date
        if (
            self.__stock_download_exists()
            and self.__get_dates_from_filename()[1] >= end_date
        ):
            self.stock_data, _ = self.__get_stock_from_downloads()
            print(f"Stock data already exists: {self.__get_file_path()}")
        else:
            self.stock_data = self.__download_stock_data()

        # Check if the given start_date and end_date equal the dates from the filename
        file_dates = self.__get_dates_from_filename()
        if start_date != file_dates or end_date != file_dates:
            self.__set_start_date(file_dates[0])
            self.__set_end_date(file_dates[1])

    def __del__(self):
        # TODO think about deleting the stock csv to save space
        print(f"Deleting stock")

    def update(self):
        """
        Update the stock data by downloading new data if necessary.
        This method checks if the stock data for a given stock name is already up to date.
        If the data is not up to date, it downloads the new data from the last recorded date
        to the current date and appends it to the existing data.
        Returns:
            None
        """

        # Download the stock data if it does not exist
        if not self.__stock_download_exists():
            self.__download_stock_data()
            return  # {"message": "Stock downloaded, because it did not exist previously"}

        # Download exists, check if up to date
        if self.__download_up_to_date():
            raise ValueError("Stock data is up to date.")

        # Retrieve the existing stock data
        stock_data, dates = self.__get_stock_from_downloads()

        # Get the date difference between the last date in the file and the current date
        last_day_in_file = dates[1]
        today = datetime.now().strftime("%Y-%m-%d")

        # Update the file by appending the new data
        new_data = yf.download(self.get_ticker(), start=last_day_in_file, end=today)
        # new_data = new_data_df.drop(new_data_df.index[[1, 2]])
        # new_data.set_index("Price", inplace=True)

        updated_data = pd.concat([stock_data, new_data])
        metadata_row = pd.DataFrame(
            [["", "", "", "", "", ""]],
            columns=stock_data.columns,  # TODO this is a hack, because I don't know how keep the Date column in the csv file
        )
        updated_data = pd.concat([metadata_row, updated_data])

        # Propagate the new data
        self.__set_stock_data(updated_data)
        updated_data.to_csv(self.__get_file_path())
        self.__update_filename_end_date(today)
        self.__set_end_date(today)

    def __download_stock_data(self):
        """
        Downloads stock data for a given stock within a specified date range and saves it to a CSV file.

        Args:
            ticker (str): The ticker symbol of the stock to download.
            start_date (str): The start date for the data in 'YYYY-MM-DD' format.
            end_date (str): The end date for the data in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: The stock data as a pandas DataFrame.
        """
        # Check if the stock data already exists and is up to date
        if self.__stock_download_exists() and self.__download_up_to_date():
            stock_data, _ = self.__get_stock_from_downloads()
            return stock_data

        # Download stock data
        stock_data = yf.download(
            self.get_ticker(), start=self.get_start_date(), end=self.get_end_date()
        )
        # Create a filename with stock name and timeframe
        file_path = f"{self.__get_data_folder()}/{self.get_ticker()}_{self.get_start_date()}:{self.get_end_date()}.csv"
        # Save the data to a CSV file
        stock_data.to_csv(file_path)
        print(f"Stock data saved to {file_path}")
        return stock_data

    def __stock_download_exists(self):
        """
        Check if the stock data exists in the "data" directory.

        Returns:
            bool: True if the stock data exists, False otherwise.
        """
        return bool(self.__get_filename())

    def __download_up_to_date(self):
        """
        Check if the stock data is up to date.

        Returns:
            bool: True if the stock data is up to date, False otherwise.
        """
        if not self.__stock_download_exists():
            return False

        # update the stock dates from the filename
        self.__set_start_date(self.__get_dates_from_filename()[0])
        self.__set_end_date(self.__get_dates_from_filename()[1])
        # convert the dates to datetime objects
        start_dt = datetime.strptime(self.get_start_date(), "%Y-%m-%d")
        end_dt = datetime.strptime(self.get_end_date(), "%Y-%m-%d")

        return (
            end_dt.date() == datetime.now().date() and end_dt.date() >= start_dt.date()
        )

    def __get_stock_from_downloads(self):
        """
        Retrieve stock data from a downloaded CSV file.
        This function searches for a CSV file in the "data" directory that matches the given ticker.
        If a matching file is found, it reads the CSV file into a pandas DataFrame and extracts the dates
        from the filename.
        Returns:
            tuple: A tuple containing the stock data as a pandas DataFrame and a list of dates extracted from the filename.
                Returns None if no matching file is found.
        """

        if not self.__stock_download_exists():
            print(f"No data found for stock: {self.get_ticker()}")
            return None

        # Read the CSV file
        stock_data = pd.read_csv(
            self.__get_file_path(),
            skiprows=[
                0,
                1,
                2,
            ],
            index_col=0,  # The first column (Date) is used as the index
            parse_dates=True,  # Automatically parse the Date column as datetime
        )
        stock_data.columns = pd.MultiIndex.from_tuples(
            [
                ("Adj Close", self.get_ticker()),
                ("Close", self.get_ticker()),
                ("High", self.get_ticker()),
                ("Low", self.get_ticker()),
                ("Open", self.get_ticker()),
                ("Volume", self.get_ticker()),
            ],
            names=["Price", "Ticker"],
        )  # TODO this is a hack, because I don't know how to get the columns from the csv file

        return stock_data, self.__get_dates_from_filename()

    def __get_filename(self):
        """
        Private method to retrieve the filename of the CSV file associated with the stock ticker.
        This method searches the 'data' directory for files matching the pattern
        '{ticker}_*.csv', where {ticker} is the stock ticker obtained from the
        get_ticker() method. If no such files are found, it returns None. Otherwise,
        it returns the first matching file.
        Returns:
            str or None: The filename of the first matching CSV file, or None if no
            matching files are found.

        """
        files = glob.glob(f"{self.__get_data_folder()}/{self.get_ticker()}_*.csv")

        return os.path.basename(files[0]) if files else None

    def __get_file_path(self):
        """
        Get the full path of the CSV file associated with the stock ticker.

        Returns:
            str: The full path of the CSV file.
        """
        return f"{self.__get_data_folder()}/{self.__get_filename()}"

    def __get_dates_from_filename(self):
        """
        Retrieve the stock dates from the downloaded CSV file.

        Returns:
            list: A list containing the start and end dates extracted from the filename.
        """
        return self.__get_filename().split("_")[1].replace(".csv", "").split(":")

    def get_day(self, date):
        """
        Get the stock data for a specific date.

        Args:
            date (str): The date to retrieve in 'YYYY-MM-DD' format.

        Returns:
            pd.Series: The stock data for the specified date.
        """
        pass

    def get_stock_data(self):
        return self.stock_data

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_ticker(self):
        return self.ticker

    def __set_end_date(self, new_end_date):
        self.__valid_date(new_end_date)
        self.end_date = new_end_date

    def __set_start_date(self, new_start_date):
        self.__valid_date(new_start_date)
        self.end_date = new_start_date

    def __set_stock_data(self, new_stock_data):
        self.__valid_data(new_stock_data)
        self.stock_data = new_stock_data

    def __update_filename_end_date(self, new_end_date):
        new_filename = f"{self.get_ticker()}_{self.get_start_date()}:{new_end_date}.csv"
        os.rename(self.__get_file_path(), f"{self.__get_data_folder()}/{new_filename}")

    def __valid_data(self, date):
        # TODO better validation
        if not isinstance(date, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")
        # if date.index.name != "Date":
        #     raise ValueError("Data must have the Date column as the index.")

    def __valid_date(self, date):
        if not isinstance(date, str):
            raise ValueError("Start date must be a string in 'YYYY-MM-DD' format.")
        if isinstance(date, str):
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Start date must be in 'YYYY-MM-DD' format.")

    def __valid_ticker(self, ticker):
        if not isinstance(ticker, str):
            raise ValueError(
                "Ticker must be a string representing a stock e.g. 'AAPL'."
            )

        stock = yf.Ticker(ticker)
        # Attempt to get historical data (e.g., the last 5 days)
        data = stock.history(period="5d")
        if data.empty:
            raise ValueError("Ticker symbol doesn't match known stock.")

    def __get_data_folder(self):
        script_dir = Path(__file__).parent
        data_folder = script_dir / "data"
        return data_folder

    def __str__(self):
        return f"Stock: {self.get_ticker()}\nStart Date: {self.get_start_date()}\nEnd Date: {self.get_end_date()}"

    def to_json(self):
        """
        Convert the stock data to a JSON format.

        Returns:
            dict: A dictionary containing the stock data in JSON format.
        """
        return {
            "ticker": self.get_ticker(),
            "start_date": self.get_start_date(),
            "end_date": self.get_end_date(),
            "data": self.stock_data.to_json(),  # TODO only return the last 255 days?!
        }


if __name__ == "__main__":
    stock = Stock("AAPL", "2021-01-01", "2021-12-31")
    print(stock)
    stock.update()
    print(stock)
