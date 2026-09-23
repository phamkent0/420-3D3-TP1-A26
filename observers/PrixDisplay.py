import tkinter as tk
from observers.observers import Observateur

class PrixDysplay(Observateur):
    def __init__(self, fenetre_parent : tk.Tk):

        self.fenetre = fenetre_parent
        self.frame_prix = tk.LabelFrame(self.fenetre, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        self.labels_prix = {}
        self.frame_lignes = 0

        def actualiser(self,sujet)->None:
            donnees = sujet.get_donnees()
            prix_actuels = donnees.get("prix_actuels",{})

#sup
            for ticker in list(self.frames_lignes.keys())
                if ticker not in prix_actuels
                    self.frames[ticker].destroy()
                    del self.frames_lignes[ticker]
                    del self.lables_prix[ticker]
#MAJ et creation des ligne 
            for ticker, (prix, ouverture) in prix_actuels.items:
                if ticker not in self.labels_prix:
                    frame = tk.Frame(self.frame_prix)
                frame.pack(fill=tk.X, pady=2)
                tk.Label(frame, text=f"{ticker}:", width=8, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
                label = tk.Label(frame, text="Chargement...")
                label.pack(side=tk.LEFT)
                self.labels_prix[ticker] = label
                self.frames_lignes[ticker] = frame

            var = (prix - ouverture) / ouverture * 100
            symbole = "▲" if var >= 0 else "▼"
            couleur = "green" if var >= 0 else "red"
            self.labels_prix[ticker].config(
                text=f"{prix:.2f} $  {symbole} {abs(var):.2f}%",
                fg=couleur
            )

