# Gestion des moteurs CC à l'aide du double pont en H DRV8833
# Librairie DRV8833_V2.py
# Loi de commande des moteurs en trs / s
# Génération d'une rampe de vitesse sur [0.0; consigne_pwm_moteur] sur T = 50ms

from micropython import const
from machine import Pin
from machine import PWM
import time

# Définition sens de rotation des moteurs
SENS_HORAIRE = const(1)
SENS_ANTI_HORAIRE = const(2)

VITESSE_MAX = 1.78 # Vitesse de rotation max en tours par seconde

class DRV8833 :
    def __init__  (self, In1_pin, In2_pin, sleep_pin, timer_number, freq, num_channel_pwm_In1, num_channel_pwm_In2, **kwargs) :
        # IN1_pin : entrée PWM 1 DRV8833
        # IN2_pin : entrée PWM 2 DRV8833
        # sleep_pin : SLP pin pour désactiver les ponts en H du DRV8833
        # timer_number : dans [0,1,2,3]. Choix du timer utilisé pour générer le signal pwm
        # freq : fréquence du signal pwm
        # num_channel_pwm_In1 : numéro de l'Id du canal PWM associé à la broche In1_pin
        # num_channel_pwm_In2 : numéro de l'Id du canal PWM associé à la broche In2_pin

        self.DRV8833_Sleep_Pin = Pin(sleep_pin, mode = Pin.OUT) # Initialiser la broche sleep_pin pour gérer le DRV8833
        self.DRV8833_Sleep_Pin.value(0) # Désactive le driver DRV8833
        if timer_number not in [0,1,2,3] :
            raise ValueError(
                'Unexpected timer_number value {0}.'.format(timer_number))
        self.pwm = PWM(timer_number, frequency = freq) # Utiliser le timer n° timer_number en PWM avec une fréquence de base de freq Hz
        self.DRV8833_Pwm_In1 = self.pwm.channel(num_channel_pwm_In1, pin = In1_pin, duty_cycle = 0.0)
        self.DRV8833_Pwm_In2 = self.pwm.channel(num_channel_pwm_In2, pin = In2_pin, duty_cycle = 0.0)
        self.consigne_rotation_roue = 0.0
        self.DRV8833_Sleep_Pin.value(1) # Active le driver DRV8833
        time.sleep(0.05)
        self.sens = SENS_HORAIRE
#---------------------------------------------------------------------------
# Commande d'un moteur :
# paramètres :
#   sens  : sens de rotation
#   consigne_rotation_roue : en tours par seconde
#   La broche SLEEP est toujours activée aprés l'appel au constructeur

    def Cmde_moteur (self, sens, consigne_rotation_roue) :
        self.sens = sens
        if consigne_rotation_roue < 0.0 :
            self.consigne_rotation_roue = 0.0
        elif consigne_rotation_roue > VITESSE_MAX :
            self.consigne_rotation_roue = VITESSE_MAX
        else :
            self.consigne_rotation_roue = consigne_rotation_roue
        consigne_pwm_moteur = self.ToursParSeconde_vers_PWM (self.consigne_rotation_roue)
        if self.sens == SENS_HORAIRE : # forward
            self.DRV8833_Pwm_In2.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN2 (soit 0%)
            for i in range (1, 11) :
                pwm = (i / 10.0) * consigne_pwm_moteur
                self.DRV8833_Pwm_In1.duty_cycle(pwm) # Rapport cyclique à vitesse % sur IN1
                time.sleep (0.005)
        elif self.sens == SENS_ANTI_HORAIRE : # reverse
            self.DRV8833_Pwm_In1.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN1
            for i in range (1, 11) :
                pwm = (i / 10.0) * consigne_pwm_moteur
                self.DRV8833_Pwm_In2.duty_cycle(pwm) # Rapport cyclique à vitesse % sur IN2
                time.sleep (0.005)
#---------------------------------------------------------------------------
# Définitions des mouvements de base de la plateforme robotique
    def Arret_moteur (self) :
        self.DRV8833_Pwm_In1.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN1
        self.DRV8833_Pwm_In2.duty_cycle(0.0) # Rapport cyclique à 0.0 sur IN2
#---------------------------------------------------------------------------
    @staticmethod
    def ToursParSeconde_vers_PWM (consigne_rotation_roue) :
        # Permet de calculer le rapport cyclique de la PWM de commande d'un moteur
        # en fonction de la vitesse de rotation de la roue
        # consigne_rotation_roue dans [0.0 ; 1.78] tours/s
        # Valeur retournée : rapport cyclique dans [0.0 ; 1.0]
        # y = -0,2598x6 + 1,9504x5 - 5,1191x4 + 6,2977x3 - 3,6988x2 + 1,0832x + 0,053
        # Interpolation polynomiale : y = ax^6+bx^5+cx^4+dx^3+ex^2+fx+g avec :
        #    a = -0.8829; -0,2598
        #    b = 5.1708 ; 1,9504
        #    c = -11.456; -5,1191
        #    d = 12.209; 6,2977
        #    e = -6.2879 ; -3,6988
        #    f = 1.5751 ; 1,0832
        #    g = 0.0508 ; 0,053
        # Validé le 06.03.2019
        coeff = (-0.2598, 1.9504, -5.1191, 6.2977, -3.6988, 1.0832, 0.053)

        y = consigne_rotation_roue * coeff[0] + coeff[1]
        for i in range (1, 6) :
            y = consigne_rotation_roue * y + coeff[i+1]
        if y < 0.0 :
            y = 0.0
        elif y > 1.0 :
            y = 1.0
        return y
#------------------------------------------------------------------------
