from machine import Pin,RTC
import pycom
from BME280 import *
import time
import _thread

def capteur(delay,remaining):
    start = time.time()
    while (time.time()-start) < remaining :
        time.sleep(delay)
        print("-----------------------\n")
        date = time.localtime(time.time())
        print("Time : ", date[2],"/",date[1],"/",date[0]," at ",date[3],":",date[4],":",date[5])
        x = capteur_BME280.read_temp()
        print("la température est de : ", x)
        y = capteur_BME280.read_pression()
        print("la pression est de : ", y)
        z = capteur_BME280.read_humidity()
        print("l'humidité est de : ",z)
        print("\n")
    print("finish")

print("\n-----------------------\n")
print("Robot init :\n")

print("set time\n")
rtc = RTC()
rtc.init((2022,11,4,15,5,0,0))
print(rtc.now())

print("\nset I2C\n")
bus_i2c = I2C(0)
bus_i2c.init(I2C.MASTER, baudrate = 400000)
adr = bus_i2c.scan()
print("scan bus I2C")
print ('Adresse peripherique I2C :', adr)
Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
capteur_BME280 = BME280 (BME280_I2C_ADR, bus_i2c)
capteur_BME280.Calibration_Param_Load()

print("\nset finish")

print("\nRobot ready\n\n-----------------------\n")

delay = input("Entrer le temps entre chaque prise de température, humidité et pression (en secondes):\n")
print("\n")
while True :
    try:
        delay = float(delay)
        break
    except ValueError:
        print("Valeur incorrecte")
        delay = input("Entrer le temps entre chaque prise de température, humidité et pression (en secondes):\n")
        print("\n")

remaining = input("Pendant combien de temps le robot doit-il prendre les mesures (en secondes):\n")
print("\n")
while True :
    try:
        remaining = float(remaining)
        break
    except ValueError:
        print("Valeur incorrecte")
        remaining = input("Pendant combien de temps le robot doit-il prendre les mesures (en secondes):\n")
        print("\n")

print("\n-----------------------\n")
print("Robot start\n")
_thread.start_new_thread(capteur, [delay,remaining])
time.sleep(remaining+5)
