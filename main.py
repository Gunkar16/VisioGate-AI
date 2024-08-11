import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import serial
import time
import pygame
from datetime import datetime

pygame.mixer.init()
siren_sound = pygame.mixer.Sound('siren.mp3')  
model = load_model('models/imageclassifier3.h5', compile=False)
cap = cv2.VideoCapture(0)

arduino_port = 'COM9'  
ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2) 

file_path = 'detected_class.txt'

start_time = None
detected_class = None

while True:
    ret, frame = cap.read()
    frame = cv2.transpose(frame)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 0)
    resize = cv2.resize(frame, (256, 256))
    resize = np.expand_dims(resize, axis=0) 
    resize = resize / 255.0
    yhat = model.predict(resize)
    threshold = 0.5

    if yhat > threshold:
        current_class = 'Authorized'
    elif yhat < 0.1:
        current_class = 'Background'
    else:
        current_class = 'Unauthorized'

    if current_class in ['Authorized', 'Unauthorized', 'Background']:
        if current_class == detected_class:
            if time.time() - start_time >= 1:
                ser.write(f'{detected_class}\n'.encode())
                if detected_class == 'Unauthorized':
                    siren_sound.play(1)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    output_image = frame.copy()
                    cv2.putText(output_image, timestamp, (10, output_image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imwrite(f'Person_{timestamp}.jpg', output_image)
                else:
                    siren_sound.stop() 
                with open(file_path, 'w') as file:
                    file.write(detected_class)
                
                start_time = None
                detected_class = None
        else:
            start_time = time.time()
            detected_class = current_class
    else:
        start_time = None
        detected_class = None

    cv2.putText(frame, current_class, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow('Image Classification Model', frame)
    cv2.setWindowProperty('Image Classification Model', cv2.WND_PROP_TOPMOST, 1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
