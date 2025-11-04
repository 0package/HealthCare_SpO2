from max30102 import MAX30102
import hrcalc
import time

import RPi.GPIO as GPIO
import board

import requests

import adafruit_dht
#import spidev
import math

# pin #
#SEN30102 pin number
pin = 6
t_pin = 4

#Setting GPIO PIN
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
GPIO.setup(t_pin, GPIO.IN)

#server URL
url = 'https://port-0-healthcare-m7tucm4sab201860.sel4.cloudtype.app/sensors'

#user_info
user_id = 'user@gmail.com'

# Temperature
#dhtDevice = adafruit_dht.DHT11(board.D4)

# CO2
#spi = spidev.SpiDev()
#spi.open(0,0)
#spi.max_speed_hz = 1000000

# CO2 value setting
R1 = 23500
R2 = 10000
cal_A = 1.703
cal_B = 0.2677

#def read_adc(channel):
#	if channel < 0 or channel > 7:
#		return -1
#	adc = spi.xfer2([(8+channel) << 4, 0])
#	data = ((adc[1]&3) << 8) + adc[2]
#	return data

#def measure_emf_ini(channel):
#	print('wait 3s, ini EMF')
#	time.sleep(3)
#	emf_values = []
#	for _ in range(30):
#		adc_val = read_adc(channel)
#		v_out = (adc_val * 3.3) / 1023
#		emf = v_out * ((R1+R2)/R2)
#		emf_values.append(emf)
#		time.sleep(0.2)
#	emf_ini = sum(emf_values)/len(emf_values)
#	print(f"ini V: {emf_ini:.3f} V")
#	return emf_ini

#def convert_to_co2(adc_value, emf_ini):
#	v_out = (adc_value*3.3)/1023
#	emf = v_out * ((R1+R2)/R2)
#
#	ratio = emf / emf_ini
#	if ratio <= 0:
#		return 0

#	co2_ppm = math.pow(10, (cal_A - ratio) / cal_B)
#	return round(co2_ppm)

# Sen30102 base in max30102
# Using max30102 Module
# max30102.MAX30102() : using I2C tools, default I2C address : 0xd57
# m = max30102.MAX30102(address=0x57)
m = MAX30102(address=0x57)

try:
	#emf_ini = measure_emf_ini(0)
	while True:
		
		red, ir = m.read_sequential()
		hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(red, ir)
		print(f"hr: {hr}, hrvalid: {hr_valid}, spo2: {spo2}, spo2valid: {spo2_valid}")
		#temp = round(dhtDevice.temperature, 2)
		#adc_co2_val = read_adc(0)
		#co2 = convert_to_co2(adc_co2_val, emf_ini)
		temp = 3.0
		co2 = 400
		data = {'user_id':user_id, 'temperature':temp, 'spo2':spo2, 'pulse':hr, 'co2':co2}
		try:
			response = requests.post(url, json=data)
			if response.status_code == 200:
				print(f'Data Sent: {data}')
			else:
				print(f'Error:{response.status_code} - {response.text}')
				print(response.text)
		except requests.RequestException as e:
			print(f'Network Error:{e}')
		except KeyboardInterrupt:
			GPIO.cleanup()
			break
		print(f"HR:{hr} bpm, SpO2: {spo2:.2f}%")
		time.sleep(1)
except KeyboardInterrupt:
	print("end")
