import max30102
import hrcalc
import time
import matplotlib.pyplot as plt

m = max30102.MAX30102()

try:
    while True:
        red, ir = m.read_sequential()
        print(f"Red: {red[-10:]}, IR: {ir[-10:]}") #recently measured of 10
        if len(ir) > 60:
            hr, hr_vaild, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
            print(f"Heart Rate : {hr:.1f} bpm | SpO2: {spo2:.1f}%")
        time.sleep(1)
except KeyboardInterrupt:
    print("End Measuring")

red, ir = m.read_sequential(500)
plt.plot(ir, label="IR Signal")
plt.plot(red, label="Red Signal")
plt.legend()
plt.show()
