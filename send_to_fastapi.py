# 파일명: send_to_fastapi.py
import max30102
import hrcalc
import time
import requests
import json

# FastAPI 서버 주소 (홍띠니의 서버 IP/도메인으로 수정)
API_URL = "http://localhost:5000/sensor"

m = max30102.MAX30102()

def send_data(hr, spo2):
    """FastAPI 서버로 전송"""
    data = {"heart_rate": hr, "spo2": spo2}
    try:
        response = requests.post(API_URL, json=data)
        print(f"📡 전송 완료: {response.status_code} | {data}")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

try:
    print("💓 MAX30102 데이터 측정 시작...")
    while True:
        red, ir = m.read_sequential()
        if len(ir) > 100:
            hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
            
            if hr_valid and spo2_valid:
                print(f"❤️ HR: {hr:.1f} bpm | SpO₂: {spo2:.1f}%")
                send_data(hr, spo2)
            else:
                print("⚠️ 데이터 안정화 중...")

        time.sleep(2)

except KeyboardInterrupt:
    print("측정 종료 🛑")
