"""Module de l'interface utilisateur pour la fenêtre de gestion des catégories."""

from logging import root
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
        self.root.title("Gestion des Catégories de Matériel")
        self.root.geometry("800x450")
        self.root.configure(bg="#F8F9FA")
        self.id_selectionne = None

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        # Titre général stylisé
        tk.Label(
            root, text="Catégories de Matériels", 
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=(15, 10), anchor="w", padx=20)
        
        # Zone Centrale divisée en 2 (Gauche = Formulaire, Droite = Tableau)
        zone_centrale = tk.Frame(root)
        zone_centrale.pack(fill="both", expand=True, padx=20, pady=5)

        # =====================================================================
        # CÔTÉ GAUCHE : FORMULAIRE DE TYPE CARTE (Card effect)
        # =====================================================================
        # frame_gauche devient zone_gauche pour correspondre au design épuré
        zone_gauche = tk.Frame(zone_centrale, bg="white", bd=1, relief="groove", padx=15, pady=15, width=260)
        zone_gauche.pack(side=tk.LEFT, fill="both", padx=(0, 10), expand=False)        
        zone_gauche.pack_propagate(False)

        self.lbl_form_title = tk.Label(zone_gauche, text="Nouvelle Catégorie", font=("Arial", 11, "bold"), bg="white", fg="#2C3E50")
        self.lbl_form_title.pack(anchor="w", pady=(0, 15))

        # Dictionnaires de styles partagés
        style_label = {"bg": "white", "fg": "#7F8C8D", "font": ("Arial", 9, "bold")}
        style_entry = {"font": ("Arial", 10), "bg": "#F8F9FA", "highlightthickness": 1, "highlightbackground": "#BDC3C7", "relief": "flat"}
        style_action_btn = {"font": ("Arial", 9, "bold"), "fg": "white", "relief": "flat", "pady": 6, "cursor": "hand2"}

        tk.Label(zone_gauche, text="Nom de la catégorie", **style_label).pack(anchor="w")
        self.entry_nom = tk.Entry(zone_gauche, **style_entry)
        self.entry_nom.pack(fill="x", pady=(2, 12), ipady=3)

        tk.Label(zone_gauche, text="Description complète", **style_label).pack(anchor="w")
        self.entry_desc = tk.Entry(zone_gauche, **style_entry)
        self.entry_desc.pack(fill="x", pady=(2, 20), ipady=3)

        # Boutons du formulaire avec les commandes d'origine du Code 1
        self.btn_enregistrer = tk.Button(zone_gauche, text="Créer", command=self.valider_et_ajouter, bg="#27AE60", **style_action_btn)
        self.btn_enregistrer.pack(fill="x", pady=4)

        self.btn_modifier = tk.Button(zone_gauche, text="Enregistrer", command=self.valider_et_modifier, bg="#2980B9", **style_action_btn, state=tk.DISABLED)
        self.btn_modifier.pack(fill="x", pady=4)

        btn_raz = tk.Button(zone_gauche, text="Réinitialiser", command=self.reinitialiser_formulaire, bg="#7F8C8D", **style_action_btn)
        btn_raz.pack(fill="x", pady=(15, 0))
        

        # =====================================================================
        # CÔTÉ DROIT : LE TABLEAU (TREEVIEW)
        # =====================================================================
        frame_droit = tk.Frame(zone_centrale)
        frame_droit.pack(side=tk.RIGHT, fill="both", expand=True)

        colonnes = ('id', 'nom', 'description')
        self.tableau = ttk.Treeview(frame_droit, columns=colonnes, show='headings', selectmode="browse")
        
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
        zone_boutons_bas = tk.Frame(root, bg="#F8F9FA")
        zone_boutons_bas.pack(fill="x", side=tk.BOTTOM, pady=(0, 15), padx=20)

        btn_supprimer = tk.Button(
            zone_boutons_bas, text="Supprimer", command=self.suppression_categorie,
            bg="#C0392B", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_supprimer.pack(side=tk.LEFT)

        btn_retour = tk.Button(
            zone_boutons_bas, text="Retour", command=retour_dashboard_window,
            bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_retour.pack(side=tk.RIGHT)
        
        # Interception de la croix rouge de fermeture du système
        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        # Chargement initial des données
        self.charger_categories()