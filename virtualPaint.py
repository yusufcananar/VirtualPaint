import cv2
import numpy as np

setColors = np.array([[128,100,0,179,255,255],
                      [99,174,203,109,255,255],
                      [0,0,204,41,255,255]])

drawingColorValues = [[0,0,255],
                      [255,0,0],
                      [0,255,255]]

storedPoints = [] # x,y,colorId

# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (25, 25)
# fontScale
fontScale = 0.7
# Blue color in BGR
color = (150, 200, 0)
# Line thickness of 2 px
thickness = 1

def getContours(src):
    contours, hierarchy = cv2.findContours(src, cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 250:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2,y+h//2

def detectColor(src):
    imHSV = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in setColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imHSV, lower, upper)
        x,y = getContours(mask)
        if x != 0 and y != 0:
            newPoints.append([x,y,count])
        count += 1

    return newPoints

def drawOnCanvas(storedPoints, drawingColorValues):
    cv2.putText(img, 'Press C to clean', org, font,
                fontScale, color, thickness, cv2.LINE_AA)

    for pts in storedPoints:
        cv2.circle(img, (pts[0],pts[1]), 8, drawingColorValues[pts[2]], cv2.FILLED)

# Read and Show video or webcam feed
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if success:
        img = frame.copy()
        newPoints = detectColor(frame)
        if newPoints != 0:
            for pts in newPoints:
                storedPoints.append(pts)

        if len(storedPoints) != 0:
            drawOnCanvas(storedPoints, drawingColorValues)

        cv2.imshow("stream", img)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break

        elif k == ord('c'):
            storedPoints = []

    else:
        print("Video capture is " + success)
        break



