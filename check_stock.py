import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://store.nintendo.co.kr/beeskb6aakor"


def send_telegram(message: str):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(api_url, data={"chat_id": CHAT_ID, "text": message})
    resp.raise_for_status()


def check():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")
        content = page.content()
        browser.close()

    in_stock = "품절" not in content
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
