#!/bin/bash

# Démarrer le serveur Flask
python3 /home/pi/Desktop/app.py &

# Attendre quelques secondes pour que le serveur démarre complètement
sleep 5

# Ouvrir Chromium et accéder à localhost:5000
chromium-browser --incognito --noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars http://localhost:5000


