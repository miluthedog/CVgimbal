import cv2 as cv
import serial
import time

# set up cv
trainedData = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv.VideoCapture(0)

# set up arduino
arduino = serial.Serial('COM5', 9600) # adjust this
time.sleep(2)

while True:
    running, info = cam.read()

    if not running:
        break

    gray = cv.cvtColor(info, cv.COLOR_BGR2GRAY)
    faces = trainedData.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)

    if len(faces) > 0:
        # draw rectangle: (x, y) are coord of top left pixel, w h are width height - BRG color
        (x, y, w, h) = faces[0]
        cv.rectangle(info, (x, y), (x+w, y+h), (255, 255, 0), 2)
        
        # send signal to arduino
        width = info.shape[1]
        center = x + w // 2
        normalizedX = int((center / width) * 180)
        arduino.write((str(normalizedX) + '\n').encode())

    cv.imshow('Tracking', info)

    pressEsc = cv.waitKey(1) & 0xff
    if pressEsc == 27:
        break

# clean up
cam.release()
cv.destroyAllWindows()
arduino.close()
