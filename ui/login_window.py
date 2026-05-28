"""Module de l'interface utilisateur pour la fenêtre de connexion."""

import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from ui.dashboard_window import DashboardWindow


class LoginWindow:
    """Affiche le formulaire de connexionet gère l'authentification
    de l'utilisateur.
    """

    def __init__(self, root):
        """Crée et affiche le formulaire de connexion
        à l'intérieur de la fenêtre initiale donnée.
        """
        self.root = root
        self.root.title("Connexion")
        self.root.geometry("300x200")

        tk.Label(root, text="Email").pack()

        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        tk.Label(root, text="Mot de passe").pack()

        self.password_entry = tk.Entry(
            root,
            show="*"
        )
        self.password_entry.pack()

        tk.Button(
            root,
            text="Connexion",
            command=self.login
        ).pack(pady=10)

    def login(self):
        """Lit les indentifiants dans le formulaire
        et authentifie l'utilisateur.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()

        user = AuthService.login(email, password)

        if user:

            messagebox.showinfo(
                "Succès",
                "Connexion réussie"
            )

            self.root.destroy()
            
            # gestion des roles à faire
            dashboard_root = tk.Tk()

            DashboardWindow(dashboard_root)

            dashboard_root.mainloop()

        else:

            messagebox.showerror(
                "Erreur",
                "Identifiants invalides"
            )

    def clear_fields(self):
        """Efface les champs de saisie de l'adresse e-mail
        et du mot de passe.
        """
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
