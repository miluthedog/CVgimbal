import cv2 as cv
import serial
import time

# set up cv
trainedData = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv.VideoCapture(0)
# set up arduino
arduino = serial.Serial('COM5', 9600) # adjust this
time.sleep(2)
position = 90

while True:
    running, info = cam.read()
    if not running:
        break

    gray = cv.cvtColor(info, cv.COLOR_BGR2GRAY)
    faces = trainedData.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)

    frameWidth, frameHeight = info.shape[1], info.shape[0]
    cv.circle(info, (frameWidth//2, frameHeight//2), 5, (0, 0, 255), -1)
    
    if len(faces) > 0:
    # draw shapes: (x, y) are coord of top left pixel, w h are width height - BRG color
        (x, y, w, h) = faces[0]

        cv.rectangle(info, (x, y), (x+w, y+h), (255, 255, 0), 2)
        cv.circle(info, (x + w//2, y + h//2), 5, (0, 0, 255), -1)
        cv.line(info, (frameWidth//2, frameHeight//2), (x + w//2, y + h//2), (255, 255, 0), 2)
        
        # send signal to arduino
        errorX = frameWidth//12
        camX = frameWidth//2
        faceX = x + w//2
        if faceX > camX + errorX and position > 0:
            position-=1
        elif faceX < camX - errorX and position < 180:
            position+=1

        arduino.write((str(position) + '\n').encode())

    cv.imshow('Tracking', info)

    pressEsc = cv.waitKey(1) & 0xff
    if pressEsc == 27:
        break

cam.release()
cv.destroyAllWindows()
arduino.close()
