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
    
    def ajouter_materiel(self):
        """Affiche une boîte de dialogue pour ajouter un nouveau matériel."""
        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un matériel")
        popup.geometry("350x400")
        popup.grab_set()  # Empêche d'interagir avec la fenêtre principale tant que le popup est ouvert
        
        # Titre du formulaire
        tk.Label(popup, text="Ajouter un nouveau matériel", font=("Arial", 12, "bold")).pack(pady=15)
        
        # Conteneur centré pour aligner les labels et les champs de saisie
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")
        
        # Champ Nom
        tk.Label(form_frame, text="Nom : ", anchor='w').pack(anchor='w', pady=(5,0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.pack(fill="x", pady=2)
        
        # Champ Numéro de série
        tk.Label(form_frame, text="Numéro de série : ", anchor='w').pack(anchor='w', pady=(5,0))
        entry_serial = tk.Entry(form_frame)
        entry_serial.pack(fill="x", pady=2)
        
        # Champ Catégorie
        tk.Label(form_frame, text="Catégorie : ", anchor='w').pack(anchor='w', pady=(5,0))
        
        categories = MaterialModel.get_all_categories_names()  # Récupère les noms des catégories pour les afficher dans la Combobox
        entry_categorie = ttk.Combobox(form_frame, values=categories, state="readonly")
        entry_categorie.current(0)  # Sélectionne la première catégorie par défaut
        entry_categorie.pack(fill="x", pady=2)
        
        # Champ Quantité
        tk.Label(form_frame, text="Quantité :").pack(anchor="w")

        # On définit des bornes (ex: de 0 à 10000)
        self.entry_quantite = ttk.Spinbox(form_frame, from_=0, to=10000, increment=1)
        self.entry_quantite.pack(fill="x", pady=5)        
        # Champ Status
        tk.Label(form_frame, text="Status : ", anchor='w').pack(anchor='w', pady=(5,0))
        entry_status = tk.Entry(form_frame)
        entry_status.pack(fill="x", pady=2)

        # Champ Date d'achat
        tk.Label(form_frame, text="Date d'achat (YYYY-MM-DD) : ", anchor='w').pack(anchor='w', pady=(5,0))
        entry_date_achat = tk.Entry(form_frame)
        entry_date_achat.pack(fill="x", pady=2)

        # Bouton pour soumettre le formulaire
        tk.Button(popup, text="Ajouter", command=lambda: self.soumettre_ajout(entry_nom.get(), entry_serial.get(), entry_categorie.get(), entry_quantite.get(), entry_date_achat.get())).pack(pady=20)

    def soumettre_ajout(self, nom, serial_number, categorie, quantite, date_achat):
        """Soumet les informations du nouveau matériel au modèle."""
        try:
            MaterialModel.create_material(nom, serial_number, categorie, quantite, date_achat)
            self.charger_materiels()
            messagebox.showinfo("Ajouter", "Le matériel a été ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Ajouter", f"Erreur lors de l'ajout du matériel : {e}")

    def modifier_materiel(self):
        """Affiche une boîte de dialogue pour modifier un matériel existant."""
        messagebox.showinfo("Modifier", "Fonction de modification à implémenter")

    def supprimer_materiel(self):
        """Affiche une boîte de dialogue pour supprimer un matériel existant."""
        selected_item = self.tableau.selection()
        if not selected_item:
            messagebox.showwarning("Supprimer", "Veuillez sélectionner un matériel à supprimer.")
            return
        values = self.tableau.item(selected_item[0])['values']
        material_id = values[0]  # Supposant que l'ID est dans la première colonne
        material_name = values[1]  # Supposant que le nom est dans la deuxième colonne
        materiel_serial_number = values[2]  # Supposant que le numéro de série est dans la troisième colonne
        
        confirm = messagebox.askyesno("Supprimer", f"Êtes-vous sûr de vouloir supprimer le matériel '{material_name}' (N° de série: {materiel_serial_number}) ?")
        
        if confirm:
            try:
                MaterialModel.delete_material(material_id)
                self.charger_materiels()
                messagebox.showinfo("Supprimer", f"Le matériel '{material_name}' a été supprimé avec succès.")
            except Exception as e:
                messagebox.showerror("Supprimer", f"Erreur lors de la suppression du matériel : {e}")
        

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
            text="Informations des matériels",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        #tableau d'affichage des matériels
        colonnes = ('id', 'nom', 'numéro de série', 'catégorie', 'quantité', 'status', 'date d\'achat')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
        # En-têtes (Uniquement pour les colonnes que l'on VEUT voir)
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('numéro de série', text='Numéro de Série')
        self.tableau.heading('catégorie', text='Catégorie')
        self.tableau.heading('quantité', text='Quantité')
        self.tableau.heading('status', text='Status')
        self.tableau.heading('date d\'achat', text='Date d\'achat')
        
        # Affichage du tableau
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Configuration des tailles de TOUTES les colonnes
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom', width=100)
        self.tableau.column('numéro de série', width=100)
        self.tableau.column('catégorie', width=100)
        self.tableau.column('quantité', width=80)
        self.tableau.column('status', width=100)
        self.tableau.column('date d\'achat', width=100)
        
        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(pady=10)
        
        # Bouton ajouter un matériel
        btn_ajouter = tk.Button(
            zone_boutons, 
            text="Ajouter", 
            command=self.ajouter_materiel,
            bg="#28A745",
            fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
        )
        btn_ajouter.pack(side=tk.LEFT, padx=10)
        
        # Bonton modifier un matériel
        btn_modifier = tk.Button(
            zone_boutons, 
            text="Modifier", 
            command=self.modifier_materiel,
            bg="#007ACC",
            fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
        )
        btn_modifier.pack(side=tk.LEFT, padx=10)

        # Bouton supprimer un matériel
        btn_supprimer = tk.Button(
            zone_boutons, 
            text="Supprimer", 
            command=self.supprimer_materiel,
            bg="#DC3545",
            fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
        )
        btn_supprimer.pack(side=tk.LEFT, padx=10)

        # Bouton de retour
        btn_retour = tk.Button(
            zone_boutons, 
            text="Retour", 
            command=retour_dashboard_window,
            font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
        )
        btn_retour.pack(side=tk.LEFT, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        self.charger_materiels()