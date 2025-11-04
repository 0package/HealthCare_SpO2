# 파일명: main.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# 1) 데이터 형식 정의
class SensorData(BaseModel):
    heart_rate: float
    spo2: float

# 2) 데이터 수신 엔드포인트
@app.post("/sensor")
async def receive_sensor_data(data: SensorData):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ❤️ HR: {data.heart_rate:.1f} bpm | SpO₂: {data.spo2:.1f}%")
    
    # 저장 or DB에 넣는 부분 (예시)
    with open("sensor_log.csv", "a") as f:
        f.write(f"{timestamp},{data.heart_rate},{data.spo2}\n")
    
    return {"status": "success", "received": data}

# 3) 실행 명령 (터미널)
# uvicorn main:app --host 0.0.0.0 --port 5000 --reload

