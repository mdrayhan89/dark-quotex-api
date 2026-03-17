import requests
import time
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta

app = FastAPI()

OWNER_INFO = {
    "Owner_Developer": "DARK-X-RAYHAN",
    "Telegram": "@mdrayhan85"
}

# আপনার সেই ২৬+ নির্দিষ্ট OTC পেয়ারের লিস্ট
ALLOWED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc",
    "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc", "EURAUD_otc", "EURCAD_otc",
    "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc", "EURUSD_otc",
    "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc", "GBPJPY_otc", "GBPNZD_otc",
    "GBPUSD_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc",
    "USDCAD_otc", "USDCHF_otc", "USDJPY_otc", "USDBDT_otc", "USDINR_otc"
]

# আপনার কনসোল থেকে পাওয়া লেটেস্ট ডাটা
COOKIES = {
    "lang": "en",
    "_ga": "GA1.1.453634495.1773337729",
    "__vid1": "89f387f95a92729124e9994373142ae3",
    "activeAccount": "demo",
    "z": '[[ "graph", 2, 0, 0, 0.1786324 ]]'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://qxbroker.com/en/demo-trade"
}

# --- প্রক্সি সেটিংস (কাজ না করলে শুধু IP:PORT পরিবর্তন করবেন) ---
proxy_url = "http://67.201.33.10:25283" 

PROXIES = {
    "http": proxy_url,
    "https": proxy_url
}

@app.get("/")
def home():
    return {"status": "Active", "owner": "DARK-X-RAYHAN", "proxy_status": "Enabled"}

@app.get("/api/candles")
async def get_candles(pair: str = "USDBDT_otc", count: int = 10):
    if pair not in ALLOWED_PAIRS:
        return {"success": False, "message": f"Pair {pair} is not in allowed list."}

    try:
        ts = int(time.time())
        url = f"https://qxbroker.com/api/v1/candles-list/{pair}/60/{ts}/{count}"
        
        # প্রক্সি এবং কুকি সহ রিকোয়েস্ট
        response = requests.get(url, cookies=COOKIES, headers=HEADERS, proxies=PROXIES, timeout=20)
        
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
        
        return {
            "success": False,
            "error": "Access Denied or Proxy Failed",
            "status_code": response.status_code,
            "msg": "Try changing the proxy_url in code."
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
