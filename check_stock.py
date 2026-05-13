import requests
import os
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://store.nintendo.co.kr/beeskb6aakor"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def send_telegram(message: str):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(api_url, data={"chat_id": CHAT_ID, "text": message})
    resp.raise_for_status()


def check():
    resp = requests.get(URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    in_stock = "품절" not in resp.text
    if in_stock:
        send_telegram(
            "🚨 닌텐도 스위치 2 재입고!\n"
            f"👉 {URL}"
        )
        print("재입고 감지 - 텔레그램 알림 전송 완료")
    else:
        print("현재 품절 상태")


if __name__ == "__main__":
    check()
