from datetime import datetime
import yfinance as yf
from models.sujet import Sujet


def recuperer_prix(ticker: str):
    info = yf.Ticker(ticker).fast_info
    prix = info.last_price
    ouverture = info.open
    if prix is None:
        raise ValueError(f"Le titre '{ticker}' n'existe pas.")
    return prix, ouverture


class PortfolioSysteme(Sujet):

    def __init__(self):
        super().__init__()
        self._titres = {
            "AAPL": {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
            "GOOGL": {"quantite": 5, "seuil_haut": 160.0, "seuil_bas": 120.0},
            "MSFT": {"quantite": 8, "seuil_haut": 430.0, "seuil_bas": 380.0},
        }
        self._prix_actuels = {}
        self._horodatage = ""

    def actualiser_cours(self) -> None:
        self._prix_actuels.clear()
        for ticker in self._titres:
            try:
                prix, ouverture = recuperer_prix(ticker)
                self._prix_actuels[ticker] = (prix, ouverture)
            except Exception as e:
                print(f"Erreur pour {ticker}: {e}")

        self._horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notifier()

    def get_donnees(self) -> dict:
        donnees_combinees = {}
        for symbole, info_titre in self._titres.items():
            prix, ouverture = self._prix_actuels.get(symbole, (0.0, 0.0))
            donnees_combinees[symbole] = {
                "prix": prix,
                "ouverture": ouverture,
                "quantite": info_titre["quantite"],
                "seuil_haut": info_titre.get("seuil_haut"),
                "seuil_bas": info_titre.get("seuil_bas"),
            }

        return {
            "titres": donnees_combinees,
            "prix_actuels": self._prix_actuels,
            "horodatage": self._horodatage,
        }

    def ajouter_titre(
        self,
        ticker: str,
        quantite: int,
        seuil_bas: float = None,
        seuil_haut: float = None,
    ) -> None:
        ticker = ticker.upper().strip()
        prix, _ = recuperer_prix(ticker)
        self._titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": round(
                seuil_haut if seuil_haut is not None else prix * 1.2, 2
            ),
            "seuil_bas": round(
                seuil_bas if seuil_bas is not None else prix * 0.8, 2
            ),
        }
        self.actualiser_cours()

    def retirer_titre(self, ticker: str) -> None:
        ticker = ticker.upper().strip()
        if ticker in self._titres:
            del self._titres[ticker]
            self.actualiser_cours()