"""Module de l'interface utilisateur pour la fenêtre principale du tableau de bord."""

import tkinter as tk
from tkinter import Menu
from tkinter.messagebox import showinfo
from ui.user_window import UserWindow
from ui.materiel_window import MaterielWindow


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
            text="Tableau de bord"
        ).pack(pady=10)

        """La barre de menu"""
        menubar = Menu(self.root)
        
        menubar.add_command(label="Utilisateurs", command=show_user_window)
        menubar.add_command(label="Matériels", command=show_materiel_window)
        
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
