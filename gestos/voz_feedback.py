import pyttsx3
import threading
from config import VOICE_RATE, VOICE_VOLUME, LANGUAGE

class VozFeedback:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)
        
        # Tentar carregar voz em português
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def anunciar(self, texto):
        """Fala o texto em thread separada"""
        def falar():
            try:
                self.engine.say(texto)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Erro ao falar: {e}")
        
        thread = threading.Thread(target=falar)
        thread.daemon = True
        thread.start()
    
    def parar(self):
        self.engine.stop()

# Criar arquivo vazio __init__.py em gestos/
# gestos/__init__.py
