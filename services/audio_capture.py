
import sounddevice as sd
import numpy as np
import queue, time, wave, os, tempfile
from typing import Optional

def rms_dbfs(x: np.ndarray, eps=1e-9) -> float:
    """RMS en dBFS pour un signal int16 normalisé [-1,1]."""
    if x.size == 0: return -120.0
    m = np.sqrt(np.mean(np.square(x.astype(np.float32))))
    db = 20.0 * np.log10(max(m, eps))
    return max(-120.0, min(0.0, db))

def record_until_silence(sample_rate=16000, frame_ms=30,
                         max_seconds=8, vad_backend="auto",
                         energy_threshold_db=-40.0, silence_tail_ms=800):
    """
    Enregistre via le micro jusqu'à détecter un silence prolongé après la parole.
    - vad_backend: 'auto' | 'energy' | 'webrtc'
    - energy_threshold_db: seuil d'énergie (dBFS) pour considérer "parole"
    """
    blocksize = int(sample_rate * (frame_ms/1000.0))
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        q.put(indata.copy())

    # Backends
    use_webrtc = False
    if vad_backend in ("auto","webrtc"):
        try:
            import webrtcvad  # type: ignore
            vad = webrtcvad.Vad(2)  # agressivité moyenne
            use_webrtc = True
        except Exception:
            use_webrtc = False

    collected = []
    started = False
    silence_ms = 0
    start_time = time.time()

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16',
                        blocksize=blocksize, callback=callback):
        while True:
            try:
                bf = q.get(timeout=0.5)
            except queue.Empty:
                continue

            if use_webrtc:
                pcm = bf.flatten().tobytes()
                is_speech = vad.is_speech(pcm, sample_rate)
            else:
                # Energy-based VAD (pure Python)
                x = bf.astype(np.float32) / 32768.0
                level = rms_dbfs(x)
                is_speech = (level > float(energy_threshold_db))

            if is_speech:
                started = True
                silence_ms = 0
                collected.append(bf.copy())
            else:
                if not started:
                    # encore silence avant la première parole → continue
                    pass
                else:
                    silence_ms += frame_ms
                    collected.append(bf.copy())
                    if silence_ms >= silence_tail_ms:
                        break

            if (time.time() - start_time) >= max_seconds:
                break

    if not collected:
        collected = [np.zeros((blocksize,1), dtype=np.int16)]

    audio = np.concatenate(collected, axis=0).astype(np.int16)
    out_path = os.path.join(tempfile.gettempdir(), "assistant_input.wav")
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return out_path
