from fastapi import FastAPI, __version__, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from stock.StockManager import StockManager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite development server
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


stock_manager = StockManager()


class StockRequest(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol, e.g., AAPL")
    start_date: date = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: date = Field(..., description="End date in YYYY-MM-DD format")


@app.get("/")
async def root():
    html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>FastAPI on Vercel</title>
            </head>
            <body>
                <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
                    <h1>Hello from FastAPI@{__version__}</h1>
                    <ul>
                        <li><a href="/docs">/docs</a></li>
                    </ul>
                    <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
                </div>
            </body>
        </html>
        """
    return HTMLResponse(html)


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
