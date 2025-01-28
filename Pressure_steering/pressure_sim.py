import numpy as np

def simulate_pressure_data(duration=10, sampling_rate=10):
    t = np.linspace(0, duration, duration * sampling_rate)
    
    # Normal pressure Simulation (Normal range 30-70)
    pressure = np.random.uniform(30, 70, size=t.shape)
    
    # Fatigue simulation (less pressure sometimes)
    fatigue_start = int(0.6 * len(t))  # 60% of time less pressure
    pressure[fatigue_start:] = np.random.uniform(10, 30, size=t[fatigue_start:].shape)
    
    return t, pressure
