import serial
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inicializar Firebase Realtime Database
cred = credentials.Certificate("clavem.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://masm-289bb-default-rtdb.firebaseio.com/'
})
ref = db.reference('/')

# Configurar referencia a la colección "lecturas_temperatura"
lecturas_ref = ref.child("lecturas_temperatura")

# Configuración del puerto serial
puerto_serial = serial.Serial('COM3', 9600)
time.sleep(2) # Esperar 2 segundos para conectarse al puerto serial

try:
    while True:
        datos = puerto_serial.readline().decode().strip() # Leer los datos del puerto serial y eliminar espacios en blanco
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Obtener la fecha y hora actuales
        lectura = {"fecha_hora": fecha_hora, "temperatura": datos}
        print("Fecha y hora:", fecha_hora, "Temperatura:", datos) # Imprimir la fecha, hora y temperatura
        
        # Enviar la lectura a Firebase en tiempo real
        lecturas_ref.push(lectura)

        # Esperar 1 segundo antes de la próxima lectura
        time.sleep(1)

except KeyboardInterrupt:
    pass # Capturar la excepción si se presiona Ctrl+C para salir

finally:
    puerto_serial.close() # Cerrar el puerto serial al finalizar
