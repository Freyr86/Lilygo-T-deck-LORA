# Lilygo-T-deck-LORA
English

LORA point-to-point cat for the Lilygo T-deck

Communication based on LORA transmission with the SX1262 chip integrated into certain devices.

Feel free to create tickets in case of any issues.

Thanks to Robert Grizzell for his codes that helped me develop this module.
https://github.com/rgrizzell

Commands:  /exit to exit
            /pseudo to change nickname
            /help to display help
            /freq to change frequency
            /bandw to change bandwidth
            /power to change transmission power
            /coder to change coding level
            /rssi to enable/disable RSSI display
            /save to save parameters

Frequency command: /freq [frequency]
            [frequency] = frequency in MHz
            Available frequencies:
            Between 150MHz and 960MHz

Bandwidth command: /bandw [bandwidth]
            [bandwidth] = width in kHz
            Available bandwidths:
              7.8, 10.4, 15.6, 20.8, 31.25,
              41.7, 62.5, 125, 250, 500

Transmission power command: /power [power]
            [power] = power in dBm
            Available power levels:
            Between -9 and 22

Coding level command: /coder [level]
            [level] = coding level
            Available levels:
            5, 6, 7, 8
            The higher the coding level, the
            lower the transfer rate, but the
            reliability of the transfer is better

RSSI command: /rssi [state]
            [state] = display state
            Available states:
            on, off
            Displays the RSSI of the last reception
            in front of the message in dBm

Français

Chat baser sur la transmission LORA avec la puce SX1262 intégrée dans certains de ces appareils.

N'hésitez pas à faire des tickets en cas de bug.

Merci à Robert Grizzell pour ces codes qui m'ont aidé à réaliser ce module.
https://github.com/rgrizzell

Commandes:  /exit pour quitter
            /pseudo pour changer de pseudo
            /help pour afficher l'aide
            /freq pour changer de fréquence
            /bandw pour changer largeur de bande
            /power pour changer la puissance envoie
            /coder pour changer le niveau de coding
            /rssi pour activer/desactiver le rssi
            /save pour sauvgarder les parametre

Commande fréquence: /freq [fréquence]
            [fréquence] = fréquence en MHz
            Fréquence disponible:
            Entre 150Mhz et 960Mhz

Commande largeur de bande: /bandw [largeur de bande]
            [largeur de bande] = largeur en kHz
            Largeur de bande disponible:
              7.8, 10.4, 15.6, 20.8, 31.25,
              41.7, 62.5, 125, 250, 500

Commande puissance d'envoie: /power [puissance]
            [puissance] = puissance en dBm
            Puissance disponible:
            Entre -9 et 22

Commande niveau de coding: /coder [niveau]
            [niveau] = niveau de coding
            Niveau disponible:
            5, 6, 7, 8
            Plus le coding est elevé plus
            le taux de transfert est faible
            mais la fiabilité du transfère
            est meilleur

Commande rssi: /rssi [etat]
            [etat] = etat de l'affichage
            Etat disponible:
            on, off
            Affiche le rssi de la derniere reception
            devant le message en dBm

