import datetime
import requests
import threading
import time

total_requests = 0
total_succeded = 0
total_failed = 0


def updateReqOutput():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\033[32m{total_requests}\033[0m requests, \033[32m{total_succeded}\033[0m successful, \033[31m{total_failed}\033[0m failed",
        end="\r",
    )


def make_vote_request(buttonID, security):
    global total_requests, total_succeded, total_failed
    url = "https://arab.org/wp-admin/admin-ajax.php"
    payload = f"action=make_vote_action&button_id={buttonID}&security={security}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    }

    response = requests.post(
        "https://arab.org/wp-admin/admin-ajax.php", data=payload, headers=headers
    )

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        total_requests += 1
        total_succeded += 1
    else:
        total_failed += 1
        total_requests += 1
        pass

    updateReqOutput()


page = requests.get("https://arab.org/click-to-help/palestine/").content.decode("utf-8")
for line in page.splitlines():
    if "security:" in str(line):
        code = line.strip().replace("security: '", "").replace("'", "")
    if "button_id:" in str(line):
        buttonID = (
            line.strip().replace("button_id: '", "").replace("'", "").replace(",", "")
        )

while True:
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=make_vote_request, args=(buttonID, code))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    time.sleep(1)
