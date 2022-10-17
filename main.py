from machine import Pin
import pycom
from BME280 import *
import time

print("test 2")
bus_i2c = I2C(0)
bus_i2c.init(I2C.MASTER, baudrate = 400000)
adr = bus_i2c.scan()
print ('Adresse peripherique I2C :', adr)
Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
capteur_BME280 = BME280 (BME280_I2C_ADR, bus_i2c)
capteur_BME280.Calibration_Param_Load()
print("test2")
while True :
    print("-----------------------")
    x = capteur_BME280.read_temp()
    print("la température est de : ", x)
    y = capteur_BME280.read_pression()
    print("la pression est de : ", y)
    z = capteur_BME280.read_humidity()
    print("l'humidité est de : ",z)
    time.sleep(5)
    print("\n")
