import tkinter as tk
from tkinter import messagebox
from observers.observers import Observateur


class Dashboard(Observateur):

    def __init__(self, fenetre, portfolio):
        self.fenetre = fenetre
        self.portfolio = portfolio
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.geometry("540x760")

        # Titre principal
        tk.Label(
            self.fenetre,
            text="Portfolio Tracker",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=10)

        # 1. Section : Prix en temps réel
        self.frame_prix = tk.LabelFrame(
            self.fenetre, text="Prix en temps réel", padx=10, pady=5
        )
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        # 2. Section : Gérer les titres
        self.frame_gestion = tk.LabelFrame(
            self.fenetre, text="Gérer les titres", padx=10, pady=5
        )
        self.frame_gestion.pack(fill=tk.X, padx=10, pady=5)

        # Formulaire d'ajout
        f_add = tk.Frame(self.frame_gestion)
        f_add.pack(fill=tk.X, pady=2)
        tk.Label(f_add, text="Ticker:").pack(side=tk.LEFT)
        self.entry_ticker = tk.Entry(f_add, width=6)
        self.entry_ticker.pack(side=tk.LEFT, padx=2)

        tk.Label(f_add, text="Qté:").pack(side=tk.LEFT)
        self.entry_qte = tk.Entry(f_add, width=4)
        self.entry_qte.insert(0, "1")
        self.entry_qte.pack(side=tk.LEFT, padx=2)

        tk.Label(f_add, text="Alerte basse:").pack(side=tk.LEFT)
        self.entry_basse = tk.Entry(f_add, width=6)
        self.entry_basse.pack(side=tk.LEFT, padx=2)

        tk.Label(f_add, text="Alerte haute:").pack(side=tk.LEFT)
        self.entry_haute = tk.Entry(f_add, width=6)
        self.entry_haute.pack(side=tk.LEFT, padx=2)

        btn_ajouter = tk.Button(
            f_add, text="Ajouter", command=self._action_ajouter
        )
        btn_ajouter.pack(side=tk.RIGHT)

        tk.Label(
            self.frame_gestion,
            text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
            font=("Segoe UI", 8),
            fg="gray",
        ).pack(anchor="w", pady=2)

        # Liste des titres + Bouton Retirer
        f_list = tk.Frame(self.frame_gestion)
        f_list.pack(fill=tk.X, pady=5)
        self.listbox_titres = tk.Listbox(f_list, height=3)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_titres.bind("<<ListboxSelect>>", self._sur_selection)

        btn_retirer = tk.Button(
            f_list, text="Retirer", command=self._action_retirer
        )
        btn_retirer.pack(side=tk.RIGHT, anchor="n", padx=5)

        # Formulaire de modification de la sélection
        f_mod = tk.Frame(self.frame_gestion)
        f_mod.pack(fill=tk.X, pady=5)

        tk.Label(f_mod, text="Sélection → Qté:").pack(side=tk.LEFT)
        self.entry_mod_qte = tk.Entry(f_mod, width=4)
        self.entry_mod_qte.pack(side=tk.LEFT, padx=2)

        tk.Label(f_mod, text="Alerte basse:").pack(side=tk.LEFT)
        self.entry_mod_basse = tk.Entry(f_mod, width=6)
        self.entry_mod_basse.pack(side=tk.LEFT, padx=2)

        tk.Label(f_mod, text="Alerte haute:").pack(side=tk.LEFT)
        self.entry_mod_haute = tk.Entry(f_mod, width=6)
        self.entry_mod_haute.pack(side=tk.LEFT, padx=2)

        btn_modifier = tk.Button(
            f_mod, text="Modifier sélection", command=self._action_modifier
        )
        btn_modifier.pack(side=tk.RIGHT)

        # 3. Section : Mon portfolio
        self.frame_portfolio = tk.LabelFrame(
            self.fenetre, text="Mon portfolio", padx=10, pady=10
        )
        self.frame_portfolio.pack(fill=tk.X, padx=10, pady=5)

        self.lbl_valeur = tk.Label(
            self.frame_portfolio,
            text="Valeur totale : 0.00 $",
            font=("Segoe UI", 12, "bold"),
        )
        self.lbl_valeur.pack()

        self.lbl_variation = tk.Label(
            self.frame_portfolio, text="0.00 $ depuis l'ouverture"
        )
        self.lbl_variation.pack()

        # 4. Section : Alertes (Fond clair et Texte Rouge)
        self.frame_alertes = tk.LabelFrame(
            self.fenetre, text="Alertes", padx=10, pady=10
        )
        self.frame_alertes.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_alertes = tk.Text(
            self.frame_alertes,
            height=4,
            bg="#f0f0f0",
            fg="red",  # Couleur ROUGE pour les alertes
            font=("Segoe UI", 9),
            relief=tk.FLAT,
        )
        self.text_alertes.pack(fill=tk.BOTH, expand=True)

        # Horodatage
        self.lbl_horodatage = tk.Label(
            self.fenetre,
            text="Dernière mise à jour : --",
            font=("Segoe UI", 8),
            fg="gray",
        )
        self.lbl_horodatage.pack(pady=5)

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        titres = donnees.get("titres", {})
        horodatage = donnees.get("horodatage", "")

        # Mise à jour de la grille des prix
        for widget in self.frame_prix.winfo_children():
            widget.destroy()

        valeur_totale = 0.0
        valeur_ouverture = 0.0
        alertes_textes = []

        self.listbox_titres.delete(0, tk.END)

        for ticker, info in titres.items():
            prix = info["prix"]
            ouverture = info["ouverture"]
            qte = info["quantite"]
            s_bas = info["seuil_bas"]
            s_haut = info["seuil_haut"]

            valeur_totale += prix * qte
            valeur_ouverture += ouverture * qte

            var_pct = (
                ((prix - ouverture) / ouverture * 100) if ouverture != 0 else 0
            )
            symbole_var = "▲" if var_pct >= 0 else "▼"
            couleur_var = "green" if var_pct >= 0 else "red"

            f_row = tk.Frame(self.frame_prix)
            f_row.pack(fill=tk.X, pady=1)
            tk.Label(
                f_row,
                text=f"{ticker}:",
                width=8,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(f_row, text=f"{prix:.2f} $", width=10, anchor="w").pack(
                side=tk.LEFT
            )
            tk.Label(
                f_row,
                text=f"{symbole_var} {abs(var_pct):.2f}%",
                fg=couleur_var,
            ).pack(side=tk.LEFT)

            # Entrée dans la Listbox
            self.listbox_titres.insert(
                tk.END,
                f"{ticker} — {qte} action(s) (alerte : {s_bas:.2f} $ / {s_haut:.2f} $)",
            )

            # Détection d'alerte (avec le symbole ⚠ comme sur l'image)
            if prix >= s_haut and s_haut > 0:
                alertes_textes.append(
                    f"⚠ {ticker} dépasse le seuil haut ({prix:.2f} $ ≥ {s_haut:.2f} $)"
                )
            elif prix <= s_bas and prix > 0:
                alertes_textes.append(
                    f"⚠ {ticker} dépasse le seuil bas ({prix:.2f} $ ≤ {s_bas:.2f} $)"
                )

        # Portfolio
        var_totale = valeur_totale - valeur_ouverture
        couleur_totale = "green" if var_totale >= 0 else "red"
        signe = "+" if var_totale >= 0 else ""

        self.lbl_valeur.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )
        self.lbl_variation.config(
            text=f"▼ {abs(var_totale):.2f} $ depuis l'ouverture"
            if var_totale < 0
            else f"▲ {var_totale:.2f} $ depuis l'ouverture",
            fg=couleur_totale,
        )

        # Affichage des alertes en rouge
        self.text_alertes.config(state=tk.NORMAL)
        self.text_alertes.delete("1.0", tk.END)
        if alertes_textes:
            for alerte in alertes_textes:
                self.text_alertes.insert(tk.END, alerte + "\n")
        else:
            self.text_alertes.insert(tk.END, "Aucune alerte.")
        self.text_alertes.config(state=tk.DISABLED)

        # Horodatage
        self.lbl_horodatage.config(
            text=f"Dernière mise à jour : {horodatage}"
        )

    def _sur_selection(self, event):
        """Remplit automatiquement les champs de modification lors d'un clic sur un titre."""
        selection = self.listbox_titres.curselection()
        if selection:
            texte = self.listbox_titres.get(selection[0])
            ticker = texte.split(" — ")[0]
            donnees = self.portfolio.get_donnees().get("titres", {})
            if ticker in donnees:
                info = donnees[ticker]
                self.entry_mod_qte.delete(0, tk.END)
                self.entry_mod_qte.insert(0, str(info["quantite"]))

                self.entry_mod_basse.delete(0, tk.END)
                self.entry_mod_basse.insert(0, str(info["seuil_bas"]))

                self.entry_mod_haute.delete(0, tk.END)
                self.entry_mod_haute.insert(0, str(info["seuil_haut"]))

    def _action_ajouter(self):
        ticker = self.entry_ticker.get().strip()
        try:
            qte = int(self.entry_qte.get())
            s_bas = (
                float(self.entry_basse.get()) if self.entry_basse.get() else None
            )
            s_haut = (
                float(self.entry_haute.get()) if self.entry_haute.get() else None
            )
            if not ticker:
                raise ValueError("Veuillez entrer un symbole.")

            self.portfolio.ajouter_titre(ticker, qte, s_bas, s_haut)
            self.entry_ticker.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _action_retirer(self):
        selection = self.listbox_titres.curselection()
        if selection:
            texte = self.listbox_titres.get(selection[0])
            ticker = texte.split(" — ")[0]
            self.portfolio.retirer_titre(ticker)

    def _action_modifier(self):
        selection = self.listbox_titres.curselection()
        if not selection:
            messagebox.showwarning(
                "Avertissement", "Veuillez sélectionner un titre dans la liste."
            )
            return

        texte = self.listbox_titres.get(selection[0])
        ticker = texte.split(" — ")[0]

        try:
            qte = int(self.entry_mod_qte.get())
            s_bas = float(self.entry_mod_basse.get())
            s_haut = float(self.entry_mod_haute.get())

            self.portfolio.ajouter_titre(ticker, qte, s_bas, s_haut)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))