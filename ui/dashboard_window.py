"""Module de l'interface utilisateur pour la fenêtre principale du tableau de bord."""

import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter.messagebox import showinfo

from ui.journal_window import JournalWindow
from ui.user_window import UserWindow
from ui.materiel_window import MaterielWindow
from ui.categorie_window import CategorieWindow

from models.stat_model import StatModel

class DashboardWindow:
    """Affiche le tableau de bord de gestion des stocks
    avec les principales informations du stock.
    """

    def refresh(self):
        """Actualise les données du tableau de bord
        et met à jour les intitulés affichés.
        """
        stock_stats = StatModel.get_stock_stats()
        self.in_stock_label.config(text=f"Matériels en stock: {stock_stats[0]} ({stock_stats[1]})")

        assigned_stats = StatModel.get_materiel_affecte_stats()
        self.assigned_label.config(text=f"Matériels affectés: {assigned_stats[0]}")

        broken_stats = StatModel.get_materiel_panne_stats()
        self.broken_label.config(text=f"Matériels en panne: {broken_stats[0]}")

    def set_title(self, title):
        """Met à jour le titre de la fenêtre initiale."""
        self.root.title(title)

    def __init__(self, root):
        """Crée et affiche la mise en page du tableau de bord
        à l'intérieur de la fenêtre initiale donnée.
        """
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("400x350")
        
        """Fonction Barre de navigation"""
        def show_user_window():
            self.root.withdraw()
            user_window = tk.Toplevel(self.root)
            UserWindow(user_window, dashboard_parent=self)

        def show_materiel_window():
            self.root.withdraw()
            materiel_window = tk.Toplevel(self.root)
            MaterielWindow(materiel_window, dashboard_parent=self)
            
        def show_categorie_window():
            self.root.withdraw()
            categorie_window = tk.Toplevel(self.root)
            CategorieWindow(categorie_window, dashboard_parent=self)
            
        def show_log_window():
            self.root.withdraw()
            log_window = tk.Toplevel(self.root)
            JournalWindow(log_window, dashboard_parent=self) 
                       
        """Fonction déconnexion"""
        def deconnexion():
            self.root.destroy()
            from ui.login_window import LoginWindow
            
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()
        
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        tk.Label(
            root,
            text="Tableau de bord",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        """La barre de menu"""
        menubar = Menu(self.root)
        
        menubar.add_command(label="Utilisateurs", command=show_user_window)
        menubar.add_command(label="Matériels", command=show_materiel_window)
        menubar.add_command(label="Catégories", command=show_categorie_window)
        menubar.add_command(label="Journal", command=show_log_window)
        self.root.config(menu=menubar)

        """Statistiques du stock"""
        self.in_stock_label = tk.Label(root, text="Matériels en stock")
        self.in_stock_label.pack()

        self.assigned_label = tk.Label(root, text="Matériels affectés")
        self.assigned_label.pack()

        self.broken_label = tk.Label(root, text="Matériels en panne")
        self.broken_label.pack()
        
        btn_logout = tk.Button(
            root,
            text="Se déconnecter",
            command=deconnexion,
            bg="#DC3545",  # Rouge discret pour l'action de déconnexion
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        # Positionné tout en bas avec un espacement confortable
        btn_logout.pack(side=tk.BOTTOM, pady=20)
        
        self.refresh()