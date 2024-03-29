from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from yf_tool import get_stock_price

class StockPriceInputCheck(BaseModel):
    stockticker: str = Field(..., description="Ticker symbol for stock or index")

class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    description = (
        "Useful for when you need to find out the price of stock. "
        "You should input the stock ticker used on the yfinance API"
    )

    def _run(self, stockticker: str):
        price_response = get_stock_price(stockticker)
        return price_response

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPriceInputCheck
