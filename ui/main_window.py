
import tkinter as tk
from tkinter import ttk
from app.controller import Controller

def run_app():
    root = tk.Tk()
    root.title("Assistante vocale — Python + Tkinter (no-build)")
    root.geometry("560x520")

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except:
        pass

    frame = ttk.Frame(root, padding=12)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="Assistante vocale (Tkinter)", font=("Segoe UI", 14, "bold"))
    title.pack(anchor="w", pady=(0,8))

    status_var = tk.StringVar(value="Prêt")
    status_lbl = ttk.Label(frame, textvariable=status_var, foreground="#2563eb")
    status_lbl.pack(anchor="w", pady=(0,12))

    btn = ttk.Button(frame, text="🎤 Parler")
    btn.pack(anchor="w")

    ttk.Separator(frame).pack(fill="x", pady=12)

    ttk.Label(frame, text="Transcript").pack(anchor="w")
    txt_transcript = tk.Text(frame, height=8, wrap="word")
    txt_transcript.pack(fill="both", expand=True, pady=(0,8))

    ttk.Label(frame, text="Réponse").pack(anchor="w")
    txt_reply = tk.Text(frame, height=8, wrap="word")
    txt_reply.pack(fill="both", expand=True)

    def set_status(s: str): status_var.set(s)
    def set_transcript(t: str):
        txt_transcript.delete("1.0","end"); txt_transcript.insert("1.0", t)
    def set_reply(t: str):
        txt_reply.delete("1.0","end"); txt_reply.insert("1.0", t)
    def set_button_state(enabled: bool): btn.config(state=("normal" if enabled else "disabled"))

    controller = Controller({
        "set_status": set_status,
        "set_transcript": set_transcript,
        "set_reply": set_reply,
        "set_button_state": set_button_state
    })

    btn.config(command=controller.start_pipeline)
    root.bind("<Control-space>", lambda e: controller.start_pipeline())
    root.mainloop()
