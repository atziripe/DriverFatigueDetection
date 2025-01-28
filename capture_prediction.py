import cv2
import numpy as np
import tensorflow as tf
from Hear_rate.Simulation.signal_simulation import *
from Pressure_steering.pressure_sim import *

model = tf.keras.models.load_model('CNN/best_model.keras')
IMG_SIZE = (64, 64)
PRESSURE_THRESHOLD = 20


def preprocess_frame(frame):
    #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(frame, IMG_SIZE)
    normalized_frame = resized_frame / 255.0
    #(1, 64, 64, 3)
    return np.expand_dims(normalized_frame, axis=0)

# Camera initialization
cap = cv2.VideoCapture(0)

# ECG signal simulation
duration = 10
sampling_rate = 100
bpm = 40
t, ecg_signal = generate_ecg_data(duration, sampling_rate, bpm)
bpm_calculated = calculate_bpm_from_simulated_ecg(ecg_signal, sampling_rate)

# pressure simulation
t, pressure = simulate_pressure_data(duration=10, sampling_rate=10)
i =0 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not accesible.")
        break

    input_frame = preprocess_frame(frame)
    i = (i + 1) % len(pressure)
    #Prediction
    prediction = model.predict(input_frame)[0][0]
    print("PREDICTION CAMERA: ", prediction)
    print("PRESSURE: ", pressure)
    eyes  = "Eyes open"
    if prediction <= 0.8:
        eyes  = "Eyes closed"
        color = (0, 0, 255)  # Red
    else:
        eyes  = "Eyes opened"
        color = (0, 255, 0) # Green

    if prediction <= 0.8 and bpm_calculated < 60 and pressure[i] < PRESSURE_THRESHOLD:
        label_status = "ACHTUNG!! Possible fatigue detected"
        eyes  = "Eyes closed"
        color = (0, 0, 255)  # Red
    elif pressure[i] < PRESSURE_THRESHOLD:
        label_status = "PLEASE HOLD THE STEERING WHEEL TIGHTER "
        color = (0, 255, 255)  # yellow
    elif prediction <= 0.8:
        label_status = "OPEN YOUR EYES!"
        eyes  = "Eyes closed"
        color = (0, 255, 255)  # Yellow
    else:
        label_status = "Normal state"
        color = (0, 255, 0) # Green
    HR = bpm_calculated

    print(f"Calculated BPM: {bpm_calculated:.2f}")
    x, y = 10, 30 
    line_spacing = 40
    cv2.putText(frame, f"{label_status}", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"{eyes} ({prediction:.2f})", (x, y + line_spacing), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"HR ({bpm_calculated:.2f})", (x, y + 2 * line_spacing), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"PRESSURE ({pressure[i]:.2f})", (x, y + 3 * line_spacing), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Fatigue detection - camera", frame)

    # "q" to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
