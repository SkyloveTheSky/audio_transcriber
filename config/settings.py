
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "stub")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    ASR_MODEL = os.getenv("ASR_MODEL", "small")

    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
    FRAME_MS = int(os.getenv("FRAME_MS", "30"))
    MAX_RECORD_SECONDS = int(os.getenv("MAX_RECORD_SECONDS", "8"))

    VAD_BACKEND = os.getenv("VAD_BACKEND", "auto")
    ENERGY_THRESHOLD_DB = float(os.getenv("ENERGY_THRESHOLD_DB", "-40"))
    SILENCE_TAIL_MS = int(os.getenv("SILENCE_TAIL_MS", "800"))

    TTS_VOICE = os.getenv("TTS_VOICE", "")
    TTS_RATE = int(os.getenv("TTS_RATE", "180"))

settings = Settings()
