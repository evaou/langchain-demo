from langchain.tools import BaseTool
from typing import Optional, Type, List
from pydantic import BaseModel, Field
from yf_tool import get_price_change_percent, get_best_performing

class StockPerformanceInputCheck(BaseModel):
    stockticker: str = Field(..., description="Ticker symbol for stock or index")
    days_ago: int = Field(..., description="Int number of days to look back")

class StockPercentageChangeTool(BaseTool):
    name = "get_price_change_percent"
    description = (
        "Useful for when you need to find out the percentage change "
        "in a stock's value. "
        "You should input the stock ticker used on the yfinance API "
        "and also input the "
        "number of days to check the change over"
    )

    def _run(self, stockticker: str, days_ago: int):
        price_change_response = get_price_change_percent(stockticker, days_ago)
        return price_change_response

    def _arun(self, stockticker: str, days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPerformanceInputCheck

class StockBestPerformanceTool(BaseTool):
    name = "get_best_performing"
    description = (
        "Useful for when you need to the performance of multiple "
        "stocks over a period. "
        "You should input a list of stock "
        "tickers used on the yfinance API "
        "and also input the number of days to check the change over"
    )

    def _run(self, stocktickers: List[str], days_ago: int):
        price_change_response = get_best_performing(stocktickers, days_ago)
        return price_change_response

    def _arun(self, stockticker: List[str], days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPerformanceInputCheck
