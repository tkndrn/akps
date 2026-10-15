from playwright.sync_api import sync_playwright

def find_m3u8():
    with sync_playwright() as p:
        # GitHub Actions (Linux) ortamında Cloudflare'e yakalanmamak için stealth argümanları
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--start-maximized"
            ]
        )
        
        # Gerçek bir kullanıcı gibi görünmek için context ayarları
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="tr-TR",
            timezone_id="Europe/Istanbul",
            extra_http_headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1"
            }
        )
        
        page = context.new_page()

        # Bot algılama mekanizmalarını (navigator.webdriver) bypass et
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        m3u8_links = []

        def handle_request(request):
            url = request.url
            if ".m3u8" in url or "m3u8" in url.lower():
                if url not in m3u8_links:
                    m3u8_links.append(url)
                    print(f"[+] Bulunan m3u8 Linki: {url}")

        page.on("request", handle_request)
        page.on("response", lambda response: handle_request(response.request))

        print("[-] Siteye bağlanılıyor (Cloudflare koruması için bekleniyor)...")
        try:
            # Sayfaya git ve Cloudflare'in yüklenmesi için biraz şans tanı
            page.goto("https://beyazelma78.com/kanal/bein-sports-1-fhd", timeout=60000, wait_until="domcontentloaded")
            
            # Cloudflare meydan okumasını (challenge) aşmak için 8-10 saniye bekleme
            page.wait_for_timeout(10000)
            
            print("[-] Sayfa yüklendi, oynatıcı tetikleniyor...")
            
            # Oynatıcı elementlerine tıklama
            play_selectors = ["video", ".vjs-big-play-button", ".plyr__control--overlaid", "button", ".play-button", "div[id*='player']"]
            for selector in play_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        element.click(timeout=2000)
                except:
                    continue

            # Akışın düşmesi için süre
            page.wait_for_timeout(15000)
            
        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

        browser.close()
        
        if not m3u8_links:
            print("[-] Doğrudan m3u8 isteği yakalanamadı. GitHub IP'leri Cloudflare tarafından engelleniyor olabilir.")
        else:
            print("\n[✔] İşlem Başarılı! Bulunan linkler:")
            for link in m3u8_links:
                print(link)

if __name__ == "__main__":
    find_m3u8()
