import cv2
import numpy
import argparse
import detectBlack
from networktables import NetworkTable

'''
Global Variables
'''
#Camera resultion
camera_res = (240 , 160, 3)

#Processing resultion

#Camera buffers and handle
camera1 = cv2.VideoCapture(0)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, camera_res[0])
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_res[1])
camera1_buffer = numpy.zeros(camera_res, dtype=numpy.uint8)

camera2 = cv2.VideoCapture(1)
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, camera_res[0])
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_res[1])
camera2_buffer = numpy.zeros(camera_res, dtype=numpy.uint8)

#Booleans
running = True
find_bin = False
capture = True

'''
Option parsing
'''
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--networked", action = "store_true", default = False, help="Use network tables")
parser.add_argument("-f", "--findBin", action = "store_true", default = False, help="Use network tables")

args = parser.parse_args()

if args.networked:
    NetworkTable.setIPAddress("localhost")
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    sd = NetworkTable.getTable("SmartDashboard")
    sd.putBoolean("findBin", False)
else:
    find_bin = args.findBin

'''
Main while loop
'''

while running:
    if args.networked:
        find_bin = sd.getBoolean("findBin", False)

    if capture:
        camera1_buffer = camera1.read()[1]
        camera2_buffer = camera2.read()[1]

    if find_bin:
        bin_position, coordinates = detectBlack.detect_black(camera2_buffer, camera_res[0])
        if args.networked:
            sd.putDouble("binPosition", bin_position)
            sd.putValue("rectanglePoints", coordinates)
        else:
            print("Bin Position: %s" % bin_position)
            #cv2.imshow("Moo", bin_position[1])
