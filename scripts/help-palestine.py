import datetime
import requests
import threading
import time
import requests
import multiprocessing

page = requests.get("https://arab.org/click-to-help/palestine/").content.decode("utf-8")

for line in page.splitlines():
    if "security:" in str(line):
        code = line.strip().replace("security: '", "").replace("'", "")
    if "button_id:" in str(line):
        buttonID = (
            line.strip().replace("button_id: '", "").replace("'", "").replace(",", "")
        )

totalRequests = 0
totalSucceeded = 0
totalFailed = 0


def updateReqOutput():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\033[32m{totalRequests}\033[0m votes made, \033[32m{totalSucceeded}\033[0m successful, \033[31m{totalFailed}\033[0m failed",
        end="\r",
    )


def makeVoteRequest(button_id, security):
    global totalRequests, totalSucceeded, totalFailed
    url = "https://arab.org/wp-admin/admin-ajax.php"
    data = {
        "action": "make_vote_action",
        "button_id": button_id,
        "security": security,
    }
    response = requests.post(url, data=data)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        totalRequests += 1
        totalSucceeded += 1
    else:
        totalFailed += 1
        pass

    updateReqOutput()


while True:
    threads = []
    for _ in range(multiprocessing.cpu_count()):
        thread = threading.Thread(target=makeVoteRequest, args=(buttonID, code))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("", end="\r")
