
import threading
from utils.logger import get_logger
from config.settings import settings
from services.audio_capture import record_until_silence
from services.asr_whisper import transcribe
from services.llm_openai import generate_reply
from services.tts_pyttsx3 import speak_async

log = get_logger(__name__)

class Controller:
    def __init__(self, ui_callbacks):
        self.ui = ui_callbacks
        self._busy = False
        self._thread = None

    def start_pipeline(self):
        if self._busy: return
        self._busy = True
        self.ui["set_button_state"](False)
        self.ui["set_status"]("Écoute… (parle maintenant)")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        try:
            wav_path = record_until_silence(
                sample_rate=settings.SAMPLE_RATE,
                frame_ms=settings.FRAME_MS,
                max_seconds=settings.MAX_RECORD_SECONDS,
                vad_backend=settings.VAD_BACKEND,
                energy_threshold_db=settings.ENERGY_THRESHOLD_DB,
                silence_tail_ms=settings.SILENCE_TAIL_MS,
            )
            self.ui["set_status"]("Transcription…")
            text = transcribe(wav_path, settings.ASR_MODEL)
            self.ui["set_transcript"](text or "")

            self.ui["set_status"]("Raisonnement…")
            reply = generate_reply(text, provider=settings.LLM_PROVIDER)
            self.ui["set_reply"](reply or "")

            self.ui["set_status"]("Parole…")
            speak_async(reply or "")
            self.ui["set_status"]("Prêt")
        except Exception as e:
            log.exception("Pipeline error: %s", e)
            self.ui["set_status"](f"Erreur: {e}")
        finally:
            self._busy = False
            self.ui["set_button_state"](True)
