import tkinter as tk
from tkinter import ttk, messagebox
from models.assignment_model import AssignmentModel

class JournalWindow:
    """Affiche les informations des journaux 
    et permet de gérer les journaux du système."""
    
    def charger_journaux(self):
        """Récupère les journaux du modèle et les insère dans le Treeview"""
        try:
            liste_journaux = AssignmentModel.get_all_assignments()
            
            for item in self.tableau.get_children():
                self.tableau.delete(item)
                
            for journal in liste_journaux:
                self.tableau.insert('', tk.END, values=journal)
                
        except Exception as e:
            print(f"Erreur lors du chargement des journaux : {e}")


    def __init__(self, root, dashboard_parent):
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Journal")
        self.root.geometry("650x400")
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            
        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)
        
        tk.Label(
            root,
            text="Liste des journaux",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Structure du tableau
        colonnes = ('id', 'nom_materiel', 'nom_employee', 'date_assignation', 'date_retour')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
                
        # En-têtes (Uniquement pour les colonnes que l'on VEUT voir)
        self.tableau.heading('nom_materiel', text='Nom du Matériel')
        self.tableau.heading('nom_employee', text='Nom de l\'Employé')
        self.tableau.heading('date_assignation', text='Date d\'Assignation')
        self.tableau.heading('date_retour', text='Date de Retour')
        
        # Affichage du tableau
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Configuration des tailles de TOUTES les colonnes
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom_materiel', width=100)
        self.tableau.column('nom_employee', width=100)
        self.tableau.column('date_assignation', width=100)
        self.tableau.column('date_retour', width=100)
        
        
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        
        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(pady=10)
        
        # Bouton de retour
        btn_retour = tk.Button(
            zone_boutons, 
            text="Retour", 
            command=retour_dashboard_window,
            padx=10
        )
        btn_retour.pack(side=tk.LEFT, padx=10)
        
        self.charger_journaux()