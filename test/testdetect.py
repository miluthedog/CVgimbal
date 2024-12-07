import cv2
import time

trainedData = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

while True:
    running, info = cam.read()

    if not running:
        break

    gray = cv2.cvtColor(info, cv2.COLOR_BGR2GRAY)
    faces = trainedData.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(info, (x, y), (x+w, y+h), (255, 255, 0), 2)

    cv2.imshow('Tracking', info)

    pressEsc = cv2.waitKey(1) & 0xff
    if pressEsc == 27:
        break

# clean up
cam.release()
cv2.destroyAllWindows()