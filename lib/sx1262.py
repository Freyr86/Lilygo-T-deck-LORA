"""
Desciption:
    classe de gestion du module sx1262 baser sur une classe ecrite par
    ehong-tl
    https://github.com/ehong-tl

Modifier par: Aymon Ludovic

V1.00

    13.01.2024
    - Ajout de la fonction run_recev pour verification de reception de message
    - Ajout de la fonction reset_stat pour remettre le module en mode reception et de réinitialiser les stat
    - Ajout de la fonction setRx pour passer en mode reception
    - Ajout de la fonction setStandBy pour passer en mode standby
    - Ajout de la fonction getFreq pour récupérer la fréquence actuel du module
    - Ajout de la fonction getBandwidth pour récupérer la largeur de bande actuel du module
    - Ajout de la fonction setBandwidth pour modifier la largeur de bande du module
    - Ajout de la fonction getOutputPower pour récupérer la puissance d'émission actuel du module
    - Ajout de la fonction setCoderate pour modifier le coderate du module
    - Ajout de la fonction getCoderate pour récupérer le coderate actuel du module
    - Ajout de la fonction getRSSI pour récupérer la valeur RSSI de la dernière reception

    14.01.2024
    - Modification de la fonction run_recev pour supprimer l'identifiant du reseau
    - Ajout de la fonction getSNR pour récupérer la valeur SNR de la dernière reception
    - Ajout de la fonction setWebId pour modifier l'identifiant du reseau
    - Modufication de la focntion send pour ajouter l'identifiant du reseau

    22.01.2024
    - Finir modification de la récéption message pour gestion d'erreur
    

"""


from _sx126x import *
from sx126x import SX126X
import _sx126x
from module import cmd

_SX126X_PA_CONFIG_SX1262 = const(0x00)

