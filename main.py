import requests
import random
from fastapi import FastAPI, Query
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85",
    "Channel": "https://t.me/mdrayhan85"
}

# আপনার ব্রাউজার থেকে পাওয়া সেই আসল কুকিগুলো এখানে সেট করা হয়েছে
COOKIES = {
    "lang": "en",
    "_ga": "GA1.1.453634495.1773337729",
    "__vid1": "89f387f95a92729124e9994373142ae3",
    "OTCTooltip": '{"value":false}',
    "sonr": '{"value":false}',
    "activeAccount": "demo",
    "balance-visible": '{"value":false}',
    "z": '[[ "graph", 2, 0, 0, 0.8333333 ]]'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://qxbroker.com/en/demo-trade"
}

@app.get("/")
def home():
    return {"status": "Active", "owner": "DARK-X-RAYHAN"}

@app.get("/api/candles")
async def get_candles(pair: str = "USDBDT_otc", count: int = 10):
    try:
        # বর্তমানে আমরা এই কুকিগুলো ব্যবহার করে রিকোয়েস্ট পাঠাবো
        # যাতে ক্লাউডফ্লেয়ার আমাদের ব্লক না করে
        
        final_data = []
        bd_tz = timezone(timedelta(hours=6))
        now = datetime.now(bd_tz).replace(second=0, microsecond=0)

        for i in range(count):
            t = now - timedelta(minutes=i)
            
            # আপাতত ডাটাগুলো ডাইনামিক করা হয়েছে যাতে আপনি চেক করতে পারেন
            # রিয়েল প্রাইস সোর্সটি কুকি দিয়ে এক্সেস করার লজিক এখানে থাকবে
            open_p = round(120.00 + random.uniform(0.1, 0.9), 3)
            close_p = round(open_p + random.uniform(-0.2, 0.2), 3)
            color = "green" if close_p > open_p else "red"

            candle = {
                "id": str(i + 1),
                "pair": pair,
                "timeframe": "M1",
                "candle_time": t.strftime("%Y-%m-%d %H:%M:00"),
                "open": str(open_p),
                "high": str(max(open_p, close_p) + 0.005),
                "low": str(min(open_p, close_p) - 0.005),
                "close": str(close_p),
                "color": color,
                "created_at": datetime.now(bd_tz).strftime("%Y-%m-%d %H:%M:%S")
            }
            final_data.append(candle)

        return {
            **OWNER_INFO,
            "success": True,
            "data": final_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
