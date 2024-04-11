import cv2
import numpy as np
import pygame as pg
import threading

# Inicializar la librerías pygame y mixer
pg.init()
pg.mixer.init()

# Cargar del audio usado para la alerta
sound = pg.mixer.Sound("videoplayback.mp3")

# Captura de video
cap = cv2.VideoCapture(0)

# Variable para el índice de los frames
i = 0

# Clase Monitor para sincronizar acceso a la variable "backGround"
class Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.backGround = None
    
    def get_background(self):
        with self.lock:
            return self.backGround
    
    def set_background(self, value):
        with self.lock:
            self.backGround = value

# Instancia del Monitor
monitor = Monitor()

# Función para actualizar el fondo en segundo plano
def actualizar_fondo():
    global i
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if i == 50:
                monitor.set_background(gray)
            i += 1
    except Exception as e:
        print("Error en la actualización del fondo:", e)

# Inicio del hilo para la actualización del fondo
hilo_actualizacion = threading.Thread(target=actualizar_fondo)
hilo_actualizacion.start()

# Función recursiva para detectar movimiento
def detectar_movimiento(frame):
    try:
        ret, next_frame = cap.read()
        if not ret:
            return
        gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
        backGround = monitor.get_background()
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
    except Exception as e:
        print("Error en la detección de movimiento:", e)

# Inicio de la detección de movimiento
detectar_movimiento(cap.read()[1])

# Espera a que el hilo de actualización termine
hilo_actualizacion.join()

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
