
from config.settings import settings

_client = None
def _get_openai_client():
    global _client
    try:
        if _client: return _client
        from openai import OpenAI
        if not settings.OPENAI_API_KEY:
            return None
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return _client
    except Exception:
        return None

def _stub_reply(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return "Je n'ai pas bien entendu. Peux-tu répéter ?"
    if any(x in t.lower() for x in ["bonjour","salut","coucou"]):
        return "Bonjour ! Comment puis-je t'aider aujourd'hui ?"
    if t.endswith("?"):
        return "Bonne question. Pour affiner, peux-tu préciser ta demande ?"
    return "D'accord. " + t

def generate_reply(prompt: str, provider: str = "stub") -> str:
    provider = (provider or "stub").lower()
    if provider != "openai":
        return _stub_reply(prompt)

    client = _get_openai_client()
    if not client:
        return _stub_reply(prompt)

    model = settings.OPENAI_MODEL or "gpt-4o-mini"
    sys = "Tu es une assistante vocale concise et polie. Réponds en français si possible."
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role":"system","content":sys},
                {"role":"user","content": prompt or ""}
            ],
            temperature=0.5
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return _stub_reply(prompt)
