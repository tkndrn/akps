

from playwright.sync_api import sync_playwright

TARGET_URL = "https://beyazelma78.com/kanal/bein-sports-1-fhd"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        found = set()

        # Ana sayfa ve iframe isteklerini izle
        def on_request(request):
            url = request.url
            if ".m3u8" in url.lower():
                found.add(url)
                print("[M3U8]", url, flush=True)

        def on_response(response):
            url = response.url
            if "beyazelma78.com" in url:
                print(
                    "[SITE RESPONSE]",
                    response.status,
                    url,
                    flush=True
                )

        def on_failed(request):
            print(
                "[REQUEST FAILED]",
                request.url,
                request.failure,
                flush=True
            )

        page.on("request", on_request)
        page.on("response", on_response)
        page.on("requestfailed", on_failed)

        try:
            print("[1] Site açılıyor...", flush=True)

            response = page.goto(
                TARGET_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("[2] HTTP durumu:",
                  response.status if response else "Yanıt yok",
                  flush=True)

            print("[3] Sayfa başlığı:",
                  page.title(),
                  flush=True)

            print("[4] Sayfa adresi:",
                  page.url,
                  flush=True)

            print("[5] Iframe sayısı:",
                  len(page.frames),
                  flush=True)

            for frame in page.frames:
                print("[FRAME]", frame.url, flush=True)

            print("[6] 20 saniye bekleniyor...", flush=True)
            page.wait_for_timeout(20000)

            print("[SONUC] Bulunan M3U8:", len(found), flush=True)

            if not found:
                print(
                    "[BILGI] Bu oturumda M3U8 isteği görülmedi.",
                    flush=True
                )

        except Exception as e:
            print("[HATA]", repr(e), flush=True)

        finally:
            browser.close()

if __name__ == "__main__":
    main()

