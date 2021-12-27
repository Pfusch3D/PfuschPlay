# PfuschPlay

Use Klipper with TFT screens which uses UART to communicate.

Das ganze Projekt wird vorerst auf Deutsch beschrieben:

Aktuell werden nur Anycubic TFTs unterstützt! Ich arbeite an einer allgemeinen Version, jedoch habe ich kein BTT/MKS TFT. Sollten die Preise davon sinken, dann werde ich mir eins bestellen 😅

Zur Installation:

Das ganze Projekt läuft auf node und wurde in Javascript geschrieben.
Bitte installiert euch zuerst git `sudo apt-get install git -y`
Danach nodeJS:
```
  sudo su
  curl -fsSL https://deb.nodesource.com/setup_17.x | bash -
  apt-get install -y nodejs
  su pi # oder euren Benutzernamen
```
  
nachdem ihr nodejs inkl. npm und git installiert habt könnt ihr im Hauptverzeichnis `cd ~` das Github Projekt klonen. Gebt dazu `git clone https://github.com/BastelKlug/PfuschPlay` in die Konsole ein. Danach ein `cd PfuschPlay` und darauffolgend `npm install`.

In der config.json findet man 3 verschiedene Einstellmöglichkeiten. Die Websocket URL lässt ihr bitte unberührt, Baudrate und Port sind auf die GPIO Ports eingestellt. Für PfuschPlay muss eine Verbindung zwischen Display und Raspberry pi stattfinden. Bearbeiten könnt ihr die Datei mit nano, welcher auf eurem Pi vorinstalliert ist. Einfach `sudo nano config.json` eingeben.
```
  DISPLAY --> Raspberry Pi 
  
  Grün --> Pin 4 (5V)
  Blau (RX) --> Pin 8 (TX)  // Das vertauschen der RX und TX Pins ist kein Fehler. T steht für Transmitter und R für Receive.
  Grau (TX) --> Pin 10 (RX) // Was gesendet wird muss irgendwo auch empfangen werden.
  Gelb --> Pin 6 (GND)
```
Bitte beachtet, dass der Pi standardmäßig die UART Pins nicht aktiviert hat. Ab MainsailOS 0.5.0 (also alle Drucker die nach dem 28. August mit MainsailOS installiert wurden) ist UART standardmäßig aktiviert. Da beim Pi 3 Bluetooth deakvitiert werden muss usw. würde ich einfach eine Neuinstallation empfehlen. Aber Achtung: printer.cfg sichern ;) Ebenso könnt ihr einen TTL Adapter verweden und das Display per USB verbinden. `ls /dev/serial/by-id/*` eingeben um die id vom TTL Adapter zu finden. Diese ID dann in die config.json eintragen.

Aktuell ist es noch nicht möglich PfuschPlay automatisch zu starten. Deshalb experimentell im PfuschPlay Ordner `node .` oder `node index.js` ausführen. 

Ich arbeite an einem systemd Service dafür 😅

(Das ganze funktioniert aktuell nicht, da euch die Macros fehlen. Lade ich die Tage mal hoch 😅)
