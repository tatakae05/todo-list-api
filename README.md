Die VM wurde im Bridge-Modus betrieben, damit sie im selben Subnetz wie der Router hängt und von außen erreichbar ist.

Um eine statische IP-Adresse zu setzen, muss der Befehl `sudo nano /etc/netplan/00-installer-config.yaml` eingegeben werden, um die Datei bearbeiten zu können. Danach muss die IP-Adresse angepasst werden, bei mir sieht es so aus:

```yaml
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
```

Anschließend wird `sudo netplan apply` angewendet, damit die Einstellungen übernommen werden. Wenn alles passt, kann man es mit Pings testen:

```bash
ping 192.168.24.254
```

> Als DNS-Server wurde die gleiche Adresse wie das Gateway verwendet, da externe DNS-Server wie 8.8.8.8 im genutzten Netz durch eine Firewall nicht erreichbar waren.

Um Benutzer anzulegen, benutzt man den Befehl `sudo adduser willi` für einen normalen Benutzer. Bei einem mit SSH-Zugriff kann man die Kombination

```bash
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff
```

benutzen. Geprüft wird es mit dem Befehl `groups fernzugriff`, ob er sudo-Rechte hat. Bei allen Benutzern einfach mit Enter bestätigen.

Da OpenSSH bei mir nicht installiert war, wurde es mit

```bash
sudo apt update
sudo apt install -y openssh-server
```

installiert. Bei allen Abfragen einfach mit Enter bestätigen.

Die SSH-Datei muss angepasst werden:

```bash
sudo nano /etc/ssh/sshd_config
```

Es müssen `PermitRootLogin` und `PasswordAuthentication` gefunden und angepasst werden auf:

```
PermitRootLogin no
PasswordAuthentication yes
```

Zudem muss noch

```
AllowUsers fernzugriff
```

hinzugefügt werden. Für den Autostart des SSH-Dienstes werden die Befehle

```bash
sudo systemctl restart ssh
sudo systemctl enable ssh
```

benutzt. Anschließend sollte von einer anderen Konsole über SSH darauf zugegriffen werden können.

Docker wird mit den Befehlen

```bash
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
```

installiert. Danach kann er mit den Befehlen

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

automatisch starten. Anschließend kann der aktuelle Benutzer noch zur Docker-Gruppe hinzugefügt werden durch

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Da mein Python-Code nicht auf der VM war, habe ich zuerst Git installiert mit

```bash
sudo apt install -y git
```

Anschließend wurde das Git-Repository geklont mit

```bash
git clone https://github.com/tatakae05/todo-list-api.git
```

um danach mit `cd todo-list-api/` auf das Repository zu wechseln.

Der nächste Schritt war, die Dockerfile zu erstellen mit:

```bash
nano Dockerfile
```

Die Datei wurde mit folgendem Inhalt gefüllt:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install flask
COPY beispiel-server.py .
COPY templates ./templates
EXPOSE 5000
CMD ["python", "beispiel-server.py"]
```

Anschließend kann das Docker-Image mit

```bash
docker build -t todo-api .
```

gebaut und mit

```bash
docker run -d -p 5000:5000 --restart always --name todo-api todo-api
```

zum Laufen gebracht werden. Die Option `--restart always` stellt sicher, dass der Container nach einem Neustart der VM automatisch wieder gestartet wird, sodass alle Einstellungen erhalten bleiben.

Geprüft werden kann der laufende Container mit:

```bash
docker ps
```

Die App ist anschließend erreichbar unter `http://192.168.24.200:5000`.
