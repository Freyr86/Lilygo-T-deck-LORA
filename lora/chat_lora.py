"""
Desciption:
    Class chat pour le réseau LoRa sur la base de son module SX1262
    Version console (pas de GUI) activer le module LoRa au démarage et le relache a la fin
    Version compatible avec le lilygo t-deck

Version: 1.0

Auteur: Aymon Ludovic

Dépendance:
    - sx1262
    - board
    - time

Mise à jour:
    24.12.2023
    - Mise en place de la base
    - Rajout de la commande /exit
    - Les commande seront basser sur les commande admin de IRC
    - pseudo de base user

    28.12.2023
    - Rajout de la commande /pseudo
    - Rajout de la commande /help
    - recharche pour utilisation clavier et rx lora sans blocage
    - verification etas IRQ
    - création d'un interuption pour gestion de la rx lora

    05.01.2024
    - Rajout de la commande /freq
    - Test de communication ok en half duplex
    - Fonctionnement de base ok sur 2 appreil
    - Test de fréquence de 150Mhz à 960Mhz ok
    - Ajout de la commande largeur de bande /bandwidth
    - Ajout de la commande puissance d'envoie /power
    - Test commande /power ok

    07.01.2023
    - Ajout de la commande niveau de coding /coder
    - Test commande /coder ok
    - Ajout de la commande rssi /rssi
    - Test commande /rssi ok
    - Ajoute de l'import commande pour modifier l'affichage REPL
    - Modification de la couleur REPL en fonction de l'etas de transmission
        Vert en cours d'envoie
        Jaune en cours de reception
    
    08.01.2023
    - Test de l'initialisation FSK pour les message longue portée pas de 
      changement notable de la valeur RSSI il faudrait tester la portée
    - La couleur du text jaune n'est pas jaune mais bleu
    - Modification de la detection de "newline"

    09.01.2023
    - Changement du text d'ouverture
    - Ajoute de la gestion d'un ficher de sauvgarde de configuration

    13.01.2023
    - Correction de léa commande pseudo
    - Création du module du module de charge et de sauvgarde de configuration
    - Ajout de la commande de sauvgarde /save
    - Test de la sauvgarde ok
    - Test de la charge ok
    - Ajout du pseudo dans le text de départ





"""
#importation des bibliothèques
from sx1262 import SX1262
from module import clavier_gestion
import board
import digitalio
import time
from module import cmd
import sys
import storage


class chat_lora:
    #démarage du système LoRa
    def __init__(self, freq=434):
        #Déclaration du module LoRa
        self.sx = SX1262(spi_bus=board.SPI, clk=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.LORA_CS, irq=board.LORA_DIO1, rst=board.LORA_RST, gpio=board.LORA_BUSY)
        
        #initialisation du module LoRa
        #"""
        self.sx.begin(freq=freq, bw=500.0, sf=12, cr=8, syncWord=0x12,
                power=-5, currentLimit=60.0, preambleLength=8,
                implicit=False, implicitLen=0xFF,
                crcOn=True, txIq=False, rxIq=False,
                tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
        #"""

        #self.sx.beginFSK()

        #déclaration du clavier
        self.clavier = clavier_gestion.clavier()

        #déclaration de variable reception
        self.txt_ecrit = ""

        #déclaration de la boucle principale
        self.main_loop = True
        
        #declaration de la variable pseudov nm,
        self.pseudo = "user"

        #déclaration de la variable rssi
        self.rssi = False

        #couleur d'afficahge selon etas
        self.col_standby = None
        self.col_rx = None
        self.col_tx = None
        
        # chargement de sauvgarde si elle existe
        self.load_parametre()
        

    #déclaration de l'interuption
    async def rx_lora(self):
        if board.LORA_DIO1.value:
            print("rx")
        
    #arret complet du système LoRa
    def __del__(self):
        self.sx.__del__()
        del self.sx
        del self.clavier
        del self.txt_ecrit
        del self.main_loop

    #commande help
    def help(self):
        print("Commandes:  /exit pour quitter")
        print("            /pseudo pour changer de pseudo")
        print("            /help pour afficher l'aide")
        print("            /freq pour changer de fréquence")
        print("            /bandw pour changer largeur de bande")
        print("            /power pour changer la puissance envoie")
        print("            /coder pour changer le niveau de coding")
        print("            /rssi pour activer/desactiver le rssi")
        print("            /save pour sauvgarder les parametre")


    #commande fréquence
    def help_freq(self):
        print("Commande fréquence: /freq [fréquence]")
        print("            [fréquence] = fréquence en MHz")
        print("            Fréquence disponible:")
        print("            Entre 150Mhz et 960Mhz")

    #commande largeur de bande
    def help_bandwidth(self):
        print("Commande largeur de bande: /bandw [largeur de bande]")
        print("            [largeur de bande] = largeur en kHz")
        print("            Largeur de bande disponible:")
        print("            7.8, 10.4, 15.6, 20.8, 31.25,")
        print("            41.7, 62.5, 125, 250, 500")

    #commande puissance d'envoie
    def help_power(self):
        print("Commande puissance d'envoie: /power [puissance]")
        print("            [puissance] = puissance en dBm")
        print("            Puissance disponible:")
        print("            Entre -9 et 22")

    #commande niveau de coding
    def help_coder(self):
        print("Commande niveau de coding: /coder [niveau]")
        print("            [niveau] = niveau de coding")
        print("            Niveau disponible:")
        print("            5, 6, 7, 8")
        print("            Plus le coding est elevé plus")
        print("            le taux de transfert est faible")
        print("            mais la fiabilité du transfère") 
        print("            est meilleur")

    #commande rssi
    def help_rssi(self):
        print("Commande rssi: /rssi [etat]")
        print("            [etat] = etat de l'affichage")
        print("            Etat disponible:")
        print("            on, off")
        print("            Affiche le rssi de la derniere reception")
        print("            devant le message en dBm")

    #sauvgarde des parametre
    def save_parametre(self):
        try:
            #essayer de remonter le système de fichier lecture ecriture
            storage.remount("/",False)

            #verification existance du fichier
            if cmd.file_exist("/lora/sav_lora_parametre.py"):
                #suppression du fichier
                cmd.rm("/lora/sav_lora_parametre.py")

            #création et ouveture du fichier
            f = open("/lora/sav_lora_parametre.py", "w")

            #ecriture du début de fichier
            f.write("PARAMETRE = {\n")

            #ecirture des parametre
            f.write("'pseudo': '" + self.pseudo + "',\n")
            f.write("'freq': " + str(self.sx.getFreq()) + ",\n")
            f.write("'bandwidth': " + str(self.sx.getBandwidth()) + ",\n")
            f.write("'power': " + str(self.sx.getOutputPower()) + ",\n")
            f.write("'coderate': " + str(self.sx.getCoderate()) + ",\n")
            f.write("'rssi': " + str(self.rssi) + "\n")

            #ecriture de la fin de fichier
            f.write("}")

            #fermeture du fichier
            f.close()
            storage.remount("/",True)

        except Exception as err:
            print(str(err))

    #chargement des parametre
    def load_parametre(self):
        #verification de l'existance d'un fichier de sauvgarde
        if cmd.file_exist("/lora/sav_lora_parametre.py"):
            #importation du fichier
            from lora import sav_lora_parametre

            #chargement des parametre
            self.pseudo = sav_lora_parametre.PARAMETRE['pseudo']
            self.sx.setFrequency(sav_lora_parametre.PARAMETRE['freq'])
            self.sx.setBandwidth(sav_lora_parametre.PARAMETRE['bandwidth'])
            self.sx.setOutputPower(sav_lora_parametre.PARAMETRE['power'])
            self.sx.setCoderate(sav_lora_parametre.PARAMETRE['coderate'])
            self.rssi = sav_lora_parametre.PARAMETRE['rssi']
            
    #méthode principal
    def run(self):
        #inisalisation de l'ecrant
        for i in range(0, 20):
            print("")

        #affichage commande de base
        print("Bienvenue sur le chat LoRa V1.00")
        print("Pseudo " + self.pseudo)
        print("Frequence " + str(self.sx.getFreq()) + "Mhz")
        print("Bandwidth " + str(self.sx.getBandwidth()) + "kHz")
        print("Power " + str(self.sx.getOutputPower()) + "dBm")
        print("Coderate " + str(self.sx.getCoderate()))
        print("")
        print("/help pour plus d'information")

        #initialisation varaible texte
        temp_txt = ""

        #passage puce en mode récéption
        self.sx.setRx()

        #attente entrée clavier
        while self.main_loop:
            #verificatio entrée clavier
            temp_txt = str(clavier_gestion.input_limit(temp_txt))
            

            #si entrée clavier
            if "\n" in temp_txt:
                #reduction du la fin de texte
                temp_txt = temp_txt.replace(" \n ", "")

                #verification de commande spéciale
                #sortie de programme
                if "/exit" in temp_txt:
                    self.main_loop = False

                #commande help
                elif "/help" in temp_txt:
                    self.help()
                #commande pseudo
                elif "/pseudo" in temp_txt:
                    temp_txt = temp_txt.replace("/pseudo", "")
                    #gestion changeemnt de pseudo
                    if len(temp_txt) > 1:
                        self.pseudo = temp_txt[1:len(temp_txt)]
                        print(" Pseudo changé en: " + self.pseudo)
                    #affichage du pseudo actuel
                    else:
                        print(" Pseudo actuel: " + self.pseudo)

                #commande fréquence
                elif "/freq" in temp_txt:
                    val_frequ = 0
                    temp_txt = temp_txt.replace("/freq", "")
                    #gestion changement de fréquence
                    if len(temp_txt) > 1:

                        try:
                            #extraction de la fréquence
                            val_frequ = int(temp_txt)

                            #verification de la fréquence
                            if val_frequ >= 150 and val_frequ <= 960 :
                                #passage de la puce en standby
                                self.sx.setStandBy()
                                #change^ment de fréquence
                                self.sx.setFrequency(val_frequ)
                                #passage de la puce en récéption
                                self.sx.reset_stat()
                                #information de changement de fréquence
                                print(" Fréquence changé en: " + str(val_frequ) + "Mhz")
                            #fréquence invalide
                            else:
                                print(" Fréquence " + str(val_frequ) + " invalide")
                                self.help_freq()
                        #erreur de conversion
                        except Exception as err:
                            print("Erreur de conversion eviter les espace et le lettre")
                            print("*ERROR* Exception:",str(err))
                    
                    #affichage de la fréquence actuel
                    else:
                        print(" Fréquence actuel: " + str(self.sx.getFreq()) + "Mhz")
                        self.help_freq()    

                #commande largeur de bande
                elif "/bandw" in temp_txt:
                    val_bandwidth = 0
                    temp_txt = temp_txt.replace("/bandw", "")
                    #gestion changement de largeur de bande
                    if len(temp_txt) > 1:

                        try:
                            #extraction de la largeur de bande
                            val_bandwidth = float(temp_txt)

                            #verification de la largeur de bande
                            if val_bandwidth == 7.8 or val_bandwidth == 10.4 or val_bandwidth == 15.6 or val_bandwidth == 20.8 or val_bandwidth == 31.25 or val_bandwidth == 41.7 or val_bandwidth == 62.5 or val_bandwidth == 125 or val_bandwidth == 250 or val_bandwidth == 500:
                                #passage de la puce en standby
                                self.sx.setStandBy()
                                #change^ment de largeur de bande
                                print(self.sx.setBandwidth(val_bandwidth))
                                #passage de la puce en récéption
                                self.sx.reset_stat()
                                #information de changement de largeur de bande
                                print(" Largeur de bande changé en: " + str(val_bandwidth) + "kHz")
                            #largeur de bande invalide
                            else:
                                print(" Largeur de bande " + str(val_bandwidth) + " invalide")
                                self.help_bandwidth()
                        #erreur de conversion
                        except Exception as err:
                            print("Erreur de conversion eviter les espaces et les lettres")
                            print("*ERROR* Exception:",str(err))
                    
                    #affichage de la largeur de bande actuel
                    else:
                        print(" Largeur de bande actuel: " + str(self.sx.getBandwidth()) + "kHz")
                        self.help_bandwidth()

                #envoie de du texte
                elif temp_txt[0:1] != "/":
                    #changement de la couleur en vert pour l'envoie
                    cmd.color_text(cmd.COLOR['green'])

                    #envoie message
                    self.sx.send(b'' + self.pseudo + ": " + temp_txt)
                    
                    #affichage message avec pseudo
                    for i in range(0, len(temp_txt)):
                        print("\x08 \x08",end="")
                    print(self.pseudo + ": " + temp_txt)

                    #effacement etas lora
                    self.sx.reset_stat()

                    #retour de la couleur text en blanc
                    cmd.color_text(cmd.COLOR['white'])

                #changement de la puissance d'envoie
                elif "/power" in temp_txt:
                    #recupération power
                    temp_txt = temp_txt.replace("/power", "")
                    if len(temp_txt) > 1:
                        try:
                            pwr = int(temp_txt)

                            #verification valeur
                            if pwr <= -9 and pwr >= 22:
                                print(" Puissance invalide")
                            else:
                                #changement de la puissance d'envoie
                                self.sx.setOutputPower(pwr)
                                print(" Puissance d'envoie changé en: " + str(pwr) + "dBm")
                        except Exception as err:
                            print("Erreur de conversion eviter les espaces et les lettres")
                            print("*ERROR* Exception:",str(err))

                    #affichage de la puissance d'envoie actuel
                    else:
                        print(" Puissance d'envoie actuel: " + str(self.sx.getOutputPower()) + "dBm")
                        self.help_power()

                #commande du lvl de coding
                elif "/coder" in temp_txt:
                    #recupération du lvl de coding
                    temp_txt = temp_txt.replace("/coder", "")
                    if len(temp_txt) > 1:
                        try:
                            #conversion du lvl de coding
                            coder = int(temp_txt)

                            #verification du lvl de coding
                            if coder <= 8 and coder >= 5:
                                #changement du lvl de coding
                                self.sx.setCoderate(coder)
                                print(" LVL de coding changé en: " + str(coder))
                            else:
                                print(" LVL de coding invalide")
                        except Exception as err:
                            print("Erreur de conversion eviter les espaces et les lettres")
                            print("*ERROR* Exception:",str(err))

                    #affichage du lvl de coding actuel
                    else:
                        print(" LVL de coding actuel: " + str(self.sx.getCoderate()))
                        self.help_coder()

                #commande rssi
                elif "/rssi" in temp_txt:
                    #recupération de l'etat
                    temp_txt = temp_txt.replace("/rssi", "")
                    if len(temp_txt) > 1:
                        #activation
                        if "on" in temp_txt:
                            self.rssi = True
                            print(" Affichage du rssi activé")
                        #desactivation
                        elif "off" in temp_txt:
                            self.rssi = False
                            print(" Affichage du rssi desactivé")
                        #etat invalide
                        else:
                            print(" Etat invalide")
                            self.help_rssi()
                    #affichage de l'etat actuel
                    else:
                        print("Derrniere rssi: " + str(self.sx.getRSSI()) + "dBm")
                        if self.rssi:
                            print(" Affichage du rssi actif")
                        else:
                            print(" Affichage du rssi inactif")
                        self.help_rssi()

                #commande sauvgarde
                elif "/save" in temp_txt:
                    self.save_parametre()
                    print(" Sauvgarde des parametre effectué")

                #commmande de test
                elif "/test" in temp_txt:
                    self.sx.test()

                #cmd inconu
                else:
                    #commande inconnu
                    print(" Commande inconu")

                #effacement variable
                temp_txt = ""

            #recupération des message
            msg = self.sx.run_recev()

            #self.sx.test()

            #si message plus long que 0 impression
            if len(msg) > 0:

                #modification du message avec valeur rssi
                if(self.rssi):
                    msg = " RSSI: " + str(self.sx.getRSSI()) + "dBm " + msg

                #print du message
                print(msg)
                self.sx.reset_stat()

                #retour de la couleur text en blanc
                cmd.color_text(cmd.COLOR['white'])

        #passage puce en mode standby
        self.sx.setStandBy()
        #destruction object Lora
        self.__del__()
        #nettoyage ecrant 
        for bcl in range(0, 20):
            print("")
