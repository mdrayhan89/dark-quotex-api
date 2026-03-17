import requests
import time
from fastapi import FastAPI, Query
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85"
}

# আপনার কনসোল থেকে পাওয়া লেটেস্ট তথ্য
COOKIES = {
    "lang": "en",
    "_ga": "GA1.1.453634495.1773337729",
    "__vid1": "89f387f95a92729124e9994373142ae3",
    "activeAccount": "demo",
    "z": '[[ "graph", 2, 0, 0, 0.1786324 ]]'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Referer": "https://qxbroker.com/en/demo-trade",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

# আপনার সেই ২৬+ পেয়ারের লিস্ট
ALLOWED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc",
    "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc", "EURAUD_otc", "EURCAD_otc",
    "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc", "EURUSD_otc",
    "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc", "GBPJPY_otc", "GBPNZD_otc",
    "GBPUSD_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc",
    "USDCAD_otc", "USDCHF_otc", "USDJPY_otc", "USDBDT_otc", "USDINR_otc"
]

@app.get("/")
def status():
    return {"status": "Live", "dev": "DARK-X-RAYHAN"}

@app.get("/api/candles")
async def get_candles(pair: str = "USDBDT_otc", count: int = 10):
    if pair not in ALLOWED_PAIRS:
        return {"success": False, "message": "Invalid Pair"}

    try:
        # সরাসরি Quotex API থেকে ডাটা কল
        ts = int(time.time())
        url = f"https://qxbroker.com/api/v1/candles-list/{pair}/60/{ts}/{count}"
        
        response = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=12)
        
        # যদি Quotex সাকসেসফুল ডাটা দেয়
        if response.status_code == 200:
            raw_data = response.json()
            processed = []
            bd_tz = timezone(timedelta(hours=6))

            for i, c in enumerate(raw_data):
                o, c_val = float(c['open']), float(c['close'])
                processed.append({
                    "id": i + 1,
                    "pair": pair,
                    "time": datetime.fromtimestamp(c['at'], tz=bd_tz).strftime("%H:%M:00"),
                    "open": str(o),
                    "close": str(c_val),
                    "high": str(c['high']),
                    "low": str(c['low']),
                    "color": "green" if c_val > o else "red"
                })
            return {**OWNER_INFO, "success": True, "source": "Quotex_Live", "data": processed}

        # যদি ব্লক করে বা এরর দেয় (Fallback লজিক)
        else:
            return {
                "success": False, 
                "error": "Access Denied by Quotex",
                "status": response.status_code,
                "solution": "Update cookies in main.py immediately"
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
