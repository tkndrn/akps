from playwright.sync_api import sync_playwright

def find_m3u8():
    with sync_playwright() as p:
        # GitHub ve sunucu ortamları için gerekli argümanlar
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        # Gerçek bir kullanıcı gibi görünmek için context ayarları
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True
        )
        
        page = context.new_page()

        m3u8_links = []

        # Ağ trafiğini hem ana sayfada hem de alt frame'lerde yakala
        def handle_request(request):
            url = request.url
            if ".m3u8" in url or "m3u8" in url.lower():
                if url not in m3u8_links:
                    m3u8_links.append(url)
                    print(f"[+] Bulunan m3u8 Linki: {url}")

        page.on("request", handle_request)
        page.on("response", lambda response: handle_request(response.request))

        print("[-] Siteye bağlanılıyor...")
        try:
            # Hedef sayfaya git
            page.goto("https://beyazelma78.com/kanal/bein-sports-1-fhd", timeout=60000)
            
            print("[-] Sayfa yüklendi, frame'ler ve oynatıcı tetikleniyor...")
            
            # Sayfa yüklenmesi için biraz bekle
            page.wait_for_timeout(5000)

            # Sayfadaki tüm iframe'leri listele ve onlara da tıklama simülasyonu yap
            frames = page.frames
            print(f"[-] Toplam frame/iframe sayısı: {len(frames)}")
            
            for frame in frames:
                try:
                    frame.click("body", timeout=2000)
                except:
                    pass

            # Genel oynatıcı elementlerine tıklama denemesi
            play_selectors = ["video", ".vjs-big-play-button", ".plyr__control--overlaid", "button", ".play-button", "div[id*='player']"]
            for selector in play_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        element.click(timeout=2000)
                        print(f"[+] '{selector}' seçicisine tıklandı.")
                except:
                    continue

            # Akışın yüklenmesi için süreyi biraz uzatalım (20 saniye)
            print("[-] Akışın yakalanması bekleniyor...")
            page.wait_for_timeout(20000)
            
        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

        browser.close()
        
        if not m3u8_links:
            print("[-] Doğrudan m3u8 isteği yakalanamadı. Site bot koruması kullanıyor veya video kaynağı şifrelenmiş olabilir.")

if __name__ == "__main__":
    find_m3u8()
