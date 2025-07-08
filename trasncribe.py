import whisper
import sounddevice as sd
import numpy as np
import queue
import threading
from googletrans import Translator
from PyQt5 import QtWidgets, QtCore
import sys
from scipy.io.wavfile import write as write_wav

# Cola para audio capturado
audio_q = queue.Queue()

# Parámetros audio
samplerate = 16000
blocksize = 4000
channels = 1
translator = Translator()

# Cargar modelo Whisper
model = whisper.load_model("base")

# Ventana flotante subtítulos
class SubtitleOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel("", self)
        self.label.setStyleSheet("color: white; font-size: 24px; background-color: rgba(0, 0, 0, 150); padding: 10px; border-radius: 8px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(800, 80)
        self.move(560, 800)  # Cambia posición inicial si quieres

    def update_text(self, text):
        self.label.setText(text)
        self.label.adjustSize()

# Callback captura audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_q.put(indata.copy())

# Procesar audio, transcribir y traducir
def process_audio(window):
    buffer = np.empty((0, 1), dtype=np.float32)
    while True:
        data = audio_q.get()
        buffer = np.concatenate((buffer, data))

        if len(buffer) >= samplerate * 5:  # cada 5 segundos
            audio_chunk = buffer[:samplerate * 5]
            buffer = buffer[samplerate * 5:]

            # Guardar audio a wav (int16)
            audio_int16 = np.int16(audio_chunk * 32767)
            audio_path = "temp.wav"
            write_wav(audio_path, samplerate, audio_int16)

            # Transcribir con Whisper
            result = model.transcribe(audio_path)
            text = result["text"]

            # Traducir al español
            translated = translator.translate(text, dest='es').text

            print("▶", translated)
            window.update_text(translated)

# Ejecutar app PyQt + captura de audio
def start_app():
    app = QtWidgets.QApplication(sys.argv)
    window = SubtitleOverlay()
    window.show()

    # Hilo para procesar audio
    threading.Thread(target=process_audio, args=(window,), daemon=True).start()

    # Captura audio del sistema (VB-Cable como dispositivo de entrada)
    with sd.InputStream(samplerate=samplerate, channels=channels, blocksize=blocksize, callback=audio_callback):
        sys.exit(app.exec_())

if __name__ == "__main__":
    start_app()
