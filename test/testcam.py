import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("no cam")
    exit()

while True:
    running, info = camera.read()
    if not running:
        print("no info")
        break

    cv2.imshow('camera', info)

    esc = cv2.waitKey(1) & 0xff
    if esc == 27:
        break

camera.release()
cv2.destroyAllWindows()