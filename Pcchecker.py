import psutil
import time
import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
BASE_URL = DB_URL.replace(".json", "").rstrip("/")

def update_firebase(data):
    try:
        requests.patch(f"{BASE_URL}.json", json={"pc_status": data}, timeout=5)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 업데이트 완료")
    except:
        pass

# --- 핵심: 서버에서 기존 시간 불러오기 ---
def get_remote_usage():
    try:
        res = requests.get(f"{BASE_URL}/pc_status/today_usage_seconds.json", timeout=5).json()
        return int(res) if res else 0
    except:
        return 0

last_date = datetime.date.today().strftime("%Y-%m-%d")
# 앱 켜질 때 서버에 저장된 '초'를 가져와서 시작점으로 잡음
accumulated_seconds = get_remote_usage()
start_time = time.time()

print(f"Studio J Agent: {accumulated_seconds}초부터 이어서 측정 시작!")

while True:
    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # 1. 00시 초기화 (날짜가 바뀌면 서버 데이터도 무시하고 0부터)
    if today_str != last_date:
        accumulated_seconds = 0
        start_time = time.time()
        last_date = today_str
        print("날짜 변경으로 초기화!")

    # 2. 현재 사용 시간 = (기존에 써온 시간) + (앱 켜진 후 흐른 시간)
    total_seconds = accumulated_seconds + int(time.time() - start_time)
    time_str = str(datetime.timedelta(seconds=total_seconds))

    # 3. 데이터 전송 (오늘 총 '초'수도 같이 저장해서 다음에 이어서 쓸 수 있게 함)
    update_data = {
        "today_usage": time_str,
        "today_usage_seconds": total_seconds, # 요게 포인트!
        "last_seen": now.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Online",
        "password": MY_PASSWORD,
        "day": ['월','화','수','목','금','토','일'][now.weekday()]
    }
    update_firebase(update_data)

    time.sleep(5)
