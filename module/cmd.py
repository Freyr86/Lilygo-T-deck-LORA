#################################################################################
#                                                                               #
#   Gestion de la console circuitPython drectement avec le clavier du t-deck    #
#   Module de commande avancer                                                  #
#                                                                               #
#   Modifier par:   Freyr86                                                     #
#   Github:         https://github.com/Freyr86                                  #
#                                                                               #
#################################################################################

"""
Màj: 
10.09.2021:
    - Modification nano pour ecrire dans les fichier avec cd
    - Test modification nano ok
    - Ajout de la gestion SD card

"""


import os
import sys
import builtins
import storage
import module
import board
from analogio import AnalogIn
from time import sleep
import busio
import sdcardio

def SDCard_init():
    try:
        #initialisation de la SD
        spi = board.SPI()
        sdcard = sdcardio.SDCard(spi, board.SDCARD_CS)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        print("SD Card OK")
        return True
    except Exception as err:
        print("SD erreur:",str(err))
        return False

def sleep_ms(ms):
    sleep(ms/1000)
    
def cls():
    for loop in range(0,20):
        print()

def nano(chemin):
    from module import nano
    #recupération du chemin
    size = len(chemin)
    if size > 5:
        chemin = chemin[5:size]
        if len(os.getcwd()) > 1:
            chemin = os.getcwd() + "/" + chemin
        nano.nano_call(chemin)
    else:
        print("Entrée un nom de fichier 2")

def ls(chemin):
    #recupération du chemin
    size = len(chemin)
    chemin = chemin[3:size]

    #récupération de la liste de fichier
    try:
        file_list = os.listdir(chemin)

        #récupéraion de la longeur du tableau
        size = len(file_list)

        #renvoie des dossiers
        for loop in range(0,size):
            if not "." in file_list[loop]:
                if not "System Volume Information" in file_list[loop]:
                    print(file_list[loop])
        
        #renvoie des fichier
        for loop in range(0,size):
            if "." in file_list[loop]:
                if file_list[loop][0:1] != '.':
                    print(file_list[loop])

    #gestion des exception
    except Exception as err:
        print("*ERREUR* Exeception:",str(err))

def rmdir(chemin):
    #recupération du chemin
    size = len(chemin)
    chemin = chemin[6:size]

    #effacement du dossier
    try:
        #effacement du dossier
        storage.remount("/",False)
        os.rmdir(chemin)
        storage.remount("/",True)
    
    #gestion des exception
    except Exception as err:
        print("*ERREUR* Exeception:",str(err))

def rm(chemin):
    #recupération du chemin
    size = len(chemin)
    chemin = chemin[3:size]

    #effacement du dossier
    try:
        #effacement du dossier
        storage.remount("/",False)
        os.remove(chemin)
        storage.remount("/",True)
    
    #gestion des exception
    except Exception as err:
        print("*ERREUR* Exeception:",str(err))

def cd(chemin):
    #recupération du chemin
    size = len(chemin)
    chemin = chemin[3:size]

    #changement du dossier
    try:
        os.chdir(chemin)
    #gestion des exception
    except Exception as err:
        print("*ERREUR* Exeception:",str(err))

def mkdir(chemin):
    #recupération du chemin
    size = len(chemin)
    chemin = chemin[6:size]

    #changement du dossier
    try:
        storage.remount("/",False)
        os.mkdir(chemin)
    except Exception as err:
        print("*ERREUR* Exeception:",str(err))

def voltage():
    #retourne voltage batterie
    #attache pin
    #CALIBRATION NESSECAIRE

    batt_in = AnalogIn(board.IO4)

    #changement de la référence
    print(batt_in.reference_voltage)

    #calcul voltage
    voltage = batt_in.value * 3.3 / 65536

    #relachement pin
    batt_in.deinit()

    #retourne le voltage
    return voltage

def batt_charge():
    #4.2V < x = 100%  
    #3.3V > x = 0%
    #CALIBRATION NESSECAIRE
    
    max = 4.2
    min = 3.3

    #attache pin
    batt_in = AnalogIn(board.IO4)

    #calcul charge
    charge = 100 / (max - min) * (batt_in.value * 3.3 / 65536 - min) 

    #relachement pin
    batt_in.deinit()

    #retourne la charge en %
    return charge

def reload():
    #recharge le module
    import supervisor
    supervisor.reload()

def reboot():
    #rebooter l'appareil
    import microcontroller
    microcontroller.reset()

def color_text(color = 0xFFFFF):
    #change la couleur du texte REPL
    board.DISPLAY.root_group[2].pixel_shader[1]=color

def dir_exist(chemin):
    #verification de l'existance du dossier
    try:
        os.stat(chemin)
        return True
    except:
        return False
    
def file_exist(chemin):
    #verification de l'existance du fichier
    try:
        f = open(chemin)
        f.close()
        return True
    except:
        return False

COLOR = {
    'red' : 0x0000FF,
    'green' : 0x00FF00,
    'blue' : 0xFF0000,
    'yellow' : 0x00FFFF,
    'purple' : 0xFF00FF,
    'cyan' : 0xFFFF00,
    'white' : 0xFFFFFF,
    'black' : 0x000000
}
    