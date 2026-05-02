import psutil
import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. .env 파일 로드 (파일이 같은 폴더에 있어야 해!)
load_dotenv()

# 2. 환경 변수에서 데이터베이스 주소와 비번 가져오기
DB_URL = os.getenv("DB_URL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# 에러 체크: .env 파일을 못 읽었을 경우를 대비
if DB_URL is None:
    print("❌ 에러: .env 파일을 찾을 수 없거나 DB_URL이 비어 있습니다.")
    print(f"현재 실행 경로: {os.getcwd()}")
    print(".env 파일이 이 경로에 있는지 확인주십시오.")
    exit()

# 원격 명령용 URL 생성 (usage.json -> command.json)
CMD_URL = DB_URL.replace("usage.json", "command.json")

def get_uptime():
    """컴퓨터 부팅 이후 흐른 시간을 계산하는 함수"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분"

def send_data():
    print("PC 모니터링 시스템 가동 중...")
    
    while True:
        try:
            # 1. 웹에서 내린 원격 명령이 있는지 확인
            try:
                cmd_res = requests.get(CMD_URL).json()
                if cmd_res == "shutdown":
                    print("⚠️ 원격 종료 명령 수신! 10초 뒤 컴퓨터를 종료합니다.")
                    requests.put(CMD_URL, json="") # 명령 초기화
                    os.system("shutdown /s /t 10")
                    break
                elif cmd_res == "sleep":
                    print("💤 원격 절전 명령 수신!")
                    requests.put(CMD_URL, json="") # 명령 초기화
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            except Exception as cmd_e:
                print(f"명령 확인 중 오류(무시 가능): {cmd_e}")

            # 2. 내 컴퓨터 사용량 데이터 준비
            usage_data = {
                "cpu": psutil.cpu_percent(interval=1),
                "ram": psutil.virtual_memory().percent,
                "uptime": get_uptime(),
                "pw": MY_PASSWORD,
                "last_check": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 3. 파이어베이스로 전송
            response = requests.put(DB_URL, json=usage_data)
            
            if response.status_code == 200:
                print(f"[{usage_data['last_check']}] 보고 완료 | 사용시간: {usage_data['uptime']} | CPU: {usage_data['cpu']}%")
            else:
                print(f"❌ 전송 실패: {response.status_code}")
                
        except Exception as e:
            print(f"🚨 예외 발생: {e}")
            
        # 10초마다 반복 (원격 명령을 빠르게 확인하려면 이 시간을 줄여도 돼)
        time.sleep(0.5)

if __name__ == "__main__":
    send_data()
