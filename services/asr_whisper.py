
from faster_whisper import WhisperModel

_model_cache = {}

def _get_model(name: str):
    if name not in _model_cache:
        device = "cpu"
        compute_type = "int8"
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                compute_type = "float16"
        except Exception:
            pass
        _model_cache[name] = WhisperModel(name, device=device, compute_type=compute_type)
    return _model_cache[name]

def transcribe(audio_path: str, model_name: str = "small") -> str:
    model = _get_model(model_name)
    segments, info = model.transcribe(audio_path, beam_size=1, vad_filter=True)
    text = "".join(seg.text for seg in segments).strip()
    return text
