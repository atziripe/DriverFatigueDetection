import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

model = tf.keras.models.load_model('best_model.keras') 

def preprocess_image(img_path, target_size=(64, 64)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_eye_state(img_path):
    preprocessed_img = preprocess_image(img_path)

    prediction = model.predict(preprocessed_img)[0][0]

    # Threshold
    threshold = 0.5
    if prediction > threshold:
        print(f"Prediction: {prediction:.2f} -> Open Eyes")
    else:
        print(f"Prediction: {prediction:.2f} -> Closed Eyes")

img_path = "image/abiert.png" 
predict_eye_state(img_path)
