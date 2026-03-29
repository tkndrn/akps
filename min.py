# -*- coding: utf-8 -*-
import time
import re
from playwright.sync_api import sync_playwright

def github_buton_patlatici():
    url = "https://freeiptv2023-d.ottc.xyz/index.php"
    
    with sync_playwright() as p:
        # GitHub'da 'headless=True' olmak zorunda
        browser = p.chromium.launch(headless=True)
        # Gerçek bir Windows kullanıcısı gibi görünmek için User Agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("[*] Siteye giriş yapılıyor...")
            page.goto(url, wait_until="networkidle")

            # BUTON KİLİDİ ÇÖZÜCÜ:
            # 1. Sayfayı rastgele aşağı kaydır (GitHub Actions'da bu önemli)
            page.evaluate("window.scrollTo(0, 500)")
            
            # 2. O meşhur 5 saniyelik geri sayımı GitHub'da 12 saniye bekletiyoruz
            # Çünkü GitHub sunucuları bazen gecikmeli tepki verebilir
            print("[*] Buton kilidinin açılması bekleniyor (12 sn)...")
            time.sleep(12)

            # 3. Butonu bul ve JS ile "Görünmez Kilitleri" kaldır
            btn_text = "Create free IPTV account !"
            print("[*] Buton tetikleniyor...")
            
            page.evaluate("""(text) => {
                const buttons = document.querySelectorAll('button, div, a');
                buttons.forEach(b => {
                    if(b.innerText.includes(text)) {
                        b.disabled = false; // Kilidi kaldır
                        b.click(); // Bas!
                    }
                });
            }""", btn_text)

            # 4. Yönlendirme ve Veri Çekme
            time.sleep(5)
            # View sayfasına zorla sızma (En kesin yöntem)
            page.goto(url + "?action=view", wait_until="domcontentloaded")
            
            content = page.content()
            user = re.search(r'User(?:name)?\s*[:=-]?\s*(\w+)', content, re.I)
            password = re.search(r'Pass(?:word)?\s*[:=-]?\s*(\w+)', content, re.I)

            if user and password:
                sonuc = f"USER: {user.group(1)}\nPASS: {password.group(1)}\nUPDATE: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                with open("iptv_sonuc.txt", "w") as f:
                    f.write(sonuc)
                print(f"[+] BASARILI: {user.group(1)}")
            else:
                print("[-] Butona basıldı ama veri gelmedi. Site ban atmış olabilir.")

        except Exception as e:
            print(f"[!] Hata: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    github_buton_patlatici()
