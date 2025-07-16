# 🎙️ Real-Time Subtitles Translator with Whisper + PyQt + Google Translate

Este proyecto permite **transcribir y traducir en tiempo real** el audio capturado desde el sistema (como videos de YouTube, reuniones o películas) usando el modelo **Whisper** de OpenAI. Los subtítulos traducidos se muestran en una **ventana flotante superpuesta** sobre la pantalla, ideal para seguir contenido en otros idiomas de forma accesible.

## 🚀 Características

- 🎧 Captura de audio en tiempo real desde el sistema (usa VB-Cable u otro dispositivo virtual)
- 🧠 Transcripción precisa con [Whisper](https://github.com/openai/whisper)
- 🌍 Traducción automática al español con `googletrans`
- 🪟 Ventana flotante translúcida sobre cualquier aplicación (PyQt5)
- 🔄 Actualización dinámica de subtítulos cada 5 segundos

---

## 📦 Requisitos

- Python >= 3.8
- pip
- Dispositivo de captura de audio (ej. **VB-Cable** en Windows)
- GPU (opcional, pero recomendable para rendimiento de Whisper)

### 📚 Dependencias

```bash
pip install openai-whisper sounddevice numpy scipy googletrans==4.0.0-rc1 PyQt5
