# PfuschPlay

Use Klipper with TFT screens which uses UART to communicate.

Das ganze Projekt wird vorerst auf Deutsch beschrieben:

Aktuell werden nur Anycubic TFTs unterstützt! Ich arbeite an einer allgemeinen Version, jedoch habe ich kein BTT/MKS TFT zur Verfügung. Sollten die Preise davon sinken, dann werde ich mir eins dafür bestellen 😅

Zur Installation:

Das ganze Projekt läuft auf node und wurde in Javascript geschrieben.
Bitte installiert euch zuerst git ( sudo apt-get install git -y ) 
Dnach nodeJS:

  sudo su
  curl -fsSL https://deb.nodesource.com/setup_17.x | bash -
  apt-get install -y nodejs
  
nachdem ihr nodejs inkl. npm und git installiert habt könnt ihr im Hauptverzeichnis das Github Projekt klonen. Gebt dazu git clone https://github.com/BastelKlug/PfuschPlay in die Konsole ein. danach cd PfuschPlay und darauffolgend npm install.

In der config.json findet man 3 verschiedene Einstellmöglichkeiten. Die Websocket URL lässt ihr bitte unberührt, Baudrate und Port sind auf die GPIO Ports eingestellt. Für PfuschPlay muss eine Verbindung zwischen Display und Raspberry pi stattfinden. 
  
  DISPLAY --> Raspberry Pi
  

