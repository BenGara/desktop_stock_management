"""Module de l'interface utilisateur pour la fenêtre de gestion des matériels."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.material_model import MaterialModel

class MaterielWindow:
    """Affiche les informations des matériels 
    et permet de gérer les matériels du stock."""

    def charger_materiels(self):
        """Récupère les matériels du modèle et les insère dans le Treeview"""
        try:
            liste_materiels = MaterialModel.get_all_materials()
            
            for item in self.tableau.get_children():
                self.tableau.delete(item)
                
            for materiel in liste_materiels:
                self.tableau.insert('', tk.END, values=materiel)
                
        except Exception as e:
            print(f"Erreur lors du chargement des matériels : {e}")

    def __init__(self, root, dashboard_parent):
        """Crée et affiche les informations du matériel
        à l'intérieur de la fenêtre initiale donnée.
        """
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Matériels")
        self.root.geometry("650x400")
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        tk.Label(
            root,
            text="Informations des matériels"
        ).pack(pady=10)
        
        #tableau d'affichage des matériels
        colonnes = ('id', 'nom', 'numéro de série', 'catégorie', 'quantité', 'status', 'date d\'achat')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
        self.tableau.heading('id', text='ID')
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('numéro de série', text='Numéro de Série')
        self.tableau.heading('catégorie', text='Catégorie')
        self.tableau.heading('quantité', text='Quantité')
        self.tableau.heading('status', text='Status')
        self.tableau.heading('date d\'achat', text='Date d\'achat')
        
        self.tableau.column('id', width=30, anchor='center')
        self.tableau.column('nom', width=100)
        self.tableau.column('numéro de série', width=100)
        self.tableau.column('catégorie', width=100)
        self.tableau.column('quantité', width=80)
        self.tableau.column('status', width=100)
        self.tableau.column('date d\'achat', width=100)
        
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)

        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(pady=10)
        
        # Bouton de retour
        btn_retour = tk.Button(
            zone_boutons, 
            text="← Retour", 
            command=retour_dashboard_window,
            padx=10
        )
        btn_retour.pack(side=tk.LEFT, padx=10)

        self.charger_materiels()