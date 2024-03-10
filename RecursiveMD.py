import cv2
import numpy as np
import pygame as pg
import threading

# Inicializar la librerias pygame y mixer
pg.init()
pg.mixer.init()

# Cargar del audio usado para la alerta
sound = pg.mixer.Sound("videoplayback.mp3")

# Captura de video
cap = cv2.VideoCapture(0)

# Variable para el indice de los frames
i = 0

# Variable para el fondo de la imagen
backGround = None 

# Semaforo para sincronizar acceso a la variable "backGround"
semaforo = threading.Semaphore(1) 

# Funcion para actualizar el fondo en segundo plano
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

# Inicio del hilo para la actualizacion del fondo
hilo_actualizacion = threading.Thread(target=actualizar_fondo)
hilo_actualizacion.start()

# Funcion recursiva para detectar movimiento
# Lo que hace esta implementacion de recursividad es que la funcion cuando detecta movimiento en un frame, se llama a ela misma recursivamente con el siguiente frame escaneado
def detectar_movimiento(frame):

    ret, next_frame = cap.read()

    if ret == False:
        return

    gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

    # Aqui se sincroniza el acceso a la variable "backGround"
    with semaforo:
        if backGround is not None:
            dif = cv2.absdiff(gray, backGround)
            _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
            cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                area = cv2.contourArea(c)
                if area > 8000:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(next_frame, (x, y), (x + w, y + h), (55, 255, 0), 2)
                    print("Detectando movimiento...PIIIII")
                    sound.play()

    # Se muestra el frame actual
    cv2.imshow('camarita', next_frame)

    # Se comprueba si se ha presionado la tecla 'q' para cerrar la ventana y salir del prog
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        return

    # Se llama a la funcion de forma recursiva con el siguiente frame
    detectar_movimiento(next_frame)

# Inicio de la detección de movimiento
detectar_movimiento(cap.read()[1])

# Espera a que el hilo de actualizacion termine
hilo_actualizacion.join()

# Aqui se liberan los recursos de la pc
cap.release()
cv2.destroyAllWindows()