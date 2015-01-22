import cv2
import numpy as np

def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)
'''def findContoursList(inputList, mode, method):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(cv2.findContours(inputList[i].copy(), mode, method)[1])
    return outputList'''
img = cv2.imread('Images/YT_3.jpg')
running = True
#while(running):
cv2.imshow('img', img)

#bgr = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(hsv)

h = threshold_range(h, 20, 50)
cv2.imshow('h', h)
s = threshold_range(s, 0, 125)
cv2.imshow('s', s)
v = threshold_range(v, 140, 255)
cv2.imshow('v', v)

combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
cv2.imshow('Combined', combined)
img2 = combined.copy()

trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print contours
cv2.imshow('img2b4', img2)
nContours = np.array()
for contour in contours:
    if cv2.arclength(contour, True) > 20:
        nContours.append(contour)

a = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
cv2.drawContours(a, nContours,-1,(0,0,255),2)
cv2.imshow('contoury', a)
cv2.waitKey(0)
