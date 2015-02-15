
import cv2

vc = cv2.VideoCapture()

w, h = 215, 120

#vc.set(cv2.CAP_PROP_FRAME_WIDTH, w)
#vc.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

vc.open(0)

#vc.set(cv2.CAP_PROP_FRAME_WIDTH, w)
#vc.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

while True:
    retval, img = vc.read()
    
    if not retval:
        print("Error")
        break
    
    cv2.imshow('name', img)
    
    if cv2.waitKey(1)  & 0xFF == ord('q'):
        break