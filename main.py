from machine import Pin,RTC,SD
import pycom
from BME280 import *
from DRV8833 import *
from network import Bluetooth
import time
import _thread
from VL6180X import *

def write_SD(data):
    f = open('/sd/capture.txt', 'w')
    f.write(data)
    f.close()

#class blue_tooth(object):
#    def __init__(self):
#        self.bluetooth = Bluetooth()
#        self.bluetooth.set_advertisement(name='Pycom', service_uuid=b'1234567890123458')
#    def connection_to_pc(self):
#        while self.bluetooth.isscanning():
#            adv = self.bluetooth.get_adv()
#            if adv and self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'PC':
#                print("PC found")
#                break
#            time.sleep_ms(500)
#        print("PC connected")
#    def send_data(self,data):
#        self.bluetooth.set_advertisement(name='Pycom', service_uuid=b'1234567890123458',manufacturer_data=data)
#        self.bluetooth.advertise(True)

def capteur():
    print("-----------------------\n")
    date = time.localtime(time.time())
    print("Time : ", date[2],"/",date[1],"/",date[0]," at ",date[3],":",date[4],":",date[5])
    x = capteur_BME280.read_temp()
    print("la température est de : ", x)
    y = capteur_BME280.read_pression()
    print("la pression est de : ", y)
    z = capteur_BME280.read_humidity()
    print("l'humidité est de : ",z)
    lum = capteur_d_1_VL6180X.ambiant_light_mesure()
    print("la luminosité est de : ",lum)
    print("\n")
    write_SD("Time : "+str(date[2])+"/"+str(date[1])+"/"+str(date[0])+" at "+str(date[3])+":"+str(date[4])+":"+str(date[5])+" la température est de : "+str(x)+" la pression est de : "+str(y)+" l'humidité est de : "+str(z)+" la luminosité est de : "+str(lum))
    #bluetooth.send_data(f"Time : {date[2]}/{date[1]}/{date[0]} at {date[3]}:{date[4]}:{date[5]}\nla température est de : {x}\nla pression est de : {y}\nl'humidité est de : {z}")

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

print("\nInit distance sensor\n")

VL6180X_CE_Pin = "P3"
VL6180X_I2C_adr_defaut = const(0x29)

VL6180X_GPIO_CE_Pin = Pin(VL6180X_CE_Pin, mode=Pin.OUT)
VL6180X_GPIO_CE_Pin.value(1)

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
capteur_d_1_VL6180X = VL6180X(VL6180X_I2C_adr_defaut, bus_i2c)

print("\nset PWM\n")
DRV8833_Sleep_pin = "P20"
DRV8833_AIN1 = "P21"
DRV8833_AIN2 = "P22"
DRV8833_BIN1 = "P12"
DRV8833_BIN2 = "P19"

print("\ninit motors\n")
Moteur_Droit = DRV8833(DRV8833_AIN1, DRV8833_AIN2,DRV8833_Sleep_pin, 1, 500, 0, 1)
Moteur_Gauche = DRV8833(DRV8833_BIN1, DRV8833_BIN2,DRV8833_Sleep_pin, 1, 500, 2, 3)

#print("\ninit bluetooth\n")
#
#bluetooth = blue_tooth()
#bluetooth.connection_to_pc()
#bluetooth.send_data("Init channel")

print("\ninit SD\n")

sd = SD()
os.mount(sd, '/sd')

print("\nset finish")

print("\nRobot ready\n\n-----------------------\n")

delay = 4.0
print("\n")

print("\n-----------------------\n")
print("Robot start\n")


"Si la distance est inférieur à 75cm, le robot tourne jusqu'à ce que la distance soit supérieur à 75cm"
"Toutes les 4 secondes, le robot envoie les données de la température, de la pression et de l'humidité"

last_time = time.time()

while True:
    distance = capteur_d_1_VL6180X.range_mesure()
    print("distance : ", distance)
    if distance < 75:
        tourner_droite(1)
    else:
        avancer(1)
    if (time.time() - last_time) > delay:
        capteur()
