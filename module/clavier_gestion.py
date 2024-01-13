#################################################################################
#                                                                               #
#   Gestion de la console circuitPython drectement avec le clavier du t-deck    #
#   Module de commande avancer                                                  #
#                                                                               #
#   Un grand merci à:   RetiredWizard                                           #
#   Github:             https://github.com/RetiredWizard/                       #
#                                                                               #
#   Modifier par:       Freyr86                                                 #
#   Github:             https://github.com/Freyr86                              #
#                                                                               #
#################################################################################
from sys import stdin,stdout,implementation

import board
import displayio
import time
from time import sleep
from supervisor import runtime
from adafruit_bus_device.i2c_device import I2CDevice
import countio
import keypad

def sleep_ms(ms):
    sleep(ms/1000)

#déclaration du clavier
class clavier:

    persiste_txt = ""

    def __init__(self):
        self._key = bytearray(1)
       	self._touched = False
        _ADDRESS_KBD = 0x55

        self._i2c = I2CDevice(board.I2C(), _ADDRESS_KBD)

    def get_screensize(self):
        return (19,52)

    def serial_bytes_available(self):
        if not self._touched:
            retval = 0
            with self._i2c as i2c:
                try:
                    i2c.readinto(self._key)
                except:
                    self._key=bytearray(1)
            if self._key[0] != 0:
                retval = 1
                self._touched = True
            else:
                retval = self.uart_bytes_available()
        else:
            retval = 1

        return retval
    
    def uart_bytes_available(self):
        # Does the same function as supervisor.runtime.serial_bytes_available
        retval = runtime.serial_bytes_available

        return retval

    def read_keyboard(self,num):
        retval = ""
        while num > 0:
            self.serial_bytes_available()
            if self._touched:
                retval = chr(self._key[0])
                self._touched = False
                num -= 1
            else:
                if self.uart_bytes_available():
                    retval = stdin.read(1)
                    num -= 1

        return retval
    
    def read_keyboard_limit(self,num):
        retval = ""
        loop = 0
        while num > 0 and loop < 10:
            self.serial_bytes_available()
            if self._touched:
                #print(self._key[0])
                #gestion des caratère spéciaux
                if self._key[0] == 8:
                    retval = "-1"
                elif self._key[0] == 13:
                    retval = "+1"
                else:
                    retval = chr(self._key[0])
                self._touched = False
                num -= 1
            else:
                if self.uart_bytes_available():
                    retval = stdin.read(1)
                    num -= 1
            loop = loop + 1
            time.sleep(1/1000)

            if loop == 10:
                retval = None
        return retval

in_clav = clavier()

def input(disp_text=None): 

    if disp_text != None:
        print(disp_text,end="")

    bld_chr1 = '_(+'
    bld_chr2 = '-+)'
    bld_chr =  '=[]'
    bld_started = False

    keys = ''
    editCol = 0
    loop = True
    ctrlkeys = ''
    arrow = ''
    onLast = True
    onFirst = True
    blink = True
    timer = time.time()


    while loop:
        #print(editCol,keys)
        if ctrlkeys == '':
            arrow = ""
            trackloop = True
        else:
            ctrlkeys = ''
            trackloop = False
        #recupération clavier
        if in_clav.serial_bytes_available():
            if in_clav.uart_bytes_available():
                keys = keys[:editCol]+stdin.read(1)+keys[editCol:]
                editCol += 1
                if keys[editCol-1] == '\x1b':
                    keys = keys[:editCol-1]+keys[editCol:]
                    ctrlkeys = stdin.read(2)
                    # ctrlkeys = up:[A down:[B right:[C left:[D
                    arrow = ctrlkeys[1]
            else:
                keys = keys[:editCol]+in_clav.read_keyboard(1)+keys[editCol:]
                editCol += 1

            # Convert two character sequences into missing keyboard keys
            # '_-' -> '='     '(+' -> '['       '+)' -> ']'
            bld_done = False
            bcindx = bld_chr2.find(keys[editCol-1:editCol])
            if bld_chr1.find(keys[editCol-1:editCol]) != -1 and not bld_started and arrow == "":
                bld_started = True
            elif keys[editCol-2:editCol] ==  bld_chr1[bcindx]+bld_chr2[bcindx] and bld_started:
                bld_started = False
                keys = keys[:editCol-2]+bld_chr[bcindx]+keys[editCol:]
                print('\x08'+keys[editCol-2:]+' '+('\x08'*(len(keys[editCol:])+(1 if onLast else 2))),end="")
                editCol -= 1
                bld_done = True
            else:
                bld_started = False

            if arrow != "" and ctrlkeys != "":
                editCol -= 1
            elif keys[editCol-1:editCol] == '\x08':
                keys = keys[:max(0,editCol-2)]+keys[editCol:]
                if editCol > 1:
                    print(('\x08'*(editCol-1))+keys+'  \x08\x08',end="")
                    editCol = max(0,editCol-2)
                    if editCol < len(keys):
                        print("\x08"*(len(keys)-editCol),end="")
                else:
                    editCol -= 1
                    onFirst = True
            elif len(keys[editCol-1:editCol]) > 0 and keys[editCol-1:editCol] in '\n\r':
                if len(keys) > editCol:
                    print(keys[editCol:editCol+1]+"\x08",end="")
                elif editCol == len(keys):
                    print(" \x08",end="")
                keys = keys[:editCol-1]+keys[editCol:]
                print()
                loop = False
            elif not bld_done:
                onFirst = False
                print(keys[editCol-1:],end="")
                if len(keys[editCol-1:]) > 1:
                    print(" \x08",end="")
                if editCol < len(keys):
                    print("\x08"*(len(keys)-editCol),end="")

            if loop:
                if time.time() != timer:
                    blink = not blink
                    timer = time.time()

                if blink:
                    print("_\x08",end="")
                else:
                    if len(keys) > editCol:
                        print(keys[editCol:editCol+1]+"\x08",end="")
                    else:
                        print(" \x08",end="")
            
    return keys

#recupératon d'un text console avec limitation de temps et effacement du text
def input_limit(txt=""): 

    #boucle de limitation de temps
    for i in range(0, 30):
        rec_clavier = in_clav.read_keyboard_limit(1)

        #gestion du backspace
        if rec_clavier == "-1":
            if len(txt) > 0:
                txt = txt[:-1]
                print("\x08 \x08",end="")
        #gestion de l'entrée
        elif rec_clavier == "+1":
            txt = txt + " \n "
        #gestion du text autre
        elif rec_clavier != None:
            txt = txt + str(rec_clavier)
            for i in range(0, len(txt)):
                print("\x08 \x08",end="")
            print(txt, end="")
        
        sleep_ms(1)

    return txt
            