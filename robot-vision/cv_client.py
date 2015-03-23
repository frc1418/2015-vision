
import cv2
import numpy

# Camera resolution to capture at
width = 240
height = 160


def process_stream(processor):
    
    #Camera buffers and handle
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    img = None
    
    while True:
        
        retval, img = camera.read(img)
        if processor.should_process():
            processor.process(img)
    