
import threading
import pyttsx3
from config.settings import settings

_engine = None
def _get_engine():
    global _engine
    if _engine: return _engine
    eng = pyttsx3.init()
    if settings.TTS_RATE:
        eng.setProperty("rate", int(settings.TTS_RATE))
    vpref = (settings.TTS_VOICE or "").strip().lower()
    if vpref:
        for v in eng.getProperty("voices") or []:
            if vpref in (v.name or "").lower():
                eng.setProperty("voice", v.id)
                break
    _engine = eng
    return _engine

def speak(text: str):
    if not text: return
    eng = _get_engine()
    eng.say(text)
    eng.runAndWait()

def speak_async(text: str):
    import threading
    th = threading.Thread(target=speak, args=(text,), daemon=True)
    th.start()
    return th
