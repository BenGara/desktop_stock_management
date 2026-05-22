"""Module de l'interface utilisateur pour la fenêtre principale du tableau de bord."""

import tkinter as tk


class DashboardWindow:
    """Affiche le tableau de bord de gestion des stocks
    avec les principales informations du stock.
    """

    def __init__(self, root):
        """Crée et affiche la mise en page du tableau de bord
        à l'intérieur de la fenêtre initiale donnée.
        """
        self.root = root
        self.root.title("Dashboard")

        tk.Label(
            root,
            text="Tableau de bord"
        ).pack(pady=10)

        self.in_stock_label = tk.Label(root, text="Matériels en stock")
        self.in_stock_label.pack()

        self.assigned_label = tk.Label(root, text="Matériels affectés")
        self.assigned_label.pack()

        self.broken_label = tk.Label(root, text="Matériels en panne")
        self.broken_label.pack()

    def refresh(self):
        """Actualise les données du tableau de bord
        et met à jour les intitulés affichés.
        """
        self.in_stock_label.config(text="Matériels en stock")
        self.assigned_label.config(text="Matériels affectés")
        self.broken_label.config(text="Matériels en panne")

    def set_title(self, title):
        """Met à jour le titre de la fenêtre initiale."""
        self.root.title(title)
