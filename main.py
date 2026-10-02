import tkinter as tk
from models.portfolio import PortfolioSysteme
from views.dashboard import Dashboard
from observers.logger import LoggerFichier


def rafraichir_automatique(fenetre, portfolio, intervalle_ms=10000):
    """Rafraîchit les cours de bourse périodiquement sans bloquer l'IHM."""
    portfolio.actualiser_cours()
    fenetre.after(
        intervalle_ms,
        lambda: rafraichir_automatique(fenetre, portfolio, intervalle_ms),
    )


def main():
    fenetre = tk.Tk()
    portfolio = PortfolioSysteme()
    dashboard = Dashboard(fenetre, portfolio)
    logger = LoggerFichier("portfolio.csv")
    portfolio.abonner(dashboard)
    portfolio.abonner(logger)
    rafraichir_automatique(fenetre, portfolio, intervalle_ms=15000)
    fenetre.mainloop()


if __name__ == "__main__":
    main()