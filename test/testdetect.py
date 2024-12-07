import cv2 as cv

trainedData = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv.VideoCapture(0)

while True:
    running, info = cam.read()

    if not running:
        break

    gray = cv.cvtColor(info, cv.COLOR_BGR2GRAY)
    faces = trainedData.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv.rectangle(info, (x, y), (x+w, y+h), (255, 255, 0), 2)

    cv.imshow('Tracking', info)

    pressEsc = cv.waitKey(1) & 0xff
    if pressEsc == 27:
        break

# clean up
cam.release()
cv.destroyAllWindows()