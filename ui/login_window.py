# -*- coding: utf-8 -*-
"""Module de l'interface utilisateur pour la fenêtre de connexion."""

import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from services.session_service import SessionService
from ui.dashboard_window import DashboardWindow


class LoginWindow:
    """Affiche le formulaire de connexion et gère l'authentification."""

    def __init__(self, root):
        """Crée et affiche le formulaire de connexion."""
        self.root = root
        self.root.title("Connexion - Stock Manager")
        self.root.geometry("360x320")
        self.root.configure(bg="#F8F9FA")

        card_frame = tk.Frame(root, bg="white", bd=1, relief="groove", padx=20, pady=20)
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=310, height=260)

        tk.Label(
            card_frame, text="AUTHENTIFICATION", bg="white", fg="#2C3E50",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 15))

        tk.Label(card_frame, text="Adresse Email", bg="white", fg="#7F8C8D",
                 font=("Arial", 9, "bold")).pack(anchor="w")
        self.email_entry = tk.Entry(
            card_frame, font=("Arial", 10), bg="#F8F9FA",
            highlightthickness=1, highlightbackground="#BDC3C7", relief="flat"
        )
        self.email_entry.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(card_frame, text="Mot de passe", bg="white", fg="#7F8C8D",
                 font=("Arial", 9, "bold")).pack(anchor="w")
        self.password_entry = tk.Entry(
            card_frame, show="*", font=("Arial", 10), bg="#F8F9FA",
            highlightthickness=1, highlightbackground="#BDC3C7", relief="flat"
        )
        self.password_entry.pack(fill="x", pady=(2, 15), ipady=4)

        tk.Button(
            card_frame, text="Se connecter", command=self.login,
            bg="#2C3E50", fg="white", font=("Arial", 10, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#34495E", activeforeground="white"
        ).pack(fill="x", ipady=6)

        # Permettre la connexion via la touche Entrée
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        """Lit les identifiants du formulaire et authentifie l'utilisateur."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Champs requis", "Veuillez remplir l'email et le mot de passe.")
            return

        user = AuthService.login(email, password)

        if user:
            self.root.withdraw()   # Cache la fenêtre de login (sans la détruire)

            dashboard_root = tk.Toplevel(self.root)
            DashboardWindow(dashboard_root, self.root)
        else:
            messagebox.showerror("Erreur", "Identifiants invalides.")
            self.password_entry.delete(0, tk.END)

    def clear_fields(self):
        """Efface les champs de saisie."""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
