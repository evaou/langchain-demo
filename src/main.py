import os
import sys
import aiohttp

from fastapi import Request, FastAPI, HTTPException

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

from stock_price import StockPriceTool
from stock_performance import StockPercentageChangeTool, StockBestPerformanceTool

from linebot import AsyncLineBotApi, WebhookParser
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
linebot_api = AsyncLineBotApi(channel_access_token, async_http_client)
linebot_parser = WebhookParser(channel_secret)

langchain_model = ChatOpenAI(model="gpt-3.5-turbo-0613")
langchain_tools = [StockPriceTool(), StockPercentageChangeTool(), StockBestPerformanceTool()]
langchain_agent = initialize_agent(langchain_tools, langchain_model, agent=AgentType.OPENAI_FUNCTIONS)

@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    body = await request.body()
    body = body.decode()

    try:
        events = linebot_parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        result = langchain_agent.run(event.message.text)

        await linebot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )

    return 'OK'

@app.get("/hello")
async def hello():
    return {"message": "Hello!"}
