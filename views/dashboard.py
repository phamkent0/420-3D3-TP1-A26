import tkinter as tk
from observers.observers import Observateur


class Dashboard(Observateur):

    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Portfolio Tracker - Dashboard")

        self.lignes_titres = {}

        # Titre principal
        titre = tk.Label(
            self.fenetre,
            text="Portfolio Tracker",
            font=("Segoe UI", 18, "bold")
        )
        titre.pack(pady=10)

        # Section des prix
        self.frame_prix = tk.LabelFrame(
            self.fenetre,
            text="Prix des titres",
            padx=10,
            pady=10
        )
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        # En-têtes du tableau
        tk.Label(
            self.frame_prix,
            text="Titre",
            font=("Segoe UI", 10, "bold"),
            width=12
        ).grid(row=0, column=0)

        tk.Label(
            self.frame_prix,
            text="Prix actuel",
            font=("Segoe UI", 10, "bold"),
            width=15
        ).grid(row=0, column=1)

        tk.Label(
            self.frame_prix,
            text="Variation",
            font=("Segoe UI", 10, "bold"),
            width=15
        ).grid(row=0, column=2)

        tk.Label(
            self.frame_prix,
            text="Quantité",
            font=("Segoe UI", 10, "bold"),
            width=12
        ).grid(row=0, column=3)

        # Section du portefeuille
        self.frame_portefeuille = tk.LabelFrame(
            self.fenetre,
            text="Mon portefeuille",
            padx=10,
            pady=10
        )
        self.frame_portefeuille.pack(fill=tk.X, padx=10, pady=5)

        self.label_valeur = tk.Label(
            self.frame_portefeuille,
            text="Valeur totale : En attente des données",
            font=("Segoe UI", 12, "bold")
        )
        self.label_valeur.pack()

        self.label_variation = tk.Label(
            self.frame_portefeuille,
            text=""
        )
        self.label_variation.pack()

        self.label_maj = tk.Label(
            self.fenetre,
            text="En attente de la première mise à jour...",
            font=("Segoe UI", 9),
            fg="gray"
        )
        self.label_maj.pack(pady=5)

    def actualiser(self, sujet):
        """
        Appelée automatiquement lorsque le sujet notifie
        ses observateurs.
        """
        donnees = sujet.get_donnees()

        valeur_totale = 0
        valeur_ouverture = 0

        # Parcourir les titres reçus du sujet
        for symbole in donnees:
            prix = donnees[symbole]["prix"]
            ouverture = donnees[symbole]["ouverture"]
            quantite = donnees[symbole]["quantite"]

            valeur_totale += prix * quantite
            valeur_ouverture += ouverture * quantite

            variation = prix - ouverture

            if ouverture != 0:
                variation_pourcentage = (variation / ouverture) * 100
            else:
                variation_pourcentage = 0

            self.afficher_titre(
                symbole,
                prix,
                variation_pourcentage,
                quantite
            )

        # Calculer la variation totale du portefeuille
        variation_totale = valeur_totale - valeur_ouverture

        if valeur_ouverture != 0:
            variation_pourcentage_totale = (
                variation_totale / valeur_ouverture
            ) * 100
        else:
            variation_pourcentage_totale = 0

        self.afficher_portefeuille(
            valeur_totale,
            variation_totale,
            variation_pourcentage_totale
        )

        self.label_maj.config(
            text="Dashboard mis à jour"
        )

    def afficher_titre(self, symbole, prix, variation, quantite):
        """
        Crée ou met à jour la ligne d'un titre.
        """

        # Créer les labels seulement si le titre n'existe pas encore
        if symbole not in self.lignes_titres:

            ligne = len(self.lignes_titres) + 1

            label_symbole = tk.Label(
                self.frame_prix,
                text=symbole,
                width=12
            )
            label_symbole.grid(row=ligne, column=0)

            label_prix = tk.Label(
                self.frame_prix,
                text="",
                width=15
            )
            label_prix.grid(row=ligne, column=1)

            label_variation = tk.Label(
                self.frame_prix,
                text="",
                width=15
            )
            label_variation.grid(row=ligne, column=2)

            label_quantite = tk.Label(
                self.frame_prix,
                text="",
                width=12
            )
            label_quantite.grid(row=ligne, column=3)

            self.lignes_titres[symbole] = {
                "prix": label_prix,
                "variation": label_variation,
                "quantite": label_quantite
            }

        # Mettre à jour les valeurs affichées
        labels = self.lignes_titres[symbole]

        labels["prix"].config(
            text=round(prix, 2).__str__() + " $"
        )

        if variation >= 0:
            texte_variation = "+" + str(round(variation, 2)) + " %"
            couleur = "green"
        else:
            texte_variation = str(round(variation, 2)) + " %"
            couleur = "red"

        labels["variation"].config(
            text=texte_variation,
            fg=couleur
        )

        labels["quantite"].config(
            text=str(quantite)
        )

    def afficher_portefeuille(
        self,
        valeur_totale,
        variation,
        variation_pourcentage
    ):
        """
        Met à jour la valeur totale et la variation du portefeuille.
        """

        self.label_valeur.config(
            text="Valeur totale : " + str(round(valeur_totale, 2)) + " $"
        )

        if variation >= 0:
            texte = (
                "Variation : +"
                + str(round(variation, 2))
                + " $ ("
                + str(round(variation_pourcentage, 2))
                + " %)"
            )
            couleur = "green"
        else:
            texte = (
                "Variation : "
                + str(round(variation, 2))
                + " $ ("
                + str(round(variation_pourcentage, 2))
                + " %)"
            )
            couleur = "red"

        self.label_variation.config(
            text=texte,
            fg=couleur
        )