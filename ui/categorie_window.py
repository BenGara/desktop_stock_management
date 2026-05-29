# -*- coding: utf-8 -*-
"""Module de l'interface utilisateur pour la fenêtre de gestion des catégories."""

import tkinter as tk
from tkinter import ttk, messagebox

from services.categorie_service import CategorieService
from services.session_service import SessionService
from services.permission_service import PermissionService


class CategorieWindow:
    """Affiche les catégories de matériel et permet leur gestion filtrée par rôle."""

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
        if PermissionService.peut(self._role, "ajouter_categorie"):
            self.btn_enregistrer.config(state=tk.NORMAL)
        self.btn_modifier.config(state=tk.DISABLED)

    def remplir_formulaire_depuis_selection(self, event):
        """Pré-remplit les champs de gauche quand on clique sur une ligne."""
        selection = self.tableau.selection()
        if not selection:
            return
        valeurs = self.tableau.item(selection[0], 'values')
        self.id_selectionne, nom, description = valeurs
        self.entry_nom.delete(0, tk.END)
        self.entry_nom.insert(0, nom)
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, description)
        self.lbl_form_title.config(text="Modifier la Catégorie", fg="#007ACC")
        self.btn_enregistrer.config(state=tk.DISABLED)
        if PermissionService.peut(self._role, "modifier_categorie"):
            self.btn_modifier.config(state=tk.NORMAL)

    def valider_et_ajouter(self):
        if not PermissionService.peut(self._role, "ajouter_categorie"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour ajouter une catégorie.")
            return
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
        if not PermissionService.peut(self._role, "modifier_categorie"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour modifier une catégorie.")
            return
        if not self.id_selectionne:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une catégorie.", parent=self.root)
            return
        nom = self.entry_nom.get()
        desc = self.entry_desc.get()
        try:
            CategorieService.modifier_categorie(self.id_selectionne, nom, desc)
            messagebox.showinfo("Succès", f"La catégorie '{nom.strip()}' a été mise à jour !", parent=self.root)
            self.charger_categories()
        except ValueError as ve:
            messagebox.showwarning("Saisie incomplète", str(ve), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erreur BDD", f"Impossible de modifier la catégorie : {e}", parent=self.root)

    def supprimer_categorie(self):
        if not PermissionService.peut(self._role, "supprimer_categorie"):
            messagebox.showwarning("Accès refusé", "Seul un administrateur peut supprimer une catégorie.")
            return
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une catégorie.", parent=self.root)
            return
        valeurs = self.tableau.item(selection[0], 'values')
        cat_id, nom, _ = valeurs
        confirm = messagebox.askyesno(
            "Confirmation", f"Supprimer définitivement la catégorie '{nom}' ?", parent=self.root
        )
        if confirm:
            try:
                CategorieService.supprimer_categorie(cat_id)
                messagebox.showinfo("Succès", "Catégorie supprimée.", parent=self.root)
                self.charger_categories()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Initialise la fenêtre de gestion des catégories."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self._role = SessionService.role()
        self.id_selectionne = None

        self.root.title("Gestion des Catégories")
        self.root.geometry("720x450")
        self.root.configure(bg="#F8F9FA")

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            self.dashboard_parent.refresh()

        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        tk.Label(
            root, text="Gestion des Catégories de Matériel",
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=(15, 5), anchor="w", padx=20)

        # Conteneur principal : formulaire à gauche, tableau à droite
        main_frame = tk.Frame(root, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Formulaire gauche
        form_frame = tk.LabelFrame(main_frame, text=" Formulaire ", bg="#F8F9FA",
                                   font=("Arial", 9, "bold"), padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill="y", padx=(0, 15))

        self.lbl_form_title = tk.Label(form_frame, text="Nouvelle Catégorie",
                                       font=("Arial", 10, "bold"), bg="#F8F9FA")
        self.lbl_form_title.pack(anchor="w", pady=(0, 8))

        tk.Label(form_frame, text="Nom :", bg="#F8F9FA", anchor="w").pack(fill="x")
        self.entry_nom = tk.Entry(form_frame, font=("Arial", 10))
        self.entry_nom.pack(fill="x", pady=(2, 8))

        tk.Label(form_frame, text="Description :", bg="#F8F9FA", anchor="w").pack(fill="x")
        self.entry_desc = tk.Entry(form_frame, font=("Arial", 10))
        self.entry_desc.pack(fill="x", pady=(2, 15))

        style_btn = {"font": ("Arial", 9, "bold"), "fg": "white",
                     "relief": "flat", "pady": 6, "cursor": "hand2"}

        self.btn_enregistrer = tk.Button(
            form_frame, text="Enregistrer", command=self.valider_et_ajouter,
            bg="#27AE60", **style_btn
        )
        if not PermissionService.peut(self._role, "ajouter_categorie"):
            self.btn_enregistrer.config(state=tk.DISABLED)
        self.btn_enregistrer.pack(fill="x", pady=3)

        self.btn_modifier = tk.Button(
            form_frame, text="Modifier", command=self.valider_et_modifier,
            bg="#2980B9", state=tk.DISABLED, **style_btn
        )
        self.btn_modifier.pack(fill="x", pady=3)

        if PermissionService.peut(self._role, "supprimer_categorie"):
            tk.Button(
                form_frame, text="Supprimer", command=self.supprimer_categorie,
                bg="#C0392B", **style_btn
            ).pack(fill="x", pady=3)

        tk.Button(
            form_frame, text="Réinitialiser", command=self.reinitialiser_formulaire,
            bg="#7F8C8D", **style_btn
        ).pack(fill="x", pady=(15, 3))

        tk.Button(
            form_frame, text="Retour", command=retour_dashboard_window,
            bg="#95A5A6", **style_btn
        ).pack(fill="x", pady=3)

        # Tableau droite
        colonnes = ('id', 'nom', 'description')
        self.tableau = ttk.Treeview(main_frame, columns=colonnes, show='headings', selectmode="browse")
        self.tableau.heading('nom', text='Nom de la catégorie')
        self.tableau.heading('description', text='Description')
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom', width=200)
        self.tableau.column('description', width=300)
        self.tableau.pack(side=tk.LEFT, fill="both", expand=True)

        self.tableau.bind("<<TreeviewSelect>>", self.remplir_formulaire_depuis_selection)

        self.charger_categories()
