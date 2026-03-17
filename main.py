import requests
import time
from fastapi import FastAPI, Query
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85"
}

# আপনার দেওয়া সেই ২৬টি পেয়ারের লিস্ট
ALLOWED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc",
    "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc", "EURAUD_otc", "EURCAD_otc",
    "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc", "EURUSD_otc",
    "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc", "GBPJPY_otc", "GBPNZD_otc",
    "GBPUSD_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc",
    "USDCAD_otc", "USDCHF_otc", "USDJPY_otc", "USDBDT_otc", "USDINR_otc"
]

COOKIES = {
    "lang": "en",
    "_ga": "GA1.1.453634495.1773337729",
    "__vid1": "89f387f95a92729124e9994373142ae3",
    "activeAccount": "demo",
    "z": '[[ "graph", 2, 0, 0, 0.8333333 ]]'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Referer": "https://qxbroker.com/en/demo-trade",
    "Accept": "application/json"
}

@app.get("/")
def home():
    return {"status": "Online", "pairs_supported": len(ALLOWED_PAIRS), **OWNER_INFO}

@app.get("/api/candles")
async def get_quotex_candles(pair: str = "USDBDT_otc", count: int = 10):
    # পেয়ারটি লিস্টে আছে কি না চেক করা
    if pair not in ALLOWED_PAIRS and not pair.endswith("_otc"):
        return {"success": False, "message": "Invalid Pair. Please use valid OTC pairs."}

    try:
        timestamp = int(time.time())
        # Quotex API থেকে ডাটা কল করা
        url = f"https://qxbroker.com/api/v1/candles-list/{pair}/60/{timestamp}/{count}"
        
        response = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            raw_candles = response.json() # Quotex সাধারণত একটি লিস্ট দেয়
            
            processed_data = []
            bd_tz = timezone(timedelta(hours=6))

            # Quotex থেকে আসা ডাটাকে সাজানো
            for i, c in enumerate(raw_candles):
                # Quotex ডাটা ফরম্যাট অনুযায়ী: 'open', 'close', 'high', 'low', 'at'
                open_p = float(c.get('open', 0))
                close_p = float(c.get('close', 0))
                
                color = "green" if close_p > open_p else "red" if close_p < open_p else "doji"
                
                processed_data.append({
                    "id": i + 1,
                    "pair": pair,
                    "candle_time": datetime.fromtimestamp(c['at'], tz=bd_tz).strftime("%Y-%m-%d %H:%M:%00"),
                    "open": str(open_p),
                    "high": str(c.get('high', open_p)),
                    "low": str(c.get('low', close_p)),
                    "close": str(close_p),
                    "color": color
                })

            return {
                **OWNER_INFO,
                "success": True,
                "data": processed_data
            }
        
        return {"success": False, "error": "Forbidden", "msg": "Update Cookies"}

    except Exception as e:
        return {"success": False, "error": str(e)}
