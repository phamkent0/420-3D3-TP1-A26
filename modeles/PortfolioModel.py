from datetime import datetime
from logging import info
import yfinance as yf
from modeles.sujet import Sujet

def recuperer_donnees(ticker:str):
    info = yf.Ticker(ticker).info
    prix = info["regularMarketPrice"]
    if prix is None:
        raise ValueError(f"Impossible de récupérer le prix pour le ticker {ticker}.")
    return prix,info["open"]

class PortfolioModel(Sujet):
    def __init__(self):
        super().__init__()
        self._portfolio = {
            "AAPL":  {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
            "GOOGL": {"quantite": 5,  "seuil_haut": 160.0, "seuil_bas": 120.0},
            "MSFT":  {"quantite": 8,  "seuil_haut": 430.0, "seuil_bas": 380.0},
        }
    self._prix_actuel = {}
    self._horodatage = ""

    def actualiser_donnees(self) -> None:
        self._prix_actuel.clear()
        for ticker in self._portfolio.keys():
            try:
                prix, ouverture = recuperer_donnees(ticker)
                self._prix_actuel[ticker] = {"prix": prix, "open": ouverture}
            except ValueError as e:
                print(f"Erreur lors de la récupération des données pour {ticker}: {e}")

        self._horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notifier_observateurs()
        

    def get_donnees(self):
        return {
            "titres": self._portfolio,
            "prix": self._prix_actuel,
            "horodatage": self._horodatage
        }
    