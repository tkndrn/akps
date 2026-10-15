
from playwright.sync_api import sync_playwright

TARGET_URL = "https://ronaldo.magnitude.workers.dev/?url=https://beyazelma78.com/kanal/bein-sports-1-fhd"

def find_m3u8():
    found_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_request(request):
            url = request.url
            if ".m3u8" in url and url not in found_links:
                found_links.append(url)
                print(f"[+] Bulunan m3u8: {url}", flush=True)

        page.on("request", handle_request)

        try:
            print("[-] Siteye bağlanılıyor...", flush=True)
            page.goto(
                TARGET_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )
            page.wait_for_timeout(10000)

        except Exception as e:
            print(f"[!] Hata: {e}", flush=True)

        finally:
            browser.close()

    if not found_links:
        print(
            "[-] Bu çalıştırmada m3u8 isteği yakalanamadı.",
            flush=True
        )

if __name__ == "__main__":
    find_m3u8()
