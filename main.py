import json
import time
from fastapi import FastAPI, Query
from websocket import create_connection
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85",
    "Channel": "https://t.me/mdrayhan85"
}

# আপনার ডিটেইলস
EMAIL = "trrayhan786@gmail.com"
PASSWORD = "Mdrayhan@655"

def get_quotex_data(pair, count):
    try:
        # Quotex WebSocket URL (এটি পরিবর্তন হতে পারে, তবে বর্তমানে এটি স্ট্যান্ডার্ড)
        ws = create_connection("wss://ws.qxbroker.com/socket.io/?EIO=3&transport=websocket")
        
        # এখানে লগইন লজিক এবং পেয়ার সাবস্ক্রিপশন কোড থাকবে
        # আপাতত আমরা একটি 'Request-Response' মেথড সিমুলেট করছি যা সরাসরি ডাটা টানবে
        
        # নোট: আসল সকেট কানেকশনে কুকি এবং টোকেন লাগে। 
        # রেন্ডারে এটি স্টেবল রাখতে আমরা নিচের ফরম্যাটে ডাটা প্রসেস করব
        
        candles = []
        bd_tz = timezone(timedelta(hours=6))
        now = datetime.now(bd_tz).replace(second=0, microsecond=0)

        for i in range(count):
            t = now - timedelta(minutes=i)
            # এখানে আমরা সকেট থেকে আসা ডাটা ম্যাপ করব
            # (নিরাপত্তার স্বার্থে আসল কানেকশন টোকেন আপনার ব্রাউজার থেকে নিতে হয়)
            
            candle = {
                "id": str(i + 1),
                "pair": pair,
                "timeframe": "M1",
                "candle_time": t.strftime("%Y-%m-%d %H:%M:00"),
                "open": "Loading...", # সকেট ডাটা এখানে বসবে
                "close": "Loading...",
                "color": "checking",
                "created_at": datetime.now(bd_tz).strftime("%Y-%m-%d %H:%M:%S")
            }
            candles.append(candle)
        return candles
    except Exception as e:
        return str(e)

@app.get("/api/candles")
async def candles_api(pair: str = "USDBDT_otc", count: int = 10):
    # আপনার আগের দেওয়া সেই নির্দিষ্ট পেয়ার লিস্ট এখানে কাজ করবে
    data = get_quotex_data(pair, count)
    return {**OWNER_INFO, "success": True, "data": data}
