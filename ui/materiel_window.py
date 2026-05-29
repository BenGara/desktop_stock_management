"""Module de l'interface utilisateur pour la fenêtre de gestion des matériels."""

import tkinter as tk
from tkinter import ttk, messagebox

from services.materiel_service import MaterielService
from services.session_service import SessionService
from services.permission_service import PermissionService


class MaterielWindow:
    """Affiche l'inventaire des matériels — actions filtrées selon le rôle."""

    def charger_materiels(self):
        """Récupère les matériels du service et les insère dans le Treeview."""
        try:
            liste_materiels = MaterielService.obtenir_tous_materiels()
            for item in self.tableau.get_children():
                self.tableau.delete(item)
            for materiel in liste_materiels:
                self.tableau.insert('', tk.END, values=materiel)
        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de charger les matériels : {e}", parent=self.root
            )

    def ajouter_materiel(self):
        """Affiche une boîte de dialogue pour ajouter un nouveau matériel."""
        if not PermissionService.peut(self._role, "ajouter_materiel"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour ajouter un matériel.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un matériel")
        popup.geometry("380x500")
        popup.configure(bg="#F8F9FA")
        popup.grab_set()

        tk.Label(popup, text="Nouveau Matériel Informatique",
                 font=("Arial", 12, "bold"), bg="#F8F9FA", fg="#2C3E50").pack(pady=15)

        form_frame = tk.Frame(popup, bg="#F8F9FA")
        form_frame.pack(padx=20, fill="x")

        style_label = {"bg": "#F8F9FA", "fg": "#7F8C8D", "font": ("Arial", 9, "bold")}
        style_entry = {"font": ("Arial", 10), "bg": "white",
                       "highlightthickness": 1, "highlightbackground": "#BDC3C7", "relief": "flat"}

        tk.Label(form_frame, text="Nom du matériel", **style_label).pack(anchor="w")
        entry_nom = tk.Entry(form_frame, **style_entry)
        entry_nom.pack(fill="x", pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Numéro de série", **style_label).pack(anchor="w")
        entry_serial = tk.Entry(form_frame, **style_entry)
        entry_serial.pack(fill="x", pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Catégorie", **style_label).pack(anchor="w")
        try:
            dict_cats = MaterielService.obtenir_categories_formulaire()
            liste_categories = list(dict_cats.keys())
        except Exception:
            liste_categories = []
        combo_cat = ttk.Combobox(form_frame, values=liste_categories, state="readonly")
        combo_cat.pack(fill="x", pady=(2, 8))
        if liste_categories:
            combo_cat.current(0)

        tk.Label(form_frame, text="Quantité", **style_label).pack(anchor="w")
        entry_quantite = tk.Spinbox(form_frame, from_=1, to=1000, increment=1, **style_entry)
        entry_quantite.pack(fill="x", pady=(2, 8), ipady=3)

        def valider_et_enregistrer():
            try:
                MaterielService.ajouter_materiel(
                    entry_nom.get(), entry_serial.get(),
                    combo_cat.get(), entry_quantite.get()
                )
                messagebox.showinfo("Succès", "Le matériel a bien été ajouté !", parent=popup)
                popup.destroy()
                self.charger_materiels()
            except ValueError as e:
                messagebox.showerror("Erreur de saisie", str(e), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}", parent=popup)

        tk.Button(
            popup, text="Enregistrer l'équipement", command=valider_et_enregistrer,
            bg="#27AE60", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(fill="x", padx=20, pady=10, ipady=5)

    def modifier_materiel(self):
        """Ouvre un popup pré-rempli pour modifier l'équipement sélectionné."""
        if not PermissionService.peut(self._role, "modifier_materiel"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour modifier un matériel.")
            return

        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un matériel.", parent=self.root)
            return

        valeurs = self.tableau.item(selection[0], 'values')
        mat_id, nom_actuel, serial_actuel, cat_actuelle, qte_actuelle, statut_actuel, date_actuelle = valeurs

        popup = tk.Toplevel(self.root)
        popup.title("Modifier un matériel")
        popup.geometry("380x520")
        popup.configure(bg="#F8F9FA")
        popup.grab_set()

        tk.Label(popup, text="Modifier le matériel",
                 font=("Arial", 12, "bold"), bg="#F8F9FA", fg="#2C3E50").pack(pady=15)

        form_frame = tk.Frame(popup, bg="#F8F9FA")
        form_frame.pack(padx=20, fill="x")
        style_entry = {"font": ("Arial", 10), "bg": "white",
                       "highlightthickness": 1, "highlightbackground": "#BDC3C7", "relief": "flat"}

        tk.Label(form_frame, text="Nom :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        entry_nom = tk.Entry(form_frame, **style_entry)
        entry_nom.insert(0, nom_actuel)
        entry_nom.pack(fill="x", pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Numéro de série :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 0))
        entry_serial = tk.Entry(form_frame, **style_entry)
        entry_serial.insert(0, serial_actuel)
        entry_serial.pack(fill="x", pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Catégorie", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w")
        try:
            dict_cats = MaterielService.obtenir_categories_formulaire()
            liste_categories = list(dict_cats.keys())
        except Exception:
            liste_categories = []
        combo_cat = ttk.Combobox(form_frame, values=liste_categories, state="readonly")
        combo_cat.pack(fill="x", pady=(2, 8))
        if liste_categories:
            combo_cat.current(0)

        tk.Label(form_frame, text="Quantité :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", fill="x", pady=(5, 0))
        entry_quantite = tk.Entry(form_frame, **style_entry)
        entry_quantite.insert(0, qte_actuelle)
        entry_quantite.pack(fill="x", pady=(2, 8), ipady=3)

        tk.Label(form_frame, text="Statut :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", fill="x", pady=(5, 0))
        combo_statut = ttk.Combobox(form_frame, values=["En stock", "Affecté", "En panne", "Hors service"], state="readonly")
        combo_statut.pack(fill="x", pady=(2, 8))
        if statut_actuel in ["En stock", "Affecté", "En panne", "Hors service"]:
            combo_statut.set(statut_actuel)
        else:
            combo_statut.current(0)

        tk.Label(form_frame, text="Date d'achat (AAAA-MM-JJ) :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", fill="x", pady=(5, 0))
        entry_date = tk.Entry(form_frame, **style_entry)
        entry_date.insert(0, date_actuelle if date_actuelle != "Non renseignée" else "")
        entry_date.pack(fill="x", pady=(2, 8), ipady=3)

        def valider_modification():
            try:
                MaterielService.modifier_materiel(
                    mat_id, entry_nom.get(), entry_serial.get(),
                    combo_cat.get(), entry_quantite.get(),
                    combo_statut.get(), entry_date.get()
                )
                messagebox.showinfo("Succès", "Le matériel a été modifié avec succès !", parent=popup)
                self.charger_materiels()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie non valide", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur système", f"Erreur lors de la modification : {e}", parent=popup)

        tk.Button(
            popup, text="Enregistrer les modifications", command=valider_modification,
            bg="#007ACC", fg="white", font=("Arial", 10, "bold")
        ).pack(pady=20)

    def supprimer_materiel(self):
        """Supprime définitivement le matériel sélectionné après validation."""
        if not PermissionService.peut(self._role, "supprimer_materiel"):
            messagebox.showwarning("Accès refusé", "Seul un administrateur peut supprimer un matériel.")
            return

        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un matériel.", parent=self.root)
            return

        valeurs = self.tableau.item(selection[0], 'values')
        mat_id, nom, serial, _, _, _, _ = valeurs

        confirm = messagebox.askyesno(
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer définitivement '{nom}' (S/N: {serial}) ?",
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
        self._role = SessionService.role()

        self.root.title("Gestion des Matériels")
        self.root.geometry("850x480")
        self.root.configure(bg="#F8F9FA")

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        tk.Label(
            root, text="Inventaire des Matériels Informatiques",
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=(15, 5), anchor="w", padx=20)

        colonnes = ('id', 'nom', 'serial', 'categorie', 'quantite', 'statut', 'date_achat')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')

        self.tableau.heading('nom', text='Nom du matériel')
        self.tableau.heading('serial', text='N° de Série')
        self.tableau.heading('categorie', text='Catégorie')
        self.tableau.heading('quantite', text='Quantité')
        self.tableau.heading('statut', text='Statut')
        self.tableau.heading('date_achat', text="Date d'achat")

        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom', width=150)
        self.tableau.column('serial', width=120)
        self.tableau.column('categorie', width=120)
        self.tableau.column('quantite', width=80, anchor="center")
        self.tableau.column('statut', width=110, anchor="center")
        self.tableau.column('date_achat', width=110, anchor="center")
        self.tableau.pack(fill="both", expand=True, padx=20, pady=10)

        # Barre d'actions — boutons affichés selon le rôle
        zone_boutons = tk.Frame(root, bg="#F8F9FA")
        zone_boutons.pack(fill="x", side=tk.BOTTOM, pady=15, padx=10)

        style_btn = {
            "font": ("Arial", 9, "bold"), "fg": "white",
            "relief": "flat", "padx": 15, "pady": 6, "cursor": "hand2"
        }

        if PermissionService.peut(self._role, "ajouter_materiel"):
            tk.Button(
                zone_boutons, text="Ajouter", command=self.ajouter_materiel,
                bg="#27AE60", **style_btn
            ).pack(side=tk.LEFT, padx=10)

        if PermissionService.peut(self._role, "modifier_materiel"):
            tk.Button(
                zone_boutons, text="Modifier", command=self.modifier_materiel,
                bg="#2980B9", **style_btn
            ).pack(side=tk.LEFT, padx=10)

        if PermissionService.peut(self._role, "supprimer_materiel"):
            tk.Button(
                zone_boutons, text="Supprimer", command=self.supprimer_materiel,
                bg="#C0392B", **style_btn
            ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            zone_boutons, text="Retour", command=retour_dashboard_window,
            bg="#7F8C8D", **style_btn
        ).pack(side=tk.RIGHT, padx=10)

        self.charger_materiels()
