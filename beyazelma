from playwright.sync_api import sync_playwright

def find_m3u8():
    with sync_playwright() as p:
        # GitHub ve sunucu ortamları için gerekli argümanlar eklendi
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()

        m3u8_links = []

        # Ağ trafiğini dinle
        def handle_request(request):
            if ".m3u8" in request.url:
                if request.url not in m3u8_links:
                    m3u8_links.append(request.url)
                    print(f"[+] Bulunan m3u8 Linki: {request.url}")

        page.on("request", handle_request)

        print("[-] Siteye bağlanılıyor...")
        try:
            # Orijinal hedef sayfanız
            page.goto("https://beyazelma78.com/kanal/bein-sports-1-fhd", timeout=60000)
            
            # Videonun yüklenip tetiklenmesi için biraz bekleyin veya tıklama simüle edin
            page.wait_for_timeout(10000) # 10 saniye bekle
            
        except Exception as e:
            print(f"[!] Hata oluştu: {e}")

        browser.close()
        
        if not m3u8_links:
            print("[-] Doğrudan m3u8 isteği yakalanamadı. Site korumalı olabilir veya oynatıcıya manuel tıklamak gerekebilir.")

if __name__ == "__main__":
    find_m3u8()
