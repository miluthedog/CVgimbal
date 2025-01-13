import cv2 as cv
from ultralytics import YOLO
import serial
import time

arduino = serial.Serial('COM5', 9600) 
time.sleep(2)
position = 90

yolo = YOLO('best.pt')
videoCap = cv.VideoCapture(0)

def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
             (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

while True:
    ret, frame = videoCap.read()
    if not ret:
        continue

    frameWidth, frameHeight = frame.shape[1], frame.shape[0]
    centerX, centerY = frameWidth // 2, frameHeight // 2
    cv.circle(frame, (centerX, centerY), 5, (0, 0, 255), -1) 

    results = yolo.track(frame, stream=True)

    for result in results:
        classes_names = result.names

        for box in result.boxes:
            if box.conf[0] > 0.5: # threshold  
                [x1, y1, x2, y2] = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])
                class_name = classes_names[cls]
                colour = getColours(cls)

                cv.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                cv.putText(frame, f'{class_name} {box.conf[0]:.2f}', 
                            (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 1, colour, 2)

                objCenterX = (x1 + x2) // 2
                cv.circle(frame, (objCenterX, centerY), 5, (255, 0, 0), -1)

                errorX = frameWidth // 12
                if objCenterX > centerX + errorX and position > 0:
                    position -= 1
                elif objCenterX < centerX - errorX and position < 180:
                    position += 1

                arduino.write((str(position) + '\n').encode())

    cv.imshow('Pha tracking', frame)

    pressEsc = cv.waitKey(1) & 0xff
    if pressEsc == 27:
        break

videoCap.release()
cv.destroyAllWindows()
arduino.close()
