import cv2
import numpy as np
#Function to draw a list of contours onto an image
def drawContoursList(dst, inputList, contourIdx, color, thick):
    for i in range(0, len(inputList)):
        cv2.drawContours(dst, inputList[i], contourIdx, color, thickness=thick)
def findColorAverage(img, Contours):
    #creates an array of color averages for each Contour
    #first make an array of masks of each contour
    masks = []
    for contour in range(0, len(Contours)):
        masks.append(np.zeros(Contours[contour], np.uint8))
    #Get the mean of the color of each mask of the image and store the color
    colors = []
    for mask in range(0, len(masks)):
        colors.append(cv2.mean(img, mask = masks[mask]))
    return colors

def fillContours(img, Contours, colors):
    #fills each contour with the average color from the original image
    for contour in range(0, len(Contours)):
        cv2.fillConvexPoly(img, Contours[contour], colors[contour])

def showContourImage(Image, ContoursList, OriginalSize):
    #Draws all contours onto the quant
    '''fContours = []
    for contour in range(0, len(ContourList)):
        fContours.append(ContourList[contour]*4)
    '''
    drawContoursList(Image, ContoursList, -1, (0,0,255), 1)

    #Resizes the quantified image so that it is easy to see
    newImage = cv2.resize(Image, (OriginalSize[1],OriginalSize[0]))

    #Shows the final product
    cv2.imshow("Contours", newImage)
