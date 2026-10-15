from playwright.sync_api import sync_playwright

def find_m3u8():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True
        )
        
        page = context.new_page()

        m3u8_links = []

        # Ağ trafiğini ve dönen yanıtları (response içeriğini) incele
        def handle_request(request):
            url = request.url
            if ".m3u8" in url or "m3u8" in url.lower() or "playlist" in url.lower():
                if url not in m3u8_links:
                    m3u8_links.append(url)
                    print(f"[+] Bulunan m3u8/Akış Linki (Request): {url}")

        def handle_response(response):
            try:
                url = response.url
                # JSON veya metin içeriklerinden m3u8 arayalım
                if "json" in response.headers.get("content-type", "") or "text" in response.headers.get("content-type", ""):
                    body = response.text()
                    if ".m3u8" in body:
                        print(f"[+] Yanıt İçeriğinde m3u8 Bulundu! ({url})")
                        # İçerik içindeki linki bulmaya çalışalım
                        for line in body.split():
                            if ".m3u8" in line:
                                clean_line = line.strip('"\'')
                                if clean_line not in m3u8_links:
                                    m3u8_links.append(clean_line)
                                    print(f"    -> Bulunan Link: {clean_line}")
            except:
                pass

        page.on("request", handle_request)
        page.on("response", handle_response)

        print("[-] Siteye bağlanılıyor...")
        try:
            page.goto("https://beyazelma78.com/kanal/bein-sports-1-fhd", timeout=60000)
            
            print("[-] Sayfa yüklendi, frame'ler ve oynatıcı tetikleniyor...")
            page.wait_for_timeout(5000)

            # Frame'lere tıklama simülasyonu
            frames = page.frames
            for frame in frames:
                try:
                    frame.click("body", timeout=2000)
                except:
                    pass

            # Oynatıcı elementlerine tıklama
            play_selectors = ["video", ".vjs-big-play-button", ".plyr__control--overlaid", "button", ".play-button", "div[id*='player']"]
            for selector in play_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        element.click(timeout=2000)
                        print(f"[+] '{selector}' seçicisine tıklandı.")
                except:
                    continue

            # Akışın düşmesi için biraz daha uzun bekleme
            print("[-] Akışın yakalanması bekleniyor...")
            page.wait_for_timeout(20000)
            
        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

        browser.close()
        
        if not m3u8_links:
            print("[-] Doğrudan veya içerikten m3u8 yakalanamadı. Site m3u8 yerine farklı bir protokol (örneğin özel WebSocket veya şifreli token akışı) kullanıyor olabilir.")

if __name__ == "__main__":
    find_m3u8()
