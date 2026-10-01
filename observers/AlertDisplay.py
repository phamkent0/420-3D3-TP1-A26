from observers.observers import Observateur


class Alert(Observateur):

    def __init__(self, seuil_haut, seuil_bas):
        self.seuil_haut = seuil_haut
        self.seuil_bas = seuil_bas

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()

        for symbole in donnees:
            prix = donnees[symbole]["prix"]

            if prix >= self.seuil_haut:
                print("ALERTE :", symbole, "est au-dessus du seuil.")

            elif prix <= self.seuil_bas:
                print("ALERTE :", symbole, "est sous le seuil.")