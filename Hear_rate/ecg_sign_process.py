import serial
import time
import numpy as np

def calculate_bpm(ecg_values, sampling_rate=100):

    threshold = np.mean(ecg_values) + np.std(ecg_values)
    peaks = [i for i, value in enumerate(ecg_values) if value > threshold]

    rr_intervals = np.diff(peaks) / sampling_rate 
    bpm = 60 / np.mean(rr_intervals) if len(rr_intervals) > 0 else 0

    return bpm

# Serial conection
serial_port = serial.Serial('/dev/ttyUSB0', 9600) 
time.sleep(2) 

ecg_buffer = []
sampling_rate = 100 

try:
    while True:
        if serial_port.in_waiting > 0:
            ecg_value = int(serial_port.readline().decode('utf-8').strip())
            ecg_buffer.append(ecg_value)

            if len(ecg_buffer) >= sampling_rate * 5:
                bpm = calculate_bpm(ecg_buffer, sampling_rate)
                print(f"BPM: {bpm:.2f}")

                ecg_buffer = []
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    serial_port.close()
