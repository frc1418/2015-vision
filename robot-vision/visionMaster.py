import cv2
import numpy
import argparse
import detectBlack
from networktables import NetworkTable

'''
Global Variables
'''
#Camera resultion
camera_res = (1280 , 720)

#Processing resultion

#Camera buffers and handle 
camera1 = cv2.VideoCapture(0)
camera1_buffer = numpy.zeros(camera_res)

camera2 = cv2.VideoCapture(0)
camera2_buffer = numpy.zeros(camera_res)

#Booleans
running = True
find_bin = False
capture = True

'''
Option parsing
'''
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--networked", action = "store_true", default = False, help="Use network tables")

args = parser.parse_args()

if args.networked:
    NetworkTable.setIPAddress("localhost")
    NetworkTable.setClientMode()
    NetworkTable.initialize()

'''
Main while loop
'''
while(running):
    if(args.networked):
        sd = NetworkTable.getTable("SmartDashboard")
        find_bin = sd.getBoolean("findBin", False)
    
    if(capture):
        camera1_buffer = camera1.read()[1]
        camera2_buffer = camera2.read()[2]
        
    if(find_bin):
        detectBlack.detect_black(camera1_buffer, camera_res[1])
    
