"""UI module for the main dashboard window."""

import tkinter as tk


class DashboardWindow:
    """Displays the stock management dashboard with key inventory indicators."""

    def __init__(self, root):
        """Build and display the dashboard layout inside the given root window."""
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
        """Reload dashboard data and update the displayed labels."""
        self.in_stock_label.config(text="Matériels en stock")
        self.assigned_label.config(text="Matériels affectés")
        self.broken_label.config(text="Matériels en panne")

    def set_title(self, title):
        """Update the root window title."""
        self.root.title(title)
