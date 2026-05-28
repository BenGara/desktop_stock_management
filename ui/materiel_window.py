"""Module de l'interface utilisateur pour la fenêtre de gestion des matériels."""

import tkinter as tk
from tkinter import ttk, messagebox
from services.materiel_service import MaterielService

class MaterielWindow:
    """Affiche les informations des matériels et permet de gérer les matériels du stock."""

    def charger_materiels(self):
        """Récupère les matériels nettoyés du service et les insère dans le Treeview."""
        try:
            liste_materiels = MaterielService.obtenir_tous_materiels()
            
            for item in self.tableau.get_children():
                self.tableau.delete(item)
                
            for materiel in liste_materiels:
                self.tableau.insert('', tk.END, values=materiel)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les matériels : {e}", parent=self.root)
    
    def ajouter_materiel(self):
        """Affiche une boîte de dialogue pour ajouter un nouveau matériel."""
        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un matériel")
        popup.geometry("380x480")
        popup.grab_set()
        
        tk.Label(popup, text="Ajouter un nouveau matériel", font=("Arial", 12, "bold")).pack(pady=15)
        
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")
        
        # --- CHAMPS FORMULAIRE ---
        tk.Label(form_frame, text="Nom du matériel :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Numéro de série :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_serial = tk.Entry(form_frame)
        entry_serial.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Catégorie :", anchor="w").pack(fill="x", pady=(5, 0))
        try:
            dict_cats = MaterielService.obtenir_categories_formulaire()
            liste_categories = list(dict_cats.keys())
        except Exception:
            liste_categories = []
        combo_cat = ttk.Combobox(form_frame, values=liste_categories, state="readonly")
        if liste_categories:
            combo_cat.current(0)
        combo_cat.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Quantité :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_quantite = tk.Entry(form_frame)
        entry_quantite.insert(0, "1")
        entry_quantite.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Statut :", anchor="w").pack(fill="x", pady=(5, 0))
        liste_statuts = ["En stock", "Affecté", "En panne", "Hors service"]
        combo_statut = ttk.Combobox(form_frame, values=liste_statuts, state="readonly")
        combo_statut.current(0)
        combo_statut.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Date d'achat (AAAA-MM-JJ) :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_date = tk.Entry(form_frame)
        entry_date.pack(fill="x", pady=2)

        def valider_et_enregistrer():
            try:
                MaterielService.ajouter_materiel(
                    entry_nom.get(),
                    entry_serial.get(),
                    combo_cat.get(),
                    entry_quantite.get(),
                    combo_statut.get(),
                    entry_date.get()
                )
                messagebox.showinfo("Succès", "Le matériel a été ajouté avec succès !", parent=popup)
                self.charger_materiels()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie non valide", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur système", f"Erreur lors de l'enregistrement : {e}", parent=popup)

        btn_enregistrer = tk.Button(
            popup, text="Enregistrer", command=valider_et_enregistrer,
            bg="#28A745", fg="white", font=("Arial", 10, "bold")
        )
        btn_enregistrer.pack(pady=20)
        
    def modifier_materiel(self):
        """Ouvre un popup pré-rempli pour modifier l'équipement sélectionné."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un matériel à modifier.", parent=self.root)
            return

        # Récupération des valeurs existantes dans la ligne sélectionnée
        valeurs = self.tableau.item(selection[0], 'values')
        mat_id, nom_actuel, serial_actuel, cat_actuelle, qte_actuelle, statut_actuel, date_actuelle = valeurs

        popup = tk.Toplevel(self.root)
        popup.title("Modifier un matériel")
        popup.geometry("380x480")
        popup.grab_set()
        
        tk.Label(popup, text="Modifier le matériel", font=("Arial", 12, "bold")).pack(pady=15)
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")
        
        # --- CHAMPS PRE-REMPLIS ---
        tk.Label(form_frame, text="Nom du matériel :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.insert(0, nom_actuel)
        entry_nom.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Numéro de série :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_serial = tk.Entry(form_frame)
        entry_serial.insert(0, serial_actuel)
        entry_serial.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Catégorie :", anchor="w").pack(fill="x", pady=(5, 0))
        try:
            dict_cats = MaterielService.obtenir_categories_formulaire()
            liste_categories = list(dict_cats.keys())
        except Exception:
            liste_categories = []
        combo_cat = ttk.Combobox(form_frame, values=liste_categories, state="readonly")
        combo_cat.pack(fill="x", pady=2)
        if cat_actuelle in liste_categories:
            combo_cat.set(cat_actuelle)
        elif liste_categories:
            combo_cat.current(0)
            
        tk.Label(form_frame, text="Quantité :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_quantite = tk.Entry(form_frame)
        entry_quantite.insert(0, qte_actuelle)
        entry_quantite.pack(fill="x", pady=2)
        
        tk.Label(form_frame, text="Statut :", anchor="w").pack(fill="x", pady=(5, 0))
        liste_statuts = ["En stock", "Affecté", "En panne", "Hors service"]
        combo_statut = ttk.Combobox(form_frame, values=liste_statuts, state="readonly")
        combo_statut.pack(fill="x", pady=2)
        if statut_actuel in liste_statuts:
            combo_statut.set(statut_actuel)
        else:
            combo_statut.current(0)
            
        tk.Label(form_frame, text="Date d'achat (AAAA-MM-JJ) :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_date = tk.Entry(form_frame)
        entry_date.insert(0, date_actuelle if date_actuelle != "Non renseignée" else "")
        entry_date.pack(fill="x", pady=2)

        def valider_modification():
            try:
                MaterielService.modifier_materiel(
                    mat_id,
                    entry_nom.get(),
                    entry_serial.get(),
                    combo_cat.get(),
                    entry_quantite.get(),
                    combo_statut.get(),
                    entry_date.get()
                )
                messagebox.showinfo("Succès", "Le matériel a été modifié avec succès !", parent=popup)
                self.charger_materiels()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie non valide", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur système", f"Erreur lors de la modification : {e}", parent=popup)

        btn_modifier = tk.Button(
            popup, text="Enregistrer les modifications", command=valider_modification,
            bg="#007ACC", fg="white", font=("Arial", 10, "bold")
        )
        btn_modifier.pack(pady=20)

    def supprimer_materiel(self):
        """Supprime définitivement le matériel sélectionné après validation."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un matériel à supprimer.", parent=self.root)
            return
            
        valeurs = self.tableau.item(selection[0], 'values')
        mat_id, nom, serial, _, _, _, _ = valeurs
        
        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer définitivement le matériel '{nom}' (S/N: {serial}) ?",
            parent=self.root
        )
        
        if confirm:
            try:
                MaterielService.supprimer_materiel(mat_id)
                messagebox.showinfo("Succès", "Le matériel a bien été retiré de l'inventaire.", parent=self.root)
                self.charger_materiels()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Initialise la fenêtre graphique pour la liste du matériel."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Gestion des Matériels")
        self.root.geometry("850x480")

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        tk.Label(root, text="Inventaire des Matériels Informatiques", font=("Arial", 14, "bold")).pack(pady=10)

        # Structure du tableau Treeview (S'aligne sur les colonnes renvoyées par le service)
        colonnes = ('id', 'nom', 'serial', 'categorie', 'quantite', 'statut', 'date_achat')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
        self.tableau.heading('nom', text='Nom du matériel')
        self.tableau.heading('serial', text='N° de Série')
        self.tableau.heading('categorie', text='Catégorie')
        self.tableau.heading('quantite', text='Quantité')
        self.tableau.heading('statut', text='Statut')
        self.tableau.heading('date_achat', text="Date d'achat")
        
        self.tableau.column('id', width=0, minwidth=0, stretch=False)  # Masqué
        self.tableau.column('nom', width=150)
        self.tableau.column('serial', width=120)
        self.tableau.column('categorie', width=120)
        self.tableau.column('quantite', width=80, anchor="center")
        self.tableau.column('statut', width=110, anchor="center")
        self.tableau.column('date_achat', width=110, anchor="center")
        
        self.tableau.pack(fill="both", expand=True, padx=20, pady=10)

        # Barre d'actions (Boutons inférieurs)
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(fill="x", side=tk.BOTTOM, pady=20)

        btn_ajouter = tk.Button(
            zone_boutons, text="Ajouter", command=self.ajouter_materiel,
            bg="#28A745", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_ajouter.pack(side=tk.LEFT, padx=10)
        
        btn_modifier = tk.Button(
            zone_boutons, text="Modifier", command=self.modifier_materiel,
            bg="#007ACC", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_modifier.pack(side=tk.LEFT, padx=10)

        btn_supprimer = tk.Button(
            zone_boutons, text="Supprimer", command=self.supprimer_materiel,
            bg="#DC3545", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_supprimer.pack(side=tk.LEFT, padx=10)

        btn_retour = tk.Button(zone_boutons, text="Retour", command=retour_dashboard_window, padx=20)
        btn_retour.pack(side=tk.RIGHT, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        self.charger_materiels()