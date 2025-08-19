# Assistante vocale
Cette variante supprime la dépendance stricte à `webrtcvad` (qui exige MSVC).
Un VAD **énergie** pur Python est intégré. Si `webrtcvad` est présent, il sera utilisé automatiquement.

Installez avec `pip install -r requirements.txt` puis `python main.py`.
Voir `.env.example` pour la config.
