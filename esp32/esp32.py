from machine import Pin, ADC, I2C
from time import sleep
import bmp280


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = bmp280.BMP280(i2c)


ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # 0-3.3V

humidity_sensor = ADC(Pin(35))
humidity_sensor.atten(ADC.ATTN_11DB)


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    try:
        # Lecture capteurs
        temp = bmp.temperature
        pressure = bmp.pressure
        light = ldr.read()
        humidity = humidity_sensor.read()
        humidity_pct = map_value(humidity, 0, 4095, 0, 100)

        # Envoi UART vers Raspberry
        print("T:{:.1f},P:{:.1f},H:{:.1f},L:{}".format(temp, pressure, humidity_pct, light))

        sleep(1)

    except Exception as e:
        print("Erreur capteur :", e)
        sleep(2)
