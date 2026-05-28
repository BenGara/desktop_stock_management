"""Module de l'interface utilisateur pour la fenêtre de gestion des catégories."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.categorie_model import CategorieModel

class CategorieWindow:
    """Affiche les informations des catégories 
    et permet de gérer les catégories du stock."""

    def charger_categories(self):
        """Récupère les catégories du modèle et les insère dans le Treeview"""
        try:
            liste_categories = CategorieModel.get_all_categories()
            
            for item in self.tableau.get_children():
                self.tableau.delete(item)
                
            for categorie in liste_categories:
                # Si la description est None en BDD, on affiche une chaîne vide
                cat_id, nom, desc = categorie
                desc = desc if desc is not None else ""
                self.tableau.insert('', tk.END, values=(cat_id, nom, desc))
                
        except Exception as e:
            print(f"Erreur lors du chargement des catégories : {e}")

    def sur_selection_ligne(self, event):
        """Remplit le champ de saisie lorsqu'on clique sur une ligne."""
        selection = self.tableau.selection()
        if selection:
            valeurs = self.tableau.item(selection[0], 'values')
            
            # Remplit le champ Nom
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, valeurs[1])
            
            # Remplit le champ Description
            self.entry_description.delete(0, tk.END)
            self.entry_description.insert(0, valeurs[2])
            
            # États des boutons
            self.btn_ajouter.config(state=tk.DISABLED)
            self.btn_modifier.config(state=tk.NORMAL)
            self.btn_supprimer.config(state=tk.NORMAL)
        else:
            self.reinitialiser_formulaire()

    def reinitialiser_formulaire(self):
        """Vide les champs de saisie et réinitialise les boutons."""
        self.entry_nom.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.tableau.selection_remove(self.tableau.selection())
        self.btn_ajouter.config(state=tk.NORMAL)
        self.btn_modifier.config(state=tk.DISABLED)
        self.btn_supprimer.config(state=tk.DISABLED)

    def ajouter_categorie(self):
        """Fonction d'ajout d'une catégorie."""
        nom = self.entry_nom.get().strip()
        description = self.entry_description.get().strip()
        
        if not nom:
            messagebox.showwarning("Saisie vide", "Veuillez entrer un nom de catégorie.", parent=self.root)
            return
        try:
            CategorieModel.create_categorie(nom, description)
            messagebox.showinfo("Succès", f"Catégorie '{nom}' ajoutée !", parent=self.root)
            self.charger_categories()
            self.reinitialiser_formulaire()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter : {e}", parent=self.root)

    def modifier_categorie(self):
        """Fonction de modification de la catégorie sélectionnée."""
        selection = self.tableau.selection()
        if not selection:
            return
        
        cat_id = self.tableau.item(selection[0], 'values')[0]
        nouveau_nom = self.entry_nom.get().strip()
        nouvelle_description = self.entry_description.get().strip()

        if not nouveau_nom:
            messagebox.showwarning("Saisie vide", "Le nom ne peut pas être vide.", parent=self.root)
            return

        try:
            CategorieModel.update_categorie(cat_id, nouveau_nom, nouvelle_description)
            messagebox.showinfo("Succès", "Catégorie modifiée !", parent=self.root)
            self.charger_categories()
            self.reinitialiser_formulaire()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de modifier : {e}", parent=self.root)

    def supprimer_categorie(self):
        """Fonction de suppression de la catégorie sélectionnée."""
        selection = self.tableau.selection()
        if not selection:
            return
            
        valeurs = self.tableau.item(selection[0], 'values')
        cat_id = valeurs[0]
        nom = valeurs[1]

        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Voulez-vous vraiment supprimer la catégorie '{nom}' ?\nAttention, cela peut affecter les matériels liés !",
            parent=self.root
        )
        if confirm:
            try:
                CategorieModel.delete_categorie(cat_id)
                messagebox.showinfo("Succès", "Catégorie supprimée !", parent=self.root)
                self.charger_categories()
                self.reinitialiser_formulaire()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Crée et affiche les informations de la catégorie."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Catégories")
        self.root.geometry("750x450") # Légèrement agrandi pour accueillir la colonne description
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            
        tk.Label(
            root,
            text="Informations des catégories",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # --- CONTENEUR CENTRAL ---
        conteneur_central = tk.Frame(root)
        conteneur_central.pack(fill="both", expand=True, padx=10)
        
        # --- ZONE FORMULAIRE (À GAUCHE) ---
        zone_formulaire = tk.Frame(conteneur_central, width=220)
        zone_formulaire.pack(side=tk.LEFT, fill="y", padx=10, pady=10)
        zone_formulaire.pack_propagate(False)
        
        tk.Label(zone_formulaire, text="Action / Saisie", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0,10))
        
        # Champ Nom
        tk.Label(zone_formulaire, text="Nom :").pack(anchor="w")
        self.entry_nom = tk.Entry(zone_formulaire)
        self.entry_nom.pack(fill="x", pady=5)
        
        # NOUVEAU : Champ Description
        tk.Label(zone_formulaire, text="Description :").pack(anchor="w")
        self.entry_description = tk.Entry(zone_formulaire)
        self.entry_description.pack(fill="x", pady=5)
        
        # Bouton Ajouter
        self.btn_ajouter = tk.Button(
            zone_formulaire, text="Ajouter", command=self.ajouter_categorie,
            bg="#28A745", fg="white", font=("Arial", 9, "bold"), cursor="hand2"
        )
        self.btn_ajouter.pack(fill="x", pady=5)
        
        # Bouton Modifier
        self.btn_modifier = tk.Button(
            zone_formulaire, text="Modifier", command=self.modifier_categorie,
            bg="#007ACC", fg="white", font=("Arial", 9, "bold"), state=tk.DISABLED, cursor="hand2"
        )
        self.btn_modifier.pack(fill="x", pady=5)
        
        # Bouton Supprimer
        self.btn_supprimer = tk.Button(
            zone_formulaire, text="Supprimer", command=self.supprimer_categorie,
            bg="#DC3545", fg="white", font=("Arial", 9, "bold"), state=tk.DISABLED, cursor="hand2"
        )
        self.btn_supprimer.pack(fill="x", pady=5)
        
        # Bouton Annuler/Vider
        btn_annuler = tk.Button(
            zone_formulaire, text="Vider la sélection", command=self.reinitialiser_formulaire,
            font=("Arial", 9), pady=2, cursor="hand2"
        )
        btn_annuler.pack(fill="x", pady=(15, 0))
        
        # --- ZONE TABLEAU (À DROITE) ---
        zone_tableau = tk.Frame(conteneur_central)
        zone_tableau.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        
        # Ajout de 'description' dans le tuple des colonnes du Treeview
        colonnes = ('id', 'nom', 'description')
        self.tableau = ttk.Treeview(zone_tableau, columns=colonnes, show='headings')
        
        # En-têtes visibles
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('description', text='Description')
        
        self.tableau.pack(fill='both', expand=True)
        
        # Configuration des tailles (L'ID reste masqué à 0px)
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom', width=120)
        self.tableau.column('description', width=250) # Colonne description spacieuse
        
        self.tableau.bind('<<TreeviewSelect>>', self.sur_selection_ligne)
        
        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(side=tk.BOTTOM, pady=15)
        
        btn_retour = tk.Button(
            zone_boutons, 
            text="Retour", 
            command=retour_dashboard_window,
            padx=20
        )
        btn_retour.pack()
        
        self.charger_categories()

# """Module de l'interface utilisateur pour la fenêtre de gestion des catégories."""

# import tkinter as tk
# from tkinter import ttk, messagebox
# from models.categorie_model import CategorieModel

# class CategorieWindow:
#     """Affiche les informations des catégories 
#     et permet de gérer les catégories du stock."""

#     def charger_categories(self):
#         """Récupère les catégories du modèle et les insère dans le Treeview"""
#         try:
#             liste_categories = CategorieModel.get_all_categories()
            
#             for item in self.tableau.get_children():
#                 self.tableau.delete(item)
                
#             for categorie in liste_categories:
#                 self.tableau.insert('', tk.END, values=categorie)
                
#         except Exception as e:
#             print(f"Erreur lors du chargement des catégories : {e}")

#     def sur_selection_ligne(self, event):
#         """Remplit le champ de saisie lorsqu'on clique sur une ligne."""
#         selection = self.tableau.selection()
#         if selection:
#             valeurs = self.tableau.item(selection[0], 'values')
#             self.entry_nom.delete(0, tk.END)
#             self.entry_nom.insert(0, valeurs[1]) # Injecte le nom dans la case
            
#             # Gestion des états des boutons pour éviter les erreurs
#             self.btn_ajouter.config(state=tk.DISABLED)
#             self.btn_modifier.config(state=tk.NORMAL)
#             self.btn_supprimer.config(state=tk.NORMAL)
#         else:
#             self.reinitialiser_formulaire()

