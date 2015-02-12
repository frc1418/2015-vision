import cv2
import numpy as np
import colorAverages as ca
import copy

def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)

img = cv2.imread('Images/YT_0.png')
oimg = copy.copy(img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#splitting the immage
h, s, v = cv2.split(hsv)
#looking for color within a certain range
h = threshold_range(h, 14, 59)

s = threshold_range(s, 57, 255)

v = threshold_range(v, 49, 255)

combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
img2 = combined.copy()
#finding the image
trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#makes contours into polygons
p = []

for contour in range(0, len(contours)):
    t = cv2.approxPolyDP(contours[contour], 100, True)
    #print t
    p.append(t)
bp = 0
pp = []
#Sorts small  groups and shows biggest polygon
#print len(p), 'plength'
for contour in range(0, len(p)):
    ap = cv2.arcLength(p[contour], True)
    if ap > 400:
        pp.append(p[contour])

#drawing the contours
cv2.drawContours(oimg, pp, -1,(0,0,255), 3)
colors = ca.findColorAverages(oimg, pp)
ca.fillContours(oimg, pp, colors)
#show the image

cv2.waitKey(0)
