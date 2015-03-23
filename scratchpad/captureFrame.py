import cv2
import time
import optparse

parser = optparse.OptionParser()
parser.add_option("-y", "--yPos", action="store", type="int", dest="yPos")
parser.add_option("-x", "--xPos", action="store", type="int", dest="xPos")
parser.add_option("-s", "--scale", action="store", type="int", dest="scale")
parser.add_option("-d", "--destonation", action="store", type="string", dest="path")

options, remainder = parser.parse_args()

content = cv2.VideoCapture(0)

#Takes five frames for exposure
for i in range(0,5):
    frame = content.read()[1]

scale = options.scale

x = frame.shape[1]
y = frame.shape[0]

#Scale if scale is set
if(scale != None):


    newX = (int)(x/scale)
    newY = (int)(y/scale)

    newSize = (newX, newY)
    frame = cv2.resize(frame, newSize)
elif(options.xPos != None):

    newX = options.xPos
    newY = (int)((newX*y)/x)

    newSize = (newX, newY)
    frame = cv2.resize(frame, newSize)


elif(options.yPos != None):

    newY = options.yPos
    newX = (int)((newY*x)/y)

    newSize = (newX, newY)
    frame = cv2.resize(frame, newSize)

#Figeurs out path
path = options.path
if path == None:
    path = ("%s.png" %time.strftime("%H:%M:%S"))

cv2.imwrite(path, frame)

#cv2.imshow("Test", frame)
