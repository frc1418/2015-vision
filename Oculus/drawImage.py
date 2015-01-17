import cv2

#Function to draw a list of contours onto an image
def drawContoursList(dst, inputList, contourIdx, color, thick):
    for i in range(0, len(inputList)):
        cv2.drawContours(dst, inputList[i], contourIdx, color, thickness=thick)

def showContourImage(Image, ContoursList):
    #Draws all contours onto the quant
    drawContoursList(Image, ContoursList, -1, (0,0,255), 1)

    #Resizes the quantified image so that it is easy to see
    newImage = cv2.resize(Image, (1150,600))

    #Shows the final product
    cv2.imshow("image", newImage)
