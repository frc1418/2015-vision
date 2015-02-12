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



cam = cv2.VideoCapture(0)
running = True
while(running):

    frame = cam.read()[1]
    img = frame
    size = img.shape[:2]

    #cv2.imshow('img', img)
    oimg = img.copy()
    #bgr = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    h = threshold_range(h, 20, 50)
    #cv2.imshow('h', h)
    s = threshold_range(s, 57, 255)
    #cv2.imshow('s', s)
    v = threshold_range(v, 49, 255)
    #cv2.imshow('v', v)

    combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
    #cv2.imshow('Combined', combined)
    img2 = combined.copy()

    trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rs = 0
    ls = 0
    tx = size[1]
    ty = size[0]
    midy = ty/2
    midx = tx/2
    bottomContours = []
    #Tells how many contours are on each side of the image
    #also which contours are on the bottom and which are on the top
    for contour in range(0, len(contours)):
        c = contours[contour]
        #counters for how many contours are on top and bottom
        tcounter = 0
        bcounter = 0
        for co in range(0, len(c)):
            #have to go through many layers in the array to get to the raw points
            con = c[co]
            for cont in range(0, len(con)):
                conto = con[cont]
                xc = conto[0]
                if yc >= midy:
                    bcounter = bcounter + 1
                    if xc >= midx:
                        rs = rs + 1
                    elif xc < midx:
                        ls = ls + 1
                    yc = conto[1]
                elif yc < midy:
                    tcounter = tcounter + 1
        #if there are more points on the bottom add the contour to array of contours on the bottom
        if bcounter > tcounter:
            bottomContours.append(contours[contour])

    print rs, 'rs'
    print ls, 'ls'




    #cv2.imshow('contouryb4', oimg)
    #makes contours into polygons
    p = []

    for contour in range(0, len(bottomContours)):
        t = cv2.approxPolyDP(bottomContours[contour], 100, True)
        #print t
        p.append(t)
    bp = 0
    pp = []
    #Sorts small  groups and shows bigger polygons
    #print len(p), 'plength'
    for contour in range(0, len(p)):
        ap = cv2.arcLength(p[contour], True)
        if ap > 400:
            pp.append(p[contour])
    rb = False
    lb = False
    if len(pp) > 0:
        if rs > ls:
            rb = True
        if ls <= rs:
            ls = True
    #print pp
        #print ap
    #x, y, xlen, ylen = cv2.boundingRect(pp)
    #print p
    '''if cv2.arcLength(p[contour], True) > 300:
        nContours.append(p[conto    ur])'''


    cv2.drawContours(oimg, pp, -1,(0,0,255), 3)
    cv2.imshow('contoury', oimg)
    if cv2.waitKey(1)  & 0xFF == ord('q'):
        break

cam.releas()
cv2.destroyAllWindows()
