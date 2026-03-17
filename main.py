import os
from fastapi import FastAPI, Query
from datetime import datetime
import random

app = FastAPI()

# আপনার ব্র্যান্ডিং তথ্য
OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85",
    "Channel": "https://t.me/mdrayhan85"
}

# সাপোর্ট করা পেয়ারের তালিকা
SUPPORTED_PAIRS = [
    "AUDNZD_otc", "AXP_otc", "BRLUSD_otc", "BTCUSD_otc", "EURNZD_otc",
    "EURSGD_otc", "INTC_otc", "JNJ_otc", "MCD_otc", "MSFT_otc",
    "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc", "PFE_otc",
    "USDBDT_otc", "USDCOP_otc", "USDDZD_otc", "USDEGP_otc", "USDIDR_otc",
    "USDINR_otc", "USDMXN_otc", "USDNGN_otc", "USDPKR_otc", "USDTRY_otc",
    "USDZAR_otc", "XAUUSD_otc"
]

@app.get("/")
def home():
    return {"message": "API is running", "dev": "DARK-X-RAYHAN"}

@app.get("/api/candles")
async def get_candles(pair: str = Query("USDBDT_otc"), count: int = Query(10)):
    # পেয়ার ভ্যালিডেশন
    if pair not in SUPPORTED_PAIRS:
        return {"success": False, "message": f"Pair '{pair}' is not supported."}

    try:
        candle_list = []
        for i in range(count):
            # এখানে আপনার Quotex Library থেকে ডাটা আসবে। 
            # আপাতত ফরম্যাট ঠিক রাখার জন্য ডামি ডাটা জেনারেট করা হয়েছে।
            o = round(random.uniform(120, 130), 3)
            c = round(random.uniform(120, 130), 3)
            h = max(o, c) + 0.010
            l = min(o, c) - 0.010
            
            color = "green" if c > o else "red" if c < o else "doji"

            candle = {
                "id": str(i + 1),
                "pair": pair,
                "timeframe": "M1",
                "candle_time": datetime.now().strftime("%Y-%m-%d %H:%M:00"),
                "open": str(o),
                "high": str(h),
                "low": str(l),
                "close": str(c),
                "volume": str(random.randint(10, 100)),
                "color": color,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            candle_list.append(candle)

        return {
            **OWNER_INFO,
            "success": True,
            "count": len(candle_list),
            "data": candle_list
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
