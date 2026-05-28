"""Module de l'interface utilisateur pour la fenêtre de gestion des catégories."""

import tkinter as tk
from tkinter import ttk, messagebox
from services.categorie_service import CategorieService

class CategorieWindow:
    """Affiche les catégories de matériel et permet leur gestion complète."""

    def charger_categories(self):
        """Met à jour le Treeview avec les données nettoyées du service."""
        try:
            liste_categories = CategorieService.obtenir_toutes_categories()

            for item in self.tableau.get_children():
                self.tableau.delete(item)

            for cat in liste_categories:
                self.tableau.insert('', tk.END, values=cat)

            self.reinitialiser_formulaire()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les catégories : {e}", parent=self.root)

    def reinitialiser_formulaire(self):
        """Vide les champs et remet le formulaire en mode 'Ajout'."""
        self.id_selectionne = None
        self.entry_nom.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.lbl_form_title.config(text="Nouvelle Catégorie", fg="black")
        self.btn_enregistrer.config(state=tk.NORMAL)
        self.btn_modifier.config(state=tk.DISABLED)

    def remplir_formulaire_depuis_selection(self, event):
        """Pré-remplit les champs de gauche quand on clique sur une ligne du tableau."""
        selection = self.tableau.selection()
        if not selection:
            return

        valeurs = self.tableau.item(selection[0], 'values')
        self.id_selectionne, nom, description = valeurs

        # Remplissage des champs
        self.entry_nom.delete(0, tk.END)
        self.entry_nom.insert(0, nom)

        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, description)

        # Basculer le titre et l'activation des boutons à gauche
        self.lbl_form_title.config(text="Modifier la Catégorie", fg="#007ACC")
        self.btn_enregistrer.config(state=tk.DISABLED)
        self.btn_modifier.config(state=tk.NORMAL)

    def valider_et_ajouter(self):
        """Prend les valeurs de gauche et appelle le service pour l'ajout."""
        nom = self.entry_nom.get()
        desc = self.entry_desc.get()

        try:
            CategorieService.ajouter_categorie(nom, desc)
            messagebox.showinfo("Succès", f"La catégorie '{nom.strip()}' a été créée !", parent=self.root)
            self.charger_categories()
        except ValueError as ve:
            messagebox.showwarning("Saisie incomplète", str(ve), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erreur BDD", f"Impossible d'ajouter la catégorie : {e}", parent=self.root)

    def valider_et_modifier(self):
        """Prend les valeurs de gauche et appelle le service pour appliquer la modification."""
        if not self.id_selectionne:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une catégorie dans le tableau.", parent=self.root)
            return

        nom = self.entry_nom.get()
        desc = self.entry_desc.get()

        try:
            CategorieService.modifier_categorie(self.id_selectionne, nom, desc)
            messagebox.showinfo("Succès", "La catégorie a été mise à jour !", parent=self.root)
            self.charger_categories()
        except ValueError as ve:
            messagebox.showwarning("Saisie incomplète", str(ve), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erreur BDD", f"Impossible de modifier la catégorie : {e}", parent=self.root)

    def suppression_categorie(self):
        """Supprime la catégorie sélectionnée dans le tableau après confirmation."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une catégorie dans le tableau.", parent=self.root)
            return

        valeurs = self.tableau.item(selection[0], 'values')
        category_id, nom, _ = valeurs

        confirm = messagebox.askyesno(
            "Confirmation de suppression", 
            f"Voulez-vous vraiment supprimer définitivement la catégorie '{nom}' ?\n"
            f"(Attention : cela peut impacter les matériels liés à cette catégorie)",
            parent=self.root
        )
        
        if confirm:
            try:
                CategorieService.supprimer_categorie(category_id)
                messagebox.showinfo("Succès", "La catégorie a bien été supprimée !", parent=self.root)
                self.charger_categories()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer la catégorie : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Initialise la fenêtre avec le formulaire à gauche et le tableau à droite."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Gestion des Catégories")
        self.root.geometry("850x450")
        self.id_selectionne = None

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        # Titre Principal
        tk.Label(root, text="Gestion des Catégories de Matériel", font=("Arial", 14, "bold")).pack(pady=10)

        # Zone Centrale divisée en 2 (Gauche = Formulaire, Droite = Tableau)
        zone_centrale = tk.Frame(root)
        zone_centrale.pack(fill="both", expand=True, padx=20, pady=5)

        # =====================================================================
        # CÔTÉ GAUCHE : FORMULAIRE D'AJOUT ET MODIFICATION
        # =====================================================================
        frame_gauche = tk.LabelFrame(zone_centrale, text=" Formulaire ", padx=15, pady=15)
        frame_gauche.pack(side=tk.LEFT, fill="y", padx=(0, 15))

        self.lbl_form_title = tk.Label(frame_gauche, text="Nouvelle Catégorie", font=("Arial", 11, "bold"))
        self.lbl_form_title.pack(anchor="w", pady=(0, 10))

        tk.Label(frame_gauche, text="Nom de la catégorie :", anchor="w").pack(fill="x", pady=(5, 0))
        self.entry_nom = tk.Entry(frame_gauche, width=25)
        self.entry_nom.pack(fill="x", pady=2)

        tk.Label(frame_gauche, text="Description :", anchor="w").pack(fill="x", pady=(5, 0))
        self.entry_desc = tk.Entry(frame_gauche, width=25)
        self.entry_desc.pack(fill="x", pady=2)

        # Boutons d'action du formulaire (Placés juste en dessous des champs à gauche)
        self.btn_enregistrer = tk.Button(
            frame_gauche, text="Enregistrer (Ajout)", command=self.valider_et_ajouter,
            bg="#28A745", fg="white", font=("Arial", 9, "bold"), cursor="hand2"
        )
        self.btn_enregistrer.pack(fill="x", pady=(15, 5))

        self.btn_modifier = tk.Button(
            frame_gauche, text="Enregistrer (Modif)", command=self.valider_et_modifier,
            bg="#007ACC", fg="white", font=("Arial", 9, "bold"), cursor="hand2", state=tk.DISABLED
        )
        self.btn_modifier.pack(fill="x", pady=5)
        
        btn_raz = tk.Button(
            frame_gauche, text="Vider / Annuler", command=self.reinitialiser_formulaire,
            bg="#6C757D", fg="white", font=("Arial", 9)
        )
        btn_raz.pack(fill="x", pady=(5, 0))

        # =====================================================================
        # CÔTÉ DROIT : LE TABLEAU (TREEVIEW)
        # =====================================================================
        frame_droit = tk.Frame(zone_centrale)
        frame_droit.pack(side=tk.RIGHT, fill="both", expand=True)

        colonnes = ('id', 'nom', 'description')
        self.tableau = ttk.Treeview(frame_droit, columns=colonnes, show='headings')
        
        self.tableau.heading('nom', text='Nom de la catégorie')
        self.tableau.heading('description', text='Description')
        
        self.tableau.column('id', width=0, minwidth=0, stretch=False)  # ID masqué
        self.tableau.column('nom', width=150)
        self.tableau.column('description', width=300)
        
        self.tableau.pack(fill="both", expand=True)

        # Événement : Quand on clique sur une ligne du tableau, on remplit le formulaire de gauche
        self.tableau.bind("<<TreeviewSelect>>", self.remplir_formulaire_depuis_selection)

        # =====================================================================
        # ZONE INFERIEURE : LES BOUTONS EN BAS
        # =====================================================================
        zone_boutons_bas = tk.Frame(root)
        zone_boutons_bas.pack(fill="x", side=tk.BOTTOM, pady=15, padx=20)

        # Le bouton Supprimer reste en bas à gauche
        btn_supprimer = tk.Button(
            zone_boutons_bas, text="Supprimer la sélection", command=self.suppression_categorie,
            bg="#DC3545", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_supprimer.pack(side=tk.LEFT)

        # Le bouton Retour reste en bas à droite
        btn_retour = tk.Button(zone_boutons_bas, text="Retour", command=retour_dashboard_window, padx=20, pady=5)
        btn_retour.pack(side=tk.RIGHT)

        # Interception de la croix rouge de fermeture du système
        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        # Chargement initial des données
        self.charger_categories()