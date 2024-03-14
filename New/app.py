import socket
import logging
from flask import Flask, render_template, request, redirect, url_for
from streaming import start_stream, stop_stream
import psutil

app = Flask(__name__)

# Configurez le logging pour enregistrer les messages reçus
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

# Paramètres de connexion à Twitch IRC
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'nickname'
token = 'oauth:xxxxxxxxxxx'
channel = '#channel'

# Connectez-vous à Twitch IRC
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Fonction pour envoyer un message vers le chat IRC
def send_message(message):
    sock.send(f"PRIVMSG {channel} :{message}\n".encode('utf-8'))

# Route pour afficher la page avec les boutons
@app.route('/')
def index():
    return render_template('index.html')

# Route pour démarrer le flux
@app.route('/start_stream', methods=['GET', 'POST'])
def start_stream_route():
    audio_device = request.args.get('audioDevice', 'hw:2,0')  # Par défaut, utilisez la carte son 1
    start_stream(audio_device)
    # Rediriger vers la page d'index après avoir démarré le flux
    return redirect(url_for('index'))

# Route pour arrêter le flux
@app.route('/stop_stream', methods=['GET', 'POST'])
def stop_stream_route():
    stop_stream()
    # Rediriger vers la page d'index après avoir arrêté le flux
    return redirect(url_for('index'))

# Fonction pour obtenir le statut du flux
def get_stream_status():
    # Vérifie si le processus ffmpeg est en cours d'exécution
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'ffmpeg':
            # Vérifie si le processus ffmpeg a été lancé avec la bonne commande
            if 'ffmpeg' in proc.info['cmdline']:
                return "active"  # Le flux est actif
    return "inactive"  # Le flux n'est pas actif

# Route pour afficher la page du statut du flux
@app.route('/stream_status')
def stream_status_page():
    # Obtenez le statut du flux
    stream_status = get_stream_status()
    
    # Définir la classe CSS en fonction du statut du flux
    if stream_status == "active":
        stream_status_class = "stream-active"
    else:
        stream_status_class = "stream-inactive"

    return render_template('stream_status.html', stream_status=stream_status, stream_status_class=stream_status_class)

# Route pour afficher la page de commandes Twitch
@app.route('/commands')
def twitch_commands():
    return render_template('commands.html')

# Route pour envoyer les commandes depuis les boutons
@app.route('/send_command/<command>')
def send_command(command):
    if command == 'start':
        send_message("!start")
    elif command == 'stop':
        send_message("!stop")
    elif command == 'privacy':
        send_message("!privacy")
    elif command == 'live':
        send_message("!live")
    return redirect(url_for('twitch_commands'))


if __name__ == '__main__':
    app.run(debug=True)
