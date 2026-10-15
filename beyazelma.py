from playwright.sync_api import sync_playwright

def find_m3u8():
    with sync_playwright() as p:
        # GitHub ve sunucu ortamları için gerekli argümanlar
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()

        m3u8_links = []

        # Ağ trafiğini dinle (Hem request hem response ekledik ki kaçmasın)
        def handle_request(request):
            if ".m3u8" in request.url:
                if request.url not in m3u8_links:
                    m3u8_links.append(request.url)
                    print(f"[+] Bulunan m3u8 Linki: {request.url}")

        page.on("request", handle_request)
        page.on("response", lambda response: handle_request(response.request))

        print("[-] Siteye bağlanılıyor...")
        try:
            # Hedef sayfaya git
            page.goto("https://beyazelma78.com/kanal/bein-sports-1-fhd", timeout=60000)
            
            print("[-] Sayfa yüklendi, oynatıcı tetikleniyor...")
            
            # 1. Sayfa içindeki olası boşluklara veya body'ye tıklayarak etkileşim yarat
            try:
                page.click("body", timeout=3000)
            except:
                pass

            # 2. Videonun yüklenip tetiklenmesi için biraz daha uzun bekleyelim ve tıklama simüle edelim
            play_selectors = ["video", ".vjs-big-play-button", ".plyr__control--overlaid", "button", ".play-button", "iframe"]
            for selector in play_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        element.click(timeout=2000)
                        print(f"[+] '{selector}' seçicisine tıklandı.")
                except:
                    continue

            # Akışın düşmesi için 15 saniye verelim
            page.wait_for_timeout(15000)
            
        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

        browser.close()
        
        if not m3u8_links:
            print("[-] Doğrudan m3u8 isteği yakalanamadı. Site korumalı olabilir veya oynatıcıya manuel tıklamak gerekebilir.")

if __name__ == "__main__":
    find_m3u8()
