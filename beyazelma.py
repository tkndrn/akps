
import requests

URL = "https://beyazelma78.com/api/chat/canli/stream"

def main():
    try:
        response = requests.get(
            URL,
            headers={"Accept": "text/event-stream"},
            timeout=20,
            stream=True
        )

        print("[HTTP]", response.status_code)
        print("[CONTENT-TYPE]", response.headers.get("Content-Type"))
        print("[FINAL URL]", response.url)

        if response.status_code == 200:
            print("[DATA] İlk akış satırları:")
            count = 0

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(line[:1000])
                    count += 1

                if count >= 10:
                    break
        else:
            print("[BODY]", next(response.iter_lines(), b""))

        response.close()

    except requests.RequestException as e:
        print("[ERROR]", str(e))

if __name__ == "__main__":
    main()