class SX1262(SX126X):
    TX_DONE = SX126X_IRQ_TX_DONE
    RX_DONE = SX126X_IRQ_RX_DONE
    ADDR_FILT_OFF = SX126X_GFSK_ADDRESS_FILT_OFF
    ADDR_FILT_NODE = SX126X_GFSK_ADDRESS_FILT_NODE
    ADDR_FILT_NODE_BROAD = SX126X_GFSK_ADDRESS_FILT_NODE_BROADCAST
    PREAMBLE_DETECT_OFF = SX126X_GFSK_PREAMBLE_DETECT_OFF
    PREAMBLE_DETECT_8 = SX126X_GFSK_PREAMBLE_DETECT_8
    PREAMBLE_DETECT_16 = SX126X_GFSK_PREAMBLE_DETECT_16
    PREAMBLE_DETECT_24 = SX126X_GFSK_PREAMBLE_DETECT_24
    PREAMBLE_DETECT_32 = SX126X_GFSK_PREAMBLE_DETECT_32
    STATUS = ERROR

    #identifiant du reseau
    web_id = ""

    def __init__(self, spi_bus, clk, mosi, miso, cs, irq, rst, gpio):
        super().__init__(spi_bus, clk, mosi, miso, cs, irq, rst, gpio)
        self._callbackFunction = self._dummyFunction
        self.actuel_freq = 0
        self.power = 0
        self.coderate = 7

    def __del__(self):
        SX126X.__del__(self)

    def begin(self, freq=434.0, bw=125.0, sf=9, cr=7, syncWord=SX126X_SYNC_WORD_PRIVATE,
              power=14, currentLimit=60.0, preambleLength=8, implicit=False, implicitLen=0xFF,
              crcOn=True, txIq=False, rxIq=False, tcxoVoltage=1.6, useRegulatorLDO=False,
              blocking=True):
        state = super().begin(bw, sf, cr, syncWord, currentLimit, preambleLength, tcxoVoltage, useRegulatorLDO, txIq, rxIq)
        ASSERT(state)

        if not implicit:
            state = super().explicitHeader()
        else:
            state = super().implicitHeader(implicitLen)
        ASSERT(state)

        state = super().setCRC(crcOn)
        ASSERT(state)

        state = self.setFrequency(freq)
        ASSERT(state)

        state = self.setOutputPower(power)
        ASSERT(state)

        state = super().fixPaClamping()
        ASSERT(state)

        state = self.setBlockingCallback(blocking)

        return state

    def beginFSK(self, freq=434.0, br=48.0, freqDev=50.0, rxBw=156.2, power=14, currentLimit=60.0,
                 preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
                 addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
                 crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
                 fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
                 tcxoVoltage=1.6, useRegulatorLDO=False,
                 blocking=True):
        state = super().beginFSK(br, freqDev, rxBw, currentLimit, preambleLength, dataShaping, preambleDetectorLength, tcxoVoltage, useRegulatorLDO)
        ASSERT(state)

        state = super().setSyncBits(syncWord, syncBitsLength)
        ASSERT(state)

        if addrFilter == SX126X_GFSK_ADDRESS_FILT_OFF:
            state = super().disableAddressFiltering()
        elif addrFilter == SX126X_GFSK_ADDRESS_FILT_NODE:
            state = super().setNodeAddress(addr)
        elif addrFilter == SX126X_GFSK_ADDRESS_FILT_NODE_BROADCAST:
            state = super().setBroadcastAddress(addr)
        else:
            state = ERR_UNKNOWN
        ASSERT(state)

        state = super().setCRC(crcLength, crcInitial, crcPolynomial, crcInverted)
        ASSERT(state)

        state = super().setWhitening(whiteningOn, whiteningInitial)
        ASSERT(state)

        if fixedPacketLength:
            state = super().fixedPacketLengthMode(packetLength)
        else:
            state = super().variablePacketLengthMode(packetLength)
        ASSERT(state)

        state = self.setFrequency(freq)
        ASSERT(state)

        state = self.setOutputPower(power)
        ASSERT(state)

        state = super().fixPaClamping()
        ASSERT(state)

        state = self.setBlockingCallback(blocking)

        return state

    def setFrequency(self, freq, calibrate=True):
        if freq < 150.0 or freq > 960.0:
            return ERR_INVALID_FREQUENCY

        state = ERR_NONE

        self.actuel_freq = freq

        if calibrate:
            data = bytearray(2)
            if freq > 900.0:
                data[0] = SX126X_CAL_IMG_902_MHZ_1
                data[1] = SX126X_CAL_IMG_902_MHZ_2
            elif freq > 850.0:
                data[0] = SX126X_CAL_IMG_863_MHZ_1
                data[1] = SX126X_CAL_IMG_863_MHZ_2
            elif freq > 770.0:
                data[0] = SX126X_CAL_IMG_779_MHZ_1
                data[1] = SX126X_CAL_IMG_779_MHZ_2
            elif freq > 460.0:
                data[0] = SX126X_CAL_IMG_470_MHZ_1
                data[1] = SX126X_CAL_IMG_470_MHZ_2
            else:
                data[0] = SX126X_CAL_IMG_430_MHZ_1
                data[1] = SX126X_CAL_IMG_430_MHZ_2
            state = super().calibrateImage(data)
            ASSERT(state)

        return super().setFrequencyRaw(freq)

    def setOutputPower(self, power):
        if not ((power >= -9) and (power <= 22)):
            return ERR_INVALID_OUTPUT_POWER

        ocp = bytearray(1)
        ocp_mv = memoryview(ocp)
        state = super().readRegister(SX126X_REG_OCP_CONFIGURATION, ocp_mv, 1)
        ASSERT(state)

        state = super().setPaConfig(0x04, _SX126X_PA_CONFIG_SX1262)
        ASSERT(state)

        state = super().setTxParams(power)
        ASSERT(state)

        ret = super().writeRegister(SX126X_REG_OCP_CONFIGURATION, ocp, 1)

        self.power = power

        return ret

    def setTxIq(self, txIq):
        self._txIq = txIq

    def setRxIq(self, rxIq):
        self._rxIq = rxIq
        if not self.blocking:
            ASSERT(super().startReceive())

    def setPreambleDetectorLength(self, preambleDetectorLength):
        self._preambleDetectorLength = preambleDetectorLength
        if not self.blocking:
            ASSERT(super().startReceive())

    def setBlockingCallback(self, blocking, callback=None):
        self.blocking = blocking
        if not self.blocking:
            state = super().startReceive()
            ASSERT(state)
            if callback != None:
                self._callbackFunction = callback
                super().setDio1Action(self._onIRQ)
            else:
                self._callbackFunction = self._dummyFunction
                super().clearDio1Action()
            return state
        else:
            state = super().standby()
            ASSERT(state)
            self._callbackFunction = self._dummyFunction
            super().clearDio1Action()
            return state

    def recv(self, len=0, timeout_en=False, timeout_ms=0):
        if not self.blocking:
            return self._readData(len)
        else:
            return self._receive(len, timeout_en, timeout_ms)

    def send(self, data):
        if self.web_id != "":
            data = "web_id=" + self.web_id + " " + data

        data = b'' + data

        if not self.blocking:
            return self._startTransmit(data)
        else:
            return self._transmit(data)

    def _events(self):
        return super().getIrqStatus()

    def _receive(self, len_=0, timeout_en=False, timeout_ms=0):
        state = ERR_NONE
        
        length = len_
        
        if len_ == 0:
            length = SX126X_MAX_PACKET_LENGTH

        data = bytearray(length)
        data_mv = memoryview(data)

        try:
            state = super().receive(data_mv, length, timeout_en, timeout_ms)
        except AssertionError as e:
            state = list(ERROR.keys())[list(ERROR.values()).index(str(e))]

        if state == ERR_NONE or state == ERR_CRC_MISMATCH:
            if len_ == 0:
                length = super().getPacketLength(False)
                data = data[:length]

        else:
            return b'', state

        return  bytes(data), state

    def _transmit(self, data):
        if isinstance(data, bytes) or isinstance(data, bytearray):
            pass
        else:
            return 0, ERR_INVALID_PACKET_TYPE

        state = super().transmit(data, len(data))
        return len(data), state

    def _readData(self, len_=0):
        state = ERR_NONE

        length = super().getPacketLength()

        if len_ < length and len_ != 0:
            length = len_

        data = bytearray(length)
        data_mv = memoryview(data)

        try:
            state = super().readData(data_mv, length)
        except AssertionError as e:
            state = list(ERROR.keys())[list(ERROR.values()).index(str(e))]

        if state == ERR_NONE or state == ERR_CRC_MISMATCH:
            #decoupage du message
            try:
                msg = data.decode('utf-8')
            except Exception as err:
                print(err)
            return msg

        else:
            return b'', state

    def _startTransmit(self, data):
        if isinstance(data, bytes) or isinstance(data, bytearray):
            pass
        else:
            return 0, ERR_INVALID_PACKET_TYPE

        state = super().startTransmit(data, len(data))
        return len(data), state

    def _dummyFunction(self, *args):
        pass

    def _onIRQ(self, callback):
        events = self._events()
        if events & SX126X_IRQ_TX_DONE:
            super().startReceive()
        self._callbackFunction(events)

    #reception asychrone de message
    def run_recev(self):
        #variable boucle
        bcl = 0

        #boucle de gestion d'erreur de reception
        while bcl < 3:
        
            #initialisation de la variable message
            msg = ""
            stat = super().getStatus()
            if stat == _sx126x.STATUS['MESSAGE_EN_ATTENTE']:
                #changement de couleur text lors de récéption
                cmd.color_text(cmd.COLOR['yellow'])

                #récupération du message
                try:
                    msg = self._readData()
                    bcl = 3
                except Exception as err:
                    print("Erreur de reception " + str(err))

                #verification si sur le meme reseau
                if len(self.web_id) != 0:
                    compar = "web_id=" + self.web_id + " "
                    if compar in msg:
                        #supression de l'identifiant
                        msg = msg.replace(compar, "")
                    else:
                        #supression du message si mauvais  web_id
                        msg = ""
                        #passage text en blanc
                        cmd.color_text(cmd.COLOR['white'])

                #si pas de web_id et que le message en contien un
                elif "web_id=" in msg:
                    #supression du message
                    msg = ""
                    #passage text en blanc
                    cmd.color_text(cmd.COLOR['white'])
            bcl = bcl + 1
                    
        return msg            
            


    def reset_stat(self):
        #passage en standby
        super().standby()
        
        #pause de 10ms
        _sx126x.sleep_ms(10)

        #passage en RX
        self.setRx()

    #activer mode RX
    def setRx(self):
        super().setRx(0xFFFFFF)

    #passage en mode standby
    def setStandBy(self):
        super().standby()

    #récupération de fréquence
    def getFreq(self):
        return self.actuel_freq

    #récupération de la largeur de bande
    def getBandwidth(self):
        return super().getBandwidth()
    
    #modification de la largeur de bande
    def setBandwidth(self, bw):
        return super().setBandwidth(bw)
    
    #récupération de la puissance d'émission
    def getOutputPower(self):
        return self.power
    
    #régulage coding Rate
    def setCoderate(self, cr):
        super().setCodingRate(cr)
        self.coderate = cr
    
    #set de la web_id
    def setWebId(self, web_id):
        if len(web_id) > 0 and len(web_id) < 11:
            self.web_id = web_id
            return True
        else:
            return False, "web_id invalide"
        
    #get de la web_id
    def getWebId(self):
        return self.web_id
    
    #récupération du coding rate
    def getCoderate(self):
        return self.coderate
    
    #récupération de la valeur RSSI de la derrnière reception
    def getRSSI(self):
        return super().getRSSI()

    #recupération de la valeur SNR de la derrnière reception
    def getSNR(self):
        return super().getSNR()

    #A UTILISER POUR ESSAYER LA RECEPTION AVEC COULEUR
    def test(self):
        None