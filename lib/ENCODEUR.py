# Gestion des encodeurs moteurs
# Définition des ressources associés à chaque Encodeurs
# Définition des modalités d'acquisition des données des Encodeurs
# Inclus la gestion des encodeurs pour :
#   - la mesure de vitesse de rotation des moteurs
#   - la gestion du contrôleur PID
#   - La gestion de la fonction Odométrie
# Librairie Encodeur_V2.py

from micropython import const
from machine import Pin
from machine import Timer

# Enc_voieA_pin : broche de la carte WiPy qui reçoit les ticks de la voie A de l'encodeur
# Enc_voieB_pin : broche de la carte WiPy qui reçoit les ticks de la voie B de l'encodeur
# Id_moteur : permettre d'identifier le moteur droit ou gauche
# Attributs :
# ticks_voieA : compteur de ticks voie A encodeur
# ticks_voieB: compteur de ticks voie B encodeur

RESOLUTION_CODEUR = const(1400) # Moteur : rapport de réduction 100:1
                                # Codeur : 14 ticks pour un tour d'arbre moteur
# Id moteurs
Id_Moteur_Droit = const(1)
Id_Moteur_Gauche = const(2)
#---------------------------------------------------------------------------

class ENCODEUR :
    def __init__ (self, Enc_voieA_pin, Enc_voieB_pin, Id_moteur) :

        # Affectation des broches des encodeurs
        self.Enc_voieA_pin = Enc_voieA_pin
        self.Enc_voieB_pin = Enc_voieB_pin
        self.EncodeurA = Pin(self.Enc_voieA_pin, mode = Pin.IN, pull=Pin.PULL_UP)
        self.EncodeurB = Pin(self.Enc_voieB_pin, mode = Pin.IN, pull=Pin.PULL_UP)
        self.Id_moteur = Id_moteur
        # Définition des modalités d'IT et d'appel des routines d'IT associées aux encodeurs
        self.EncodeurA.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.IT_EncodeurA) # Interruption sur fronts montant et descendant
        self.EncodeurB.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.IT_EncodeurB) # Interruption sur fronts montant et descendant

        self.ticks_voieA_odometrie = 0
        self.ticks_voieB_odometrie = 0
        self.type_deplacement = 0  # Permettre de connaître la nature du déplacement (Avancer : 16, Reculer : 8, Pivoter Droit : 4, Pivoter Gauche : 2, Arret : 1)
                                   #  pour la gestion des encodeurs associés à l'odométrie
#---------------------------------------------------------------------------
# Fonction de gestion des encodeurs moteurs : gestion par IT
    def IT_EncodeurA (self, arg) :

        if (self.Id_moteur == Id_Moteur_Droit) :
            if (self.type_deplacement == 16 or self.type_deplacement == 2) : # Si Avancer ou Pivoter gauche
                self.ticks_voieA_odometrie += 1
            elif (self.type_deplacement == 8 or self.type_deplacement == 4) : # Si Reculer ou Pivoter droit
                self.ticks_voieA_odometrie -= 1
        elif (self.Id_moteur == Id_Moteur_Gauche) :
            if (self.type_deplacement == 8 or self.type_deplacement == 2) : # Si Reculer ou Pivoter gauche
                self.ticks_voieA_odometrie -= 1
            elif (self.type_deplacement == 16 or self.type_deplacement == 4) : # Si Avancer ou Pivoter droit
                self.ticks_voieA_odometrie += 1

    def IT_EncodeurB (self, arg) :

        if (self.Id_moteur == Id_Moteur_Droit) :
            if (self.type_deplacement == 16 or self.type_deplacement == 2) : # Si Avancer ou Pivoter gauche
                self.ticks_voieB_odometrie += 1
            elif (self.type_deplacement == 8 or self.type_deplacement == 4) : # Si Reculer ou Pivoter droit
                self.ticks_voieB_odometrie -= 1
        elif (self.Id_moteur == Id_Moteur_Gauche) :
            if (self.type_deplacement == 8 or self.type_deplacement == 2) : # Si Reculer ou Pivoter gauche
                self.ticks_voieB_odometrie -= 1
            elif (self.type_deplacement == 16 or self.type_deplacement == 4) : # Si Avancer ou Pivoter droit
                self.ticks_voieB_odometrie += 1