#     def reinitialiser_formulaire(self):
#         """Vide le champ de saisie et réinitialise les boutons."""
#         self.entry_nom.delete(0, tk.END)
#         self.tableau.selection_remove(self.tableau.selection())
#         self.btn_ajouter.config(state=tk.NORMAL)
#         self.btn_modifier.config(state=tk.DISABLED)
#         self.btn_supprimer.config(state=tk.DISABLED)        
        
#     def ajouter_categorie(self):
#         """Fonction d'ajout d'une catégorie."""
#         nom = self.entry_nom.get().strip()
#         if not nom:
#             messagebox.showwarning("Saisie vide", "Veuillez entrer un nom de catégorie.", parent=self.root)
#             return
#         try:
#             CategorieModel.create_categorie(nom)
#             messagebox.showinfo("Succès", f"Catégorie '{nom}' ajoutée !", parent=self.root)
#             self.charger_categories()
#             self.reinitialiser_formulaire()
#         except Exception as e:
#             messagebox.showerror("Erreur", f"Impossible d'ajouter : {e}", parent=self.root)

#     def modifier_categorie(self):
#         """Fonction de modification de la catégorie sélectionnée."""
#         selection = self.tableau.selection()
#         if not selection:
#             return
        
#         # Récupération de l'id masqué (index 0) et du nom saisi
#         cat_id = self.tableau.item(selection[0], 'values')[0]
#         nouveau_nom = self.entry_nom.get().strip()

#         if not nouveau_nom:
#             messagebox.showwarning("Saisie vide", "Le nom ne peut pas être vide.", parent=self.root)
#             return

#         try:
#             # Pense à vérifier le nom de la méthode de mise à jour dans ton CategorieModel
#             CategorieModel.update_categorie(cat_id, nouveau_nom)
#             messagebox.showinfo("Succès", "Catégorie modifiée !", parent=self.root)
#             self.charger_categories()
#             self.reinitialiser_formulaire()
#         except Exception as e:
#             messagebox.showerror("Erreur", f"Impossible de modifier : {e}", parent=self.root)

#     def supprimer_categorie(self):
#         """Fonction de suppression de la catégorie sélectionnée."""
#         selection = self.tableau.selection()
#         if not selection:
#             return
            
#         valeurs = self.tableau.item(selection[0], 'values')
#         cat_id = valeurs[0]
#         nom = valeurs[1]

#         confirm = messagebox.askyesno(
#             "Confirmation", 
#             f"Voulez-vous vraiment supprimer la catégorie '{nom}' ?\nAttention, cela peut affecter les matériels liés !",
#             parent=self.root
#         )
#         if confirm:
#             try:
#                 CategorieModel.delete_categorie(cat_id)
#                 messagebox.showinfo("Succès", "Catégorie supprimée !", parent=self.root)
#                 self.charger_categories()
#                 self.reinitialiser_formulaire()
#             except Exception as e:
#                 messagebox.showerror("Erreur", f"Impossible de supprimer : {e}", parent=self.root)
        
