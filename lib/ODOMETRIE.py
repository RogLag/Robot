# Gestion de l'estimation de la position - oientation du Pos_Orient_Robot
# Validé le09.04.2021

from ENCODEUR_V2 import RESOLUTION_CODEUR
from machine import Timer
import math
from math import cos
from math import sin
from math import fmod

RAYON_ROUE = 4.24 / 2.0  # cm ; 5.1 cm
L = 11.4  # distance des points de contacts entre les roues gauche et droite en cm; 8.35 cm
p = 2.0 * math.pi * RAYON_ROUE # Périmètre de la roue en cm

class ODOMETRIE :
    # x_pos : position initiale du robot selon x
    # y_pos : position initiale du robot selon y
    # theta : orientation initiale du robot
    # Delta_T : période d'échantillonnage de l'odométre en ms

    # Encodeur_Mot_Droit : ressources associés à l'encodeur du moteur droit
    # Encodeur_Mot_Gauche : ressources associés à l'encodeur du moteur gauche

    def __init__ (self, x_pos, y_pos, theta, Delta_T, Encodeur_Mot_Droit, Encodeur_Mot_Gauche) :
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.theta = theta
        self.Delta_T = Delta_T
        self.Encodeur_Mot_Droit = Encodeur_Mot_Droit
        self.Encodeur_Mot_Gauche = Encodeur_Mot_Gauche
        self.Encodeur_Mot_Droit.ticks_voieA_odometrie = 0
        self.Encodeur_Mot_Droit.ticks_voieB_odometrie = 0
        self.Encodeur_Mot_Gauche.ticks_voieA_odometrie = 0
        self.Encodeur_Mot_Gauche.ticks_voieB_odometrie = 0

        self.Moteur_Droit_ticks_voieA = 0
        self.Moteur_Droit_ticks_voieB = 0
        self.Moteur_Gauche_ticks_voieA = 0
        self.Moteur_Gauche_ticks_voieB = 0

        self.Moteur_Droit_ticks_voieA_prec = 0
        self.Moteur_Droit_ticks_voieB_prec = 0
        self.Moteur_Gauche_ticks_voieA_prec = 0
        self.Moteur_Gauche_ticks_voieB_prec = 0


        self.alarm = Timer.Alarm(self.IT_Delta_x_y_theta, ms = self.Delta_T, periodic = True)
#------------------------------------------------------------------------
    def IT_Delta_x_y_theta (self, arg) :

        Delta_ticks_Md_EncA = self.Encodeur_Mot_Droit.ticks_voieA_odometrie - self.Moteur_Droit_ticks_voieA_prec
        Delta_ticks_Md_EncB = self.Encodeur_Mot_Droit.ticks_voieB_odometrie - self.Moteur_Droit_ticks_voieB_prec
        Delta_ticks_Mg_EncA = self.Encodeur_Mot_Gauche.ticks_voieA_odometrie - self.Moteur_Gauche_ticks_voieA_prec
        Delta_ticks_Mg_EncB = self.Encodeur_Mot_Gauche.ticks_voieB_odometrie - self.Moteur_Gauche_ticks_voieB_prec

        self.Moteur_Droit_ticks_voieA_prec = self.Encodeur_Mot_Droit.ticks_voieA_odometrie
        self.Moteur_Droit_ticks_voieB_prec = self.Encodeur_Mot_Droit.ticks_voieB_odometrie
        self.Moteur_Gauche_ticks_voieA_prec = self.Encodeur_Mot_Gauche.ticks_voieA_odometrie
        self.Moteur_Gauche_ticks_voieB_prec = self.Encodeur_Mot_Gauche.ticks_voieB_odometrie

        delta_l_roue_gauche = p * (Delta_ticks_Mg_EncA + Delta_ticks_Mg_EncB) * 0.5 / RESOLUTION_CODEUR # Distance parcourue par la roue gauche
        delta_l_roue_droite = p * (Delta_ticks_Md_EncA + Delta_ticks_Md_EncB) * 0.5 / RESOLUTION_CODEUR # Distance parcourue par la roue droite
        delta_l_moyen = 0.5 * (delta_l_roue_droite + delta_l_roue_gauche) # distance moyenne parcourue par le robot

        delta_x_pos = delta_l_moyen * cos(self.theta)
        delta_y_pos = delta_l_moyen * sin(self.theta)
        delta_theta = (delta_l_roue_droite - delta_l_roue_gauche) / L # En radian

        self.x_pos += delta_x_pos
        self.y_pos += delta_y_pos
        self.theta += delta_theta
        self.theta = fmod(self.theta, math.pi) # Valeur de theta dans [-Pi,+Pi]
