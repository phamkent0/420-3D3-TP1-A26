from observers.observers import Observateur

class LoggerFichier(Observateur):

    def __init__(self, chemin_fichier: str = "portfolio.csv"):
        self.chemin_fichier = chemin_fichier

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        horodatage = donnees.get("horodatage")
        prix_actuels = donnees.get("prix_actuels",{})

        if not horodatage or not prix_actuels:
            return

        with open(self.chemin_fichier, "a", encoding="utf-8") as f:
            for ticker,(prix,ouverture) in prix_actuels.items():
                f.write(f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n")