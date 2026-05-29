# -*- coding: utf-8 -*-
"""Module de l'interface utilisateur pour la fenêtre de retour de matériel."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.assignment_model import AssignmentModel


class ReturnWindow:
    """Interface graphique pour gérer la restitution et les retours des matériels."""

    def charger_affectations(self):
        """Récupère les affectations actives du modèle et les insère dans le Treeview."""
        # Nettoyage du tableau avant insertion
        for item in self.tableau.get_children():
            self.tableau.delete(item)
            
        try:
            # Appel direct de la méthode de ton modèle AssignmentModel
            liste_affectations = AssignmentModel.get_active_assignments()
            
            for aff in liste_affectations:
                # aff[0]: id, aff[1]: utilisateur (nom complet), aff[2]: nom matériel, 
                # aff[3]: numéro de série, aff[4]: date d'affectation
                self.tableau.insert('', tk.END, values=aff)
                
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Erreur lors du chargement des affectations actives : {e}"
            )

    def enregistrer_retour(self):
        """Prend la ligne sélectionnée et traite le retour du matériel en BDD."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning(
                "Sélection requise", 
                "Veuillez sélectionner une affectation dans le tableau."
            )
            return

        # Extraction des données de la ligne sélectionnée
        valeurs = self.tableau.item(selection, 'values')
        assignment_id = valeurs[0]
        nom_utilisateur = valeurs[1]
        nom_materiel = valeurs[2]
        
        # Récupération du statut choisi dans la Combobox ("Disponible" ou "En panne")
        status_choisi = self.combo_status.get()

        # Message de confirmation explicite
        confirm = messagebox.askyesno(
            "Confirmer le retour", 
            f"Confirmez-vous le retour du matériel :\n\n"
            f"• Matériel : {nom_materiel}\n"
            f"• Détenu par : {nom_utilisateur}\n"
            f"• État déclaré : {status_choisi}\n\n"
            f"Voulez-vous valider ?",
            parent=self.root
        )
        
        if confirm:
            try:
                # Exécution de la logique de retour codée dans ton AssignmentModel
                AssignmentModel.process_material_return(assignment_id, status_choisi)
                
                messagebox.showinfo(
                    "Succès", 
                    "Le retour a été enregistré. Le matériel a été réintégré.",
                    parent=self.root
                )
                
                # Actualisation locale du tableau des retours
                self.charger_affectations()  
                
                # Actualisation des compteurs de ton Dashboard principal (Cartes de stats)
                if self.parent_dashboard:
                    self.parent_dashboard.refresh()
                    
            except Exception as e:
                messagebox.showerror(
                    "Erreur", 
                    f"Impossible de traiter le retour du matériel : {e}",
                    parent=self.root
                )

    def quitter(self):
        """Ferme la fenêtre de retour et réaffiche proprement le tableau de bord."""
        self.root.destroy()
        if self.parent_dashboard:
            self.parent_dashboard.root.deiconify()

    def __init__(self, root, parent_dashboard):
        """Initialise la fenêtre de gestion des retours."""
        self.root = root
        self.parent_dashboard = parent_dashboard
        
        self.root.title("Retour de Matériel Informatique")
        self.root.geometry("750x480")
        self.root.configure(bg="#F8F9FA")

        # Interception de la fermeture par la croix (X)
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        # En-tête / Titre
        tk.Label(
            self.root, text="Enregistrement des Retours de Matériels", 
            bg="#F8F9FA", fg="#2C3E50", font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 5))
        
        tk.Label(
            self.root, text="Sélectionnez un prêt actif ci-dessous pour restituer l'équipement au stock.", 
            bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9)
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # Cadre contenant le Treeview et sa Scrollbar
        cadre_tableau = tk.Frame(self.root, bg="#F8F9FA")
        cadre_tableau.pack(fill="both", expand=True, padx=25, pady=5)

        # Définition des colonnes du tableau basées sur ton SELECT SQL
        colonnes = ("id", "utilisateur", "materiel", "serial", "date")
        self.tableau = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings", selectmode="browse")
        
        self.tableau.heading("id", text="ID")
        self.tableau.heading("utilisateur", text="Collaborateur / Utilisateur")
        self.tableau.heading("materiel", text="Désignation du Matériel")
        self.tableau.heading("serial", text="Numéro de Série")
        self.tableau.heading("date", text="Date d'affectation")

        # Configuration des dimensions et alignements
        self.tableau.column("id", width=50, anchor="center")
        self.tableau.column("utilisateur", width=180, anchor="w")
        self.tableau.column("materiel", width=180, anchor="w")
        self.tableau.column("serial", width=130, anchor="w")
        self.tableau.column("date", width=120, anchor="center")
        
        self.tableau.pack(side=tk.LEFT, fill="both", expand=True)

        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(cadre_tableau, orient=tk.VERTICAL, command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Zone du formulaire d'action en bas
        zone_actions = tk.LabelFrame(
            self.root, text=" Action de restitution ", 
            bg="white", font=("Arial", 9, "bold"), padx=15, pady=15
        )
        zone_actions.pack(fill="x", padx=25, pady=20)

        tk.Label(
            zone_actions, text="État de l'équipement au retour :", 
            bg="white", font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        # Liste déroulante des statuts pour correspondre aux traitements de process_material_return
        self.combo_status = ttk.Combobox(zone_actions, values=["Disponible", "En panne"], state="readonly", width=15)
        self.combo_status.set("Disponible")
        self.combo_status.pack(side=tk.LEFT, padx=5)

        # Bouton pour valider l'action
        btn_valider = tk.Button(
            zone_actions, text="Valider la restitution", command=self.enregistrer_retour,
            bg="#27AE60", fg="white", font=("Arial", 10, "bold"), 
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_valider.pack(side=tk.RIGHT, padx=5)

        # Bouton d'annulation
        btn_annuler = tk.Button(
            zone_actions, text="Retour", command=self.quitter,
            bg="#7F8C8D", fg="white", font=("Arial", 10), 
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_annuler.pack(side=tk.RIGHT, padx=5)

        # Premier chargement automatique des lignes au démarrage de la fenêtre
        self.charger_affectations()