from logging import root
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
        self.root.geometry("800x450")
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            self.dashboard_parent.refresh()
            
        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)
        
        tk.Label(
            root,
            text="Historique & Journal des Assignations",
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=(15, 10), anchor="w", padx=20)
        
        zone_tableau = tk.Frame(root, bg="#F8F9FA")
        zone_tableau.pack(fill="both", expand=True)

        # Structure du tableau (associé à zone_tableau et ajout de selectmode)
        colonnes = ('id', 'nom_materiel', 'nom_employee', 'date_assignation', 'date_retour')
        self.tableau = ttk.Treeview(zone_tableau, columns=colonnes, show='headings', selectmode="browse")
        
        # En-têtes (uniquement pour les colonnes que l'on veut voir)
        self.tableau.heading('nom_materiel', text='Nom du Matériel')
        self.tableau.heading('nom_employee', text='Nom de l\'Employé')
        self.tableau.heading('date_assignation', text='Date d\'Assignation')
        self.tableau.heading('date_retour', text='Date de Retour')
        
        # Affichage du tableau
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Configuration des tailles de toutes les colonnes
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom_materiel', width=180)
        self.tableau.column('nom_employee', width=150)
        self.tableau.column('date_assignation', width=130)
        self.tableau.column('date_retour', width=130)
        
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        
        zone_boutons_bas = tk.Frame(root, bg="#F8F9FA")
        zone_boutons_bas.pack(fill="x", side=tk.BOTTOM, pady=(0, 15), padx=20)
        
        btn_retour = tk.Button(
            zone_boutons_bas, 
            text="Retour", 
            command=retour_dashboard_window,
            bg="#7F8C8D", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            relief="flat", 
            padx=15, 
            pady=6, 
            cursor="hand2"
        )
        btn_retour.pack(side=tk.RIGHT)
        
        self.charger_journaux()
