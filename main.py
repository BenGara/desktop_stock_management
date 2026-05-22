"""Entry point for the Stock Management desktop application."""

import tkinter as tk

from ui.login_window import LoginWindow


def main():
    """Initialise the Tkinter root window and launch the login screen."""
    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
