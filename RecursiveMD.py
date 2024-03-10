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

def detectar_movimiento(frame):
    ret, next_frame = cap.read()

    if ret == False:
        return

    gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

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

    cv2.imshow('camarita', next_frame)

    if cv2.waitKey(1) & 0xFF == ord ('q'):
        return

    detectar_movimiento(next_frame)

# Inicio de la deteccin
detectar_movimiento(cap.read()[1])

# Esperar a que el hilo de actualizaciOn termine
hilo_actualizacion.join()

# Aqui se liberan los recursos de la pc
cap.release()
cv2.destroyAllWindows()

#Ejemplo de recursividad con algoritmo de busqueda de un factorial
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

numero = int(input("Introduzca un numero: "))

resultado = factorial(numero)

print(f"El factorial de {numero} es {resultado}")
