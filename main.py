import requests
import time
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta

app = FastAPI()

# আপনার সেই ২৬+ পেয়ারের লিস্ট
ALLOWED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc",
    "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc", "EURAUD_otc", "EURCAD_otc",
    "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc", "EURUSD_otc",
    "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc", "GBPJPY_otc", "GBPNZD_otc",
    "GBPUSD_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc", "NZDUSD_otc",
    "USDCAD_otc", "USDCHF_otc", "USDJPY_otc", "USDBDT_otc", "USDINR_otc"
]

# আপনার লেটেস্ট কনসোল কুকি ও ইউজার এজেন্ট
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

# --- প্রক্সি সেটিংস ---
# এখানে আপনার প্রক্সি আইপি এবং পোর্ট বসান (উদাহরণ স্বরূপ নিচে একটি দেওয়া হলো)
PROXIES = {
    "http": "http://username:password@proxy_ip:port",
    "https": "http://username:password@proxy_ip:port"
}

@app.get("/api/candles")
async def get_candles(pair: str = "USDBDT_otc", count: int = 10):
    if pair not in ALLOWED_PAIRS:
        return {"success": False, "message": "Invalid Pair"}

    try:
        ts = int(time.time())
        url = f"https://qxbroker.com/api/v1/candles-list/{pair}/60/{ts}/{count}"
        
        # proxies=PROXIES যোগ করা হয়েছে যাতে রেন্ডার সার্ভারের আইপি লুকিয়ে রাখা যায়
        response = requests.get(url, cookies=COOKIES, headers=HEADERS, proxies=PROXIES, timeout=15)
        
        if response.status_code == 200 and response.text.strip():
            raw_data = response.json()
            processed = []
            bd_tz = timezone(timedelta(hours=6))

            for i, c in enumerate(raw_data):
                o, cl = float(c['open']), float(c['close'])
                processed.append({
                    "id": i + 1,
                    "pair": pair,
                    "candle_time": datetime.fromtimestamp(c['at'], tz=bd_tz).strftime("%H:%M:00"),
                    "open": str(o),
                    "close": str(cl),
                    "color": "green" if cl > o else "red"
                })
            return {"success": True, "data": processed}
        
        return {"success": False, "error": "Proxy or Cookies failed", "status": response.status_code}

    except Exception as e:
        return {"success": False, "error": str(e)}
