import requests
import time
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85"
}

# আপনার দেওয়া সেই ২৬টি নির্দিষ্ট OTC পেয়ারের লিস্ট
ALLOWED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc",
    "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc", "EURAUD_otc", "EURCAD_otc",
    "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc", "EURUSD_otc",
    "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc", "GBPJPY_otc", "GBPNZD_otc",
    "GBPUSD_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc",
    "USDCAD_otc", "USDCHF_otc", "USDJPY_otc", "USDBDT_otc", "USDINR_otc"
]

# আপনার লেটেস্ট কনসোল কুকি
COOKIES = {
    "lang": "en",
    "_ga": "GA1.1.453634495.1773337729",
    "__vid1": "89f387f95a92729124e9994373142ae3",
    "activeAccount": "demo",
    "z": '[[ "graph", 2, 0, 0, 0.1786324 ]]'
}

# আপনার লেটেস্ট ইউজার-এজেন্ট
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://qxbroker.com/en/demo-trade"
}

@app.get("/")
def home():
    return {"status": "Active", "total_pairs": len(ALLOWED_PAIRS), "owner": "DARK-X-RAYHAN"}

@app.get("/api/candles")
async def get_candles(pair: str = "USDBDT_otc", count: int = 10):
    # পেয়ার চেক
    if pair not in ALLOWED_PAIRS:
        return {"success": False, "message": f"Pair '{pair}' is not supported. Use valid OTC pairs."}

    try:
        ts = int(time.time())
        url = f"https://qxbroker.com/api/v1/candles-list/{pair}/60/{ts}/{count}"
        
        response = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=15)
        
        # খালি রেসপন্স চেক (আপনার সেই JSON এরর বন্ধ করার জন্য)
        if response.status_code == 200 and response.text.strip():
            raw_data = response.json()
            processed = []
            bd_tz = timezone(timedelta(hours=6))

            for i, c in enumerate(raw_data):
                o, cl = float(c['open']), float(c['close'])
                processed.append({
                    "id": i + 1,
                    "pair": pair,
                    "candle_time": datetime.fromtimestamp(c['at'], tz=bd_tz).strftime("%Y-%m-%d %H:%M:00"),
                    "open": str(o),
                    "high": str(c.get('high', o)),
                    "low": str(c.get('low', cl)),
                    "close": str(cl),
                    "color": "green" if cl > o else "red"
                })
            
            return {
                **OWNER_INFO,
                "success": True,
                "data": processed
            }
        
        # যদি Quotex ব্লক করে থাকে
        return {
            "success": False,
            "error": "Access Denied",
            "msg": "Quotex blocked the request. Please refresh cookies or check server IP."
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
