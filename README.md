English

I will post on branches so that you have access to all versions.

Update V1.01 of January 22, 2024:

- Change in the layout of the entry message
- Modification of the backup sequence following the deletion of the file that caused issues in the previous version
- Handling of a sporadically occurring reception error in the SX1262 object
- Multiple transmission tests; the current maximum range is approximately 300 meters

Added commands:

```
/snr displays the SNR of the last reception
/webid to change the webid
```

Command /webid:

Allows the separation of your transmissions with a network name of a maximum of 10 characters.

The future of the project involves changing the casing, with the provision of STL files and some useful information about the transmission system.

There is also a plan to test an amplifier to improve the range.

Photos of the object itself will be taken, which may prove useful for reproduction.

The system will also be tested with a frequency analyzer to verify the accuracy of the data visible on the screen.

I want to remind you that depending on the country, you may not have the right to transmit on certain frequencies. I am not responsible for any infractions you may commit with this program.


Francais

Je vais poster sur des branches pour que vous ayez accès à toutes les versions.

Mise à jour V1.01 du 22.01.2024 :

- Changement de la mise en page du message d'entrée
- Modification de la séquence de sauvegarde suite à la suppression du fichier qui causait des problèmes sur l'ancienne version
- Gestion d'une erreur de réception survenant de manière sporadique dans l'objet SX1262
- Tests multiples de transmission, la portée maximale est actuellement d'environ 300 mètres

Ajout de commandes :

```
/snr affiche le SNR de la dernière réception
/webid pour changer la webid
```

Commande /webid :

Permet la séparation de vos transmissions avec un nom de réseau d'un maximum de 10 caractères.

Le futur du projet implique un changement de boîtier, avec la fourniture des fichiers STL et quelques informations utiles sur le système de transmission.

Il est également prévu de tester un amplificateur pour améliorer la portée.

Des photos de l'objet seront prises, pouvant s'avérer utiles pour la reproduction.

Le système sera également testé avec un analyseur de fréquence afin de vérifier l'exactitude des données visibles sur l'écran.

Je tiens à vous rappeler qu'en fonction des pays, vous pourriez ne pas avoir le droit de transmettre sur certaines fréquences. Je ne suis pas responsable des infractions que vous pourriez commettre avec ce programme.

______________________________________________________________________________________________________

# Lilygo-T-deck-LORA
English

LORA point-to-point cat for the Lilygo T-deck

Communication based on LORA transmission with the SX1262 chip integrated into certain devices.

Feel free to create tickets in case of any issues.

Thanks to Robert Grizzell for his codes that helped me develop this module.
https://github.com/rgrizzell

Commands:

            /exit to exit
            /pseudo to change nickname
            /help to display help
            /freq to change frequency
            /bandw to change bandwidth
            /power to change transmission power
            /coder to change coding level
            /rssi to enable/disable RSSI display
            /save to save parameters

Frequency command:

            /freq [frequency]
            [frequency] = frequency in MHz
            Available frequencies:
            Between 150MHz and 960MHz

Bandwidth command:

            /bandw [bandwidth]
            [bandwidth] = width in kHz
            Available bandwidths:
              7.8, 10.4, 15.6, 20.8, 31.25,
              41.7, 62.5, 125, 250, 500

Transmission power command:

            /power [power]
            [power] = power in dBm
            Available power levels:
            Between -9 and 22

Coding level command:

            /coder [level]
            [level] = coding level
            Available levels:
            5, 6, 7, 8
            The higher the coding level, the
            lower the transfer rate, but the
            reliability of the transfer is better

RSSI command:

            /rssi [state]
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

Commandes: 

            /exit pour quitter
            /pseudo pour changer de pseudo
            /help pour afficher l'aide
            /freq pour changer de fréquence
            /bandw pour changer largeur de bande
            /power pour changer la puissance envoie
            /coder pour changer le niveau de coding
            /rssi pour activer/desactiver le rssi
            /save pour sauvgarder les parametre

Commande fréquence:

            /freq [fréquence]
            [fréquence] = fréquence en MHz
            Fréquence disponible:
            Entre 150Mhz et 960Mhz

Commande largeur de bande:

            /bandw [largeur de bande]
            [largeur de bande] = largeur en kHz
            Largeur de bande disponible:
              7.8, 10.4, 15.6, 20.8, 31.25,
              41.7, 62.5, 125, 250, 500

Commande puissance d'envoie:

            /power [puissance]
            [puissance] = puissance en dBm
            Puissance disponible:
            Entre -9 et 22

Commande niveau de coding:

            /coder [niveau]
            [niveau] = niveau de coding
            Niveau disponible:
            5, 6, 7, 8
            Plus le coding est elevé plus
            le taux de transfert est faible
            mais la fiabilité du transfère
            est meilleur

Commande rssi:

            /rssi [etat]
            [etat] = etat de l'affichage
            Etat disponible:
            on, off
            Affiche le rssi de la derniere reception
            devant le message en dBm

