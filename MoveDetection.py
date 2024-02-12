import cv2
import numpy as np
import pygame as pg
import threading

pg.init()
pg.mixer.init()
sound = pg.mixer.Sound("videoplayback.mp3")
cap = cv2.VideoCapture(0)
i = 0
backGround = None  # Variable compartida entre hilos
semaforo = threading.Semaphore(1)  # Inicializar el semaforo con un valor de 1

# Analisis de los frames de la imagen de fondo y la actual 
def actualizar_fondo():
    global i, backGround
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i == 50:
            with semaforo:
                backGround = gray
        i += 1

# Iniciar un hilo para la actualizacion del fondo
hilo_actualizacion = threading.Thread(target=actualizar_fondo)
hilo_actualizacion.start()

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    with semaforo:
        if backGround is not None:
            dif = cv2.absdiff(gray, backGround)
            _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
            cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Dibujar contorno de area con movimiento detectada
            for c in cnts:
                area = cv2.contourArea(c)
                if area > 8000:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (55, 255, 0), 2)
                    print("Detectando movimiento...PIIIII")
                    sound.play()
    cv2.imshow('camarita', frame)
    
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

# Esperar a que el hilo de actualización termine
hilo_actualizacion.join()

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
