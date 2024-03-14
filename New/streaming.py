import subprocess

# Variable globale pour stocker le processus de streaming
stream_process = None

# Fonction pour démarrer le streaming
def start_stream(audio_device):
    global stream_process
    stream_process = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-input_format', 'yuyv422', '-i', '/dev/video0', '-f', 'alsa', '-i', audio_device, '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency', '-s', '1280x720', '-c:a', 'aac', '-ac', '2', '-f', 'flv', 'rtmp://ip.de.voter.serveur/live/cledestream'])

# Fonction pour arrêter le streaming
def stop_stream():
    global stream_process
    if stream_process is not None:
        stream_process.terminate()
        stream_process = None
# Statut du stream
def get_stream_status():
    global stream_process
    if stream_process and stream_process.poll() is None:
        return "stream-active"
    else:
        return "stream-inactive"
