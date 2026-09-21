import tkinter as tk
from observers.observers import Observateur

class PrixDysplay(Observateur):
    def __init__(self, fenetre):
        self.fenetre = fenetre_parent
        self.frame_prix = tk.LabelFrame(self.fenetre, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        self.prix_label = tk.Label(self.frame_prix, text="Prix actuel : ")
        self.prix_label.pack()

        