import cv2
import numpy as np

# Captura de video desde la cámara del móvil
cap = cv2.VideoCapture(0)
i = 0

# # Primer fotograma como referencia
# ret, fondo = cap.read()

while (True):
    # Lectura de cada fotograma
    ret, frame = cap.read()
    if ret == False:break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if i == 15:
        bgGray = gray
    if i > 15:
        dif = cv2.absdiff(gray, bgGray)
        _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
        cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('th', th)

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 9000:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #(frame, (x,y), (x+w,y+h), (255,0,0),2)
                print("Detectando movimiento...PIIIII")

    cv2.imshow('video1', frame)
    i = i+1
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

cap.release()
cv2.destroyAllWindows()