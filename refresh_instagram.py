from playwright.sync_api import sync_playwright
import os

INSTAGRAM_USERNAME = "kaam41313"
INSTAGRAM_PASSWORD = "Data@1122"

def refresh_session():
    cookies_dir = os.path.join(os.path.dirname(__file__), "cookies")
    os.makedirs(cookies_dir, exist_ok=True)
    json_path = os.path.join(cookies_dir, "instagram.json")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=json_path)
        page = context.new_page()
        page.goto("https://www.instagram.com", timeout=60000)
        context.storage_state(path=json_path)
        browser.close()
        print("✅ Refreshed instagram.json")

if __name__ == "__main__":
    refresh_session()
