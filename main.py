from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from datetime import date
from stock.StockManager import StockManager

app = FastAPI()
stock_manager = StockManager()


class StockRequest(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol, e.g., AAPL")
    start_date: date = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: date = Field(..., description="End date in YYYY-MM-DD format")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock API"}


@app.get("/stocks/{ticker}")
def get_stock(ticker: str):
    try:
        stock_json = stock_manager.get_stock_json(ticker)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    return stock_json


@app.put("/stocks/{ticker}")
def update_stock(ticker: str):
    # Implementation will follow later
    try:
        stock_json = stock_manager.update_stock(ticker)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    return stock_json


@app.post("/stocks/")
def add_stock(stock: StockRequest):
    try:
        start_date = stock.start_date.strftime("%Y-%m-%d")
        end_date = stock.end_date.strftime("%Y-%m-%d")
        stock_manager.add_stock(stock.ticker, start_date, end_date)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    return stock_manager.get_stock_json(stock.ticker)


@app.delete("/stocks/{ticker}")
def remove_stock(ticker: str):
    try:
        stock_manager.delete_stock(ticker)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    return {"message": "Stock deleted", "ticker": ticker}


'''
@app.get("/stocks/{stock_name}")
# Example request: /stocks/AAPL?start_date=2023-01-01&end_date=2023-01-31
def get_stock_by_time(stock_name: str, start_date: str, end_date: str):
    """
    Endpoint to retrieve stock data for a given stock name within a specified time range.

    Args:
        stock_name (str): The name of the stock to retrieve data for.
        start_date (str): The start date of the time range in 'YYYY-MM-DD' format.
        end_date (str): The end date of the time range in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary containing the stock name, start date, end date, and the stock data within the specified time range.
        If the stock data doesn't exist for the given time range, returns a dictionary with an error message.

    Raises:
        ValueError: If the stock data doesn't exist for the given time range.
    """
    try:
        stock_data = stock_manager.get_stock_by_time(stock_name, start_date, end_date)
        if stock_data:
            return {
                "stock_name": stock_name,
                "start_date": start_date,
                "end_date": end_date,
                "data": stock_data,
            }
    except ValueError:
        return {
            "stock_name": stock_name,
            "data": "Stock data doesn't exist for the given time range",
        }
'''
