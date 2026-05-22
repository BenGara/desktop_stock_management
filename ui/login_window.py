"""UI module for the login window."""

import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from ui.dashboard_window import DashboardWindow


class LoginWindow:
    """Displays the login form and handles user authentication."""

    def __init__(self, root):
        """Build and display the login form inside the given root window."""
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
        """Read credentials from the form and authenticate the user."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        user = AuthService.login(email, password)

        if user:

            messagebox.showinfo(
                "Succès",
                "Connexion réussie"
            )

            self.root.destroy()

            dashboard_root = tk.Tk()

            DashboardWindow(dashboard_root)

            dashboard_root.mainloop()

        else:

            messagebox.showerror(
                "Erreur",
                "Identifiants invalides"
            )

    def clear_fields(self):
        """Clear the email and password input fields."""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
