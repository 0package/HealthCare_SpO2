from smbus2 import SMBus
import time

# -----------------------------
# 설정
# -----------------------------
I2C_ADDR = 0x04       # 센서 I2C 주소 (i2cdetect로 확인)
VREF = 3.3            # 라즈베리파이 전압 기준
SENSITIVITY = 0.016   # 센서 전압 대비 %O2 (V/%)
O2_MIN = 0.0          # 센서 최소 산소 농도 (%)
O2_MAX = 25.0         # 센서 최대 산소 농도 (%)
bus = SMBus(1)        # I2C 버스 1

# -----------------------------
# 센서 읽기 함수
# -----------------------------
def read_oxygen():
    """
    I2C로 SEN0322 센서 데이터를 읽고
    보정된 산소 농도(%) 반환
    """
    try:
        # 2바이트 읽기 (센서에서 전압/ADC값)
        data = bus.read_i2c_block_data(I2C_ADDR, 0, 2)
        raw = (data[0] << 8) | data[1]  # 16bit 값
        # 전압 계산
        Vout = (raw / 65535) * VREF
        # 산소 농도로 변환
        oxygen = Vout / SENSITIVITY
        # 0~25% 범위로 클램핑
        oxygen = max(O2_MIN, min(O2_MAX, oxygen))
        return oxygen
    except Exception as e:
        print("센서 읽기 오류:", e)
        return None

# -----------------------------
# 메인 루프
# -----------------------------
if __name__ == "__main__":
    while True:
        O2 = read_oxygen()
        if O2 is not None:
            print(f"Oxygen Concentration: {O2:.2f}%")
        time.sleep(1)
