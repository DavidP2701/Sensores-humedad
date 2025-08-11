import serial
import requests
import time

# Cambia el numero de puerto de tu lap, consulta en terminal con comando: ls /dev/tty.usb*.
dispositivo = "COM6"
baud_rate = 115200

try:
    ser = serial.Serial(dispositivo, baud_rate, timeout=1)
    print(f"Conectado a {dispositivo}")
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
    exit()

api_key = 'QRHJ825J9TUYME42'
url = "https://api.thingspeak.com/update"

while True:
    try:
        data = ser.readline().decode('utf-8').strip()

        if data:
            try:
                valores = data.split(',')
                if len(valores) == 3:
                    lectura, humedadMin, humedadMax = map(int, valores)

                    payload = {
                        "api_key": api_key,
                        "field1": lectura,
                        "field2": humedadMin,
                        "field3": humedadMax
                    }

                    response = requests.get(url, params=payload)
                    print(f"Enviado: {payload} | Respuesta: {response.status_code}")
                else:
                    print(f"Formato incorrecto: {data}")
            except ValueError:
                print(f"Error al convertir: {data}")

        time.sleep(10)

    except Exception as e:
        print(f"Error general: {e}")
        break