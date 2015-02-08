import cv2
import numpy as np

def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)




cam = cv2.VideoCapture(0)
running = True
while(running):


    frame = cam.read()[1]
    img = frame

    #cv2.imshow('img', img)
    oimg = img.copy()
    #converting the color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #splitting the immage
    h, s, v = cv2.split(hsv)
    #looking for color within a certain range
    h = threshold_range(h, 14, 59)

    s = threshold_range(s, 57, 255)

    v = threshold_range(v, 49, 255)

    #recombining the image
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
    #show the image
    cv2.imshow('contoury', oimg)
    if cv2.waitKey(1)  & 0xFF == ord('q'):
        break

cam.releas()
cv2.destroyAllWindows()
