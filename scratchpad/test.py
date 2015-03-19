import cv2 
import numpy as np

frame_buffer = np.zeros((720, 1280), dtype=np.uint8) 

camera = cv2.VideoCapture(0)

for i in range(0,1):
    camera.read(frame_buffer)[1]

while(1):
    cv2.imshow("im", frame_buffer)