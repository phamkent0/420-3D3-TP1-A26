
from observers.observers import Observateur


class PortfolioDisplay(Observateur):

    def __init__(self):
        self.valeur_precedente = 0

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()

        valeur_totale = 0
        valeur_precedente = 0

        for symbole in donnees:

            prix = donnees[symbole]["prix"]
            quantite = donnees[symbole]["quantite"]
            ouverture = donnees[symbole]["ouverture"]

            valeur_totale = valeur_totale + (prix * quantite)

            valeur_precedente = valeur_precedente + (ouverture * quantite)

        variation = valeur_totale - valeur_precedente

        if valeur_precedente != 0:
            pourcentage = (variation / valeur_precedente) * 100
        else:
            pourcentage = 0

        self.afficher_portefeuille(
            valeur_totale,
            variation,
            pourcentage
        )

    def afficher_portefeuille(self, valeur_totale, variation, pourcentage):

        print("\nVALEUR DU PORTEFEUILLE")

        print("Valeur totale :", round(valeur_totale, 2), "$")

        if variation >= 0:
            print("Variation : +", round(variation, 2), "$")
        else:
            print("Variation :", round(variation, 2), "$")

        print("Variation en pourcentage :", round(pourcentage, 2), "%")