from machine import Pin,RTC
import pycom
from BME280 import *
from DRV8833 import *
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

def avancer(vitesse):
    consigne_rotation_roue = vitesse
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    time.sleep(1)
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()
    return None

def reculer(vitesse):
    consigne_rotation_roue = vitesse
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    time.sleep(1)
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()
    return None

def tourner_droite(vitesse):
    consigne_rotation_roue = vitesse
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    time.sleep(1)
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()
    return None

def tourner_gauche(vitesse):
    consigne_rotation_roue = vitesse
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    time.sleep(1)
    Moteur_Gauche.Arret_moteur()
    Moteur_Droit.Arret_moteur()
    return None

def deplacement(remaining):
    start = time.time()
    while time.time() < start+remaining:
        avancer(1)
        reculer(1)
        tourner_droite(1)
        tourner_gauche(1)

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

print("\nset PWM\n")
DRV8833_Sleep_pin = "P20"
DRV8833_AIN1 = "P21"
DRV8833_AIN2 = "P22"
DRV8833_BIN1 = "P12"
DRV8833_BIN2 = "P19"

print("\ninit motors\n")
Moteur_Droit = DRV8833(DRV8833_AIN1, DRV8833_AIN2,DRV8833_Sleep_pin, 1, 500, 0, 1)
Moteur_Gauche = DRV8833(DRV8833_BIN1, DRV8833_BIN2,DRV8833_Sleep_pin, 1, 500, 2, 3)

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
stop = time.time()+remaining
now = time.time()
_thread.start_new_thread(capteur, [delay,remaining])
_thread.start_new_thread(avancer, [1])
time.sleep(2)
_thread.start_new_thread(reculer, [1])
time.sleep(2)
_thread.start_new_thread(tourner_droite, [1])
time.sleep(2)
_thread.start_new_thread(tourner_gauche, [1])
time.sleep(2)
now = time.time()
print("motors finish")
