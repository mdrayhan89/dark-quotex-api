import os
import random
from fastapi import FastAPI, Query
from quotexapi.stable_api import Quotex
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# .env ফাইল লোড করা (লোকাল টেস্টিং এর জন্য)
load_dotenv()

app = FastAPI()

# আপনার ব্র্যান্ডিং ডাটা
OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85",
    "Channel": "https://t.me/mdrayhan85"
}

# আপনার দেওয়া নির্দিষ্ট পেয়ারের লিস্ট
SUPPORTED_PAIRS = [
    "AUDNZD_otc", "AXP_otc", "BRLUSD_otc", "BTCUSD_otc", "EURNZD_otc",
    "EURSGD_otc", "INTC_otc", "JNJ_otc", "MCD_otc", "MSFT_otc",
    "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc", "PFE_otc",
    "USDBDT_otc", "USDCOP_otc", "USDDZD_otc", "USDEGP_otc", "USDIDR_otc",
    "USDINR_otc", "USDMXN_otc", "USDNGN_otc", "USDPKR_otc", "USDTRY_otc",
    "USDZAR_otc", "XAUUSD_otc"
]

# Render ড্যাশবোর্ড থেকে এই Variables গুলো সেট করবেন
EMAIL = os.getenv("QUOTEX_EMAIL", "trrayhan786@gmail.com")
PASSWORD = os.getenv("QUOTEX_PASSWORD", "Mdrayhan@655")

# Quotex কানেকশন সেটআপ
client = Quotex(email=EMAIL, password=PASSWORD)

def check_and_connect():
    if not client.check_connect():
        client.connect()
    return client.check_connect()

@app.get("/")
def home():
    return {"status": "Active", "owner": "DARK-X-RAYHAN", "supported_pairs_count": len(SUPPORTED_PAIRS)}

@app.get("/api/candles")
async def get_candles(pair: str = Query("USDBDT_otc"), count: int = Query(10)):
    # পেয়ার ভ্যালিডেশন
    if pair not in SUPPORTED_PAIRS:
        return {"success": False, "message": f"Pair '{pair}' is not in your supported list."}

    if not check_and_connect():
        return {"success": False, "message": "Failed to connect to Quotex. Check credentials or 2FA."}

    try:
        # ১ মিনিট (60 sec) এর ক্যান্ডেল ডাটা ফেচ করা
        # বর্তমান টাইমস্ট্যাম্প থেকে ডাটা নেওয়া শুরু হবে
        candles = client.get_candles(pair, 60, count, datetime.now().timestamp())
        
        final_data = []
        bd_timezone = timezone(timedelta(hours=6)) # বাংলাদেশ সময় (UTC+6)
        
        for i, c in enumerate(candles):
            open_p = c['open']
            close_p = c['close']
            color = "green" if close_p > open_p else "red" if close_p < open_p else "doji"
            
            # টাইম কনভার্ট (বাংলাদেশ সময় অনুযায়ী)
            candle_dt = datetime.fromtimestamp(c['at'], tz=bd_timezone)

            candle_struct = {
                "id": str(i + 1),
                "pair": pair,
                "timeframe": "M1",
                "candle_time": candle_dt.strftime("%Y-%m-%d %H:%M:00"),
                "open": str(open_p),
                "high": str(c['max']),
                "low": str(c['min']),
                "close": str(close_p),
                "volume": str(int(c.get('volume', 0))),
                "color": color,
                "created_at": datetime.now(bd_timezone).strftime("%Y-%m-%d %H:%M:%S")
            }
            final_data.append(candle_struct)

        return {
            **OWNER_INFO,
            "success": True,
            "count": len(final_data),
            "data": final_data
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
