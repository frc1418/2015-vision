import cv2
import sys

import imageSimple as imgSi

#Creates the help string
helpArgs = []
helpArgs.append('   -rc    Shows raw contours being found')
helpArgs.append('   -tf    Shows tape being found')
helpArgs.append('   -img   Image input (Must be followed by path)')

#Shows raw unfiltered contours
rawContours = False

#Shows the reflective tape finder
findTape = False

#Uses image input with path
imageInput = False
imagePath = None

#Running for killing process if --help
running = True

#If there are more then 1 args
if len(sys.argv) != 1:
    skip = False
    #Runs thru the args
    for i in range(1, len(sys.argv)):
        #If skip is set it toggles it and doesnt check next
        if skip == True:
            skip = False
        else:
            current = sys.argv[i]

            #If -rc enable showing raw contours
            if current == '-rc':
                rawContours = True

            #if -tf enable showing tape finder
            elif current == '-tf':
                findTape = True

            #if -tf enable image input set the path to next argument
            #Skips the check for the next argument so it doesnt go to help
            elif current == '-img':
                imageInput = True
                i += 1
                imagePath = sys.argv[i]
                skip = True
                if len(sys.argv) == 3:
                    rawContours = True

            #If help show the help and kill
            elif current == '--help':
                running = False
                for tip in helpArgs:
                    print tip

            #If unreconized argument show help and kill
            else:
                running = False
                for tip in helpArgs:
                    print tip
#If no args just show video contours
else:
    rawContours = True

#Determining content
waitTime = None
content = None

#if image input set the content to the path and set wait time to 0
#Wait time 0 waits till the esc pressed in imageSimple so it doesnt try
#to take another frame of a one frame picture
if imageInput:
    content = cv2.imread(imagePath)
    waitTime = 0
#if its not image input set the capture to the first webcam
else:
    content = cv2.VideoCapture(0)
    waitTime = 1

imgSi.run(content, rawContours, findTape, waitTime, imageInput, running)
