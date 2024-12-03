# from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# from datetime import date
# from api.stock.StockManager import StockManager
# from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

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
"""
# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite development server
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
"""


# stock_manager = StockManager()


"""
class StockRequest(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol, e.g., AAPL")
    start_date: date = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: date = Field(..., description="End date in YYYY-MM-DD format")
"""


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Stock API"}


# ASGI-Adapter für Serverless-Umgebungen
handler = Mangum(app)
"""
@app.get("/stocks/")
async def get_all_stocks():
    try:
        tickers = stock_manager.get_all_tickers()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(content={"tickers": tickers}, status_code=200)


@app.get("/stocks/{ticker}")
async def get_stock(ticker: str):
    try:
        stock_json = stock_manager.get_stock_json(ticker)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(content=stock_json, status_code=200)


@app.put("/stocks/{ticker}")
async def update_stock(ticker: str):
    try:
        stock_json = stock_manager.update_stock(ticker)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(content=stock_json, status_code=200)


@app.post("/stocks/")
async def add_stock(stock: StockRequest):
    try:
        start_date = stock.start_date.strftime("%Y-%m-%d")
        end_date = stock.end_date.strftime("%Y-%m-%d")
        stock_manager.add_stock(stock.ticker, start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return JSONResponse(
        content=stock_manager.get_stock_json(stock.ticker), status_code=201
    )


@app.delete("/stocks/{ticker}")
async def remove_stock(ticker: str):
    try:
        stock_manager.delete_stock(ticker)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    return JSONResponse(
        content={"message": "Stock deleted", "ticker": ticker}, status_code=200
    )
"""