#     def __init__(self, root, dashboard_parent):
#         """Crée et affiche les informations de la catégorie
#         à l'intérieur de la fenêtre initiale donnée.
#         """
#         self.dashboard_parent = dashboard_parent
#         self.root = root
#         self.root.title("Catégories")
#         self.root.geometry("650x420")
        
#         def retour_dashboard_window():
#             self.root.destroy()
#             self.dashboard_parent.root.deiconify()
            
#         tk.Label(
#             root,
#             text="Informations des catégories",
#             font=("Arial", 12, "bold")
#         ).pack(pady=10)
        
#         # --- CONTENEUR CENTRAL ---
#         conteneur_central = tk.Frame(root)
#         conteneur_central.pack(fill="both", expand=True, padx=10)
        
#         # --- ZONE FORMULAIRE (À GAUCHE) ---
#         zone_formulaire = tk.Frame(conteneur_central, width=200)
#         zone_formulaire.pack(side=tk.LEFT, fill="y", padx=10, pady=10)
#         zone_formulaire.pack_propagate(False)
        
#         tk.Label(zone_formulaire, text="Ajout/Modification", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0,10))
        
#         tk.Label(zone_formulaire, text="Nom :").pack(anchor="w")
#         self.entry_nom = tk.Entry(zone_formulaire)
#         self.entry_nom.pack(fill="x", pady=5)
        
#         # Bouton Ajouter
#         btn_ajouter = tk.Button(
#             zone_formulaire, text="Ajouter", 
#             bg="#28A745", fg="white", font=("Arial", 9, "bold"),
#             command=self.ajouter_categorie
#         )
#         btn_ajouter.pack(fill="x", pady=5)

#         # Bouton Modifier
#         btn_modifier = tk.Button(
#             zone_formulaire, 
#             text="Modifier", bg="#007ACC", fg="white", font=("Arial", 9, "bold"),
#             command=self.modifier_categorie,
#         )
#         btn_modifier.pack(fill="x", pady=5)

#         # Bouton Supprimer
#         btn_supprimer = tk.Button(
#             zone_formulaire, 
#             text="Supprimer", bg="#DC3545", fg="white", font=("Arial", 9, "bold"),
#             command=self.supprimer_categorie,
#         )
#         btn_supprimer.pack(fill="x", pady=5)
        
#         # Bouton Vider la sélection
#         btn_annuler = tk.Button(
#             zone_formulaire, text="Vider la sélection",
#             command=self.reinitialiser_formulaire,
#             font=("Arial", 9), pady=2, cursor="hand2"
#         )
#         btn_annuler.pack(fill="x", pady=(15, 0))
        
#         # --- ZONE TABLEAU (À DROITE) ---
#         zone_tableau = tk.Frame(conteneur_central)
#         zone_tableau.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        
#         # Structure du tableau rattachée à zone_tableau
#         colonnes = ('id', 'nom')
#         self.tableau = ttk.Treeview(zone_tableau, columns=colonnes, show='headings')
        
#         # En-tête visible
#         self.tableau.heading('nom', text='Nom')
#         self.tableau.heading('description', text='Description')  # Même si on masque la colonne, il faut définir l'en-tête pour éviter les erreurs
        
#         # Positionnement dans le conteneur de droite
#         self.tableau.pack(fill='both', expand=True)
        
#         # Configuration des tailles (Masquage de la colonne ID à 0px)
#         self.tableau.column('id', width=0, minwidth=0, stretch=False)
#         self.tableau.column('nom', width=150)
#         self.tableau.column('description', width=200)  # Ajout de la colonne description
#         self.tableau.bind('<<TreeviewSelect>>', self.sur_selection_ligne)
        
#         # --- ZONE DES BOUTONS EN BAS ---
#         zone_boutons = tk.Frame(root)
#         zone_boutons.pack(side=tk.BOTTOM, pady=15)
        
#         btn_retour = tk.Button(
#             zone_boutons, 
#             text="Retour", 
#             command=retour_dashboard_window,
#             padx=20
#         )
#         btn_retour.pack()
        
#         self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)
        
#         # Chargement initial des données
#         self.charger_categories()