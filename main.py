from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from datetime import date
from stock.StockManager import StockManager

"""
Stock API

This API allows users to manage stock data, including retrieving, updating, adding, and deleting stock information.

Endpoints:
- GET /: Welcome message for the Stock API.
- GET /stocks/{ticker}: Retrieve stock information for a given ticker symbol.
- PUT /stocks/{ticker}: Update stock information for a given ticker symbol.
- POST /stocks/: Add a new stock with specified ticker symbol and date range.
- DELETE /stocks/{ticker}: Remove stock information for a given ticker symbol.

Example Usage:
- To add a new stock:
    POST /stocks/
    {
        "ticker": "AAPL",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31"
    }

- To get all stock tickers:
    GET /stocks/
    
- To get stock information:
    GET /stocks/AAPL

- To update stock information:
    PUT /stocks/AAPL

- To delete stock information:
    DELETE /stocks/AAPL
"""

app = FastAPI()
stock_manager = StockManager()


class StockRequest(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol, e.g., AAPL")
    start_date: date = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: date = Field(..., description="End date in YYYY-MM-DD format")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock API"}


@app.get("/stocks/")
def get_all_stocks():
    try:
        tickers = stock_manager.get_all_tickers()
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    return {"tickers": tickers}


@app.get("/stocks/{ticker}")
def get_stock(ticker: str):
    try:
        stock_json = stock_manager.get_stock_json(ticker)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    return stock_json


@app.put("/stocks/{ticker}")
def update_stock(ticker: str):
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


"""
@app.get("/stocks/{ticker}/timeframe")
def get_stock_timeframe(ticker: str, days: int):
    try:
        stock_json = stock_manager.get_stock_timeframe(ticker, days)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    return stock_json
"""
