Um eine Statische Ip-Adresse zu setzen nach den aufsetzen der VM muss der befehl:
sudo nano /etc/netplan/00-installer-config.yaml eingegeben werden, um die Datei bearbeiten zu können.
Danach muss die IP-Adresse angepasst werden bei mir sieht es so aus: 
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.24.200/24
      routes:
        - to: default
          via: 192.168.24.254
      nameservers:
        addresses:
          - 192.168.24.254

Anschließend wird sudo netplan apply angewendet damit die einstellungen übernommen werden. 
Wenn alles past kann man es mit pings testen.
Die VM muss außerden in den Bridge modus gesetzt werden.

Um Benutzer anzulegen benutzt mann den Befehl:
sudo adduser willi für einen normalen User.
Bei einen mit ssh zugriff kann man die Kombination:
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff 
benutzen. 

Geprüft wird es mit den befehl:
groups fernzugriff 
ob er ssh zugriff hat.

Bei allen benutzern einfach mit Enter bestätigen

Da Openssh bei mir nicht installiert war wurde es mit 
sudo apt update
sudo apt install -y openssh-server
installiert

Bei allen sachen einfach mit enter bestätigen

Die ssh Datei muss angepasst 
sudo nano /etc/ssh/sshd_config

Es müssen: 
PermitRootLogin 
PasswordAuthentication gefunden und angepasst werden auf:
PermitRootLogin no
PasswordAuthentication yes
Zudem muss noch 
#AllowUsers fernzugriff
hinzugefügt werden
Für den Autostart des SSH dienst werden die befehle:
sudo systemctl restart ssh
sudo systemctl enable ssh
benutzt. 
Anschließend sollte auf einer anderen Console über ssh drauf zugegriffen werden können.

Docker wird mit den Befehlen: 
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
installiert. 

Danach kann er autostarten mit den Befehlen:
sudo systemctl enable docker
sudo systemctl start docker

Anschließend kann man docker noch zu einer Gruppe hinzufügen durch:
sudo usermod -aG docker $USER
newgrp docker

Da mein Python code nicht auf der VM war habe ich erst git installiert mit:
sudo apt install -y git
Anschließend wurde das git repo geklont mit
git clone https://github.com/tatakae05/todo-list-api.git
um danach mit:
cd todo-list-api/
auf das repo zu wechseln

Der nächste schritt war die Dockerfile zu erstellen mit: 
nano Dockerfile 
wurde die Datei ertsellt und der Inhalt mit:
FROM python:3.12-slim

WORKDIR /app

Run pip install flask

COPY beispiel-server.py .
COPY templates ./templates

EXPOSE 5000

CMD ["python", "beispiel-server.py"]

gefüllt.
Anschließend kann docker mit:
docker build -t todo-api . 
gebaut und mit:
docker run -d -p 5000:5000 --name todo-api todo-api
zum laufen gebracht. 

Die Docker wurde danach nochmal gepusht und dass waren dann alle einstellungen.
