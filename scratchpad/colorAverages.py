import cv2
import numpy as np


def findColorAverages(img, ContoursLists):
    #creates an array of color averages for each Contour
    #first make an array of masks of each contour
    #print 'shapes', img.shape
    masks = []
    colors = []
    #carters four layer system is annoying
    for contourlist in range(0, len(ContoursLists)):
        currentLayer = ContoursLists[contourlist]
        #cv2.drawContours(img, currentLayer, -1, (0, 0, 255))
        for contour in range(0, len(currentLayer)):
            #print 'contour', currentLayer[contour]
            currentContour = currentLayer[contour]
            #print 'currentContour', currentContour
            #get the bounding rectangle of the contour for mask of points
            x, y, w, h = cv2.boundingRect(currentContour)
            #print x, y, w, h
            x2 = x + h
            y2 = y + h
            #points = [(x, y), (x2, y), (x, y2), (x2, y2)]
            #make the masks
            mask = np.zeros(img.shape[:2], np.uint8)

            mask[x:x2, y:y2] = 255
            #print 'mask', mask
            color = cv2.mean(img, mask)
            #print color, 'color'
            colors.append(color)
    return colors

def fillContours(img, ContourLists, colors):
    #fills each contour with the average color from the original image
    for contourlist in range(0, len(ContourLists)):
        currentList = ContourLists[contourlist]
        cv2.drawContours(img, ContourLists[contourlist], -1, (0, 0, 255))
        for contour in range(0, len(currentList)):
            #problem with points(contours)
            #print 'contours', [contour]
            if len(colors) >= len(currentList):
                cv2.fillPoly(img, [currentList[contour]], colors[contour])

    #show the img with the contours and the color averages
    cv2.imshow("image", img)
