"""Point d'entrée de l'application."""

import tkinter as tk

from ui.login_window import LoginWindow


def main():
    """Initialise l'écran de connexion en tant que
    première fenêtre de Tkinter.
    """
    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
