
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import os
import sys

TARGET_URL = os.getenv(
    "TARGET_URL",
    "https://beyazelma78.com/kanal/bein-sports-1-fhd"
)

found_links = set()

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def on_request(request):
            url = request.url
            parsed = urlparse(url)

            if ".m3u8" in parsed.path.lower():
                if url not in found_links:
                    found_links.add(url)
                    print("[M3U8]", url, flush=True)

        page.on("request", on_request)

        try:
            print("[INFO] Siteye bağlanılıyor...", flush=True)

            response = page.goto(
                TARGET_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            status = response.status if response else 0
            print(f"[HTTP] {status}", flush=True)
            print(f"[TITLE] {page.title()}", flush=True)

            if status == 403 or "Just a moment" in page.title():
                print(
                    "[UYARI] Cloudflare erişimi engelledi. "
                    "İzinli erişim yöntemi gerekiyor.",
                    flush=True
                )
                return

            page.wait_for_timeout(20000)

            if found_links:
                with open(
                    "m3u8_result.txt", "w", encoding="utf-8"
                ) as f:
                    for link in sorted(found_links):
                        f.write(link + "\n")

                print(
                    f"[OK] {len(found_links)} bağlantı bulundu.",
                    flush=True
                )
            else:
                print(
                    "[SONUC] M3U8 isteği yakalanamadı.",
                    flush=True
                )

        except Exception as e:
            print(f"[HATA] {e}", flush=True)
            sys.exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
