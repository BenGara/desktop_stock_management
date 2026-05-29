# -*- coding: utf-8 -*-
"""Module de l'interface utilisateur pour la fenêtre de gestion des utilisateurs."""

import tkinter as tk
from tkinter import ttk, messagebox

from services.user_service import UserService
from services.session_service import SessionService
from services.permission_service import PermissionService


class UserWindow:
    """Gestion des utilisateurs — accessible aux ADMIN uniquement."""

    def charger_utilisateurs(self):
        """Met à jour le Treeview avec les utilisateurs fournis par le service."""
        try:
            liste_utilisateurs = UserService.obtenir_tous_utilisateurs()
            for item in self.tableau.get_children():
                self.tableau.delete(item)
            for user in liste_utilisateurs:
                self.tableau.insert('', tk.END, values=user)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les utilisateurs : {e}", parent=self.root)

    def ajouter_utilisateur(self):
        if not PermissionService.peut(self._role, "ajouter_utilisateur"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour ajouter un utilisateur.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un nouvel utilisateur")
        popup.geometry("350x400")
        popup.grab_set()

        tk.Label(popup, text="Nouvel Utilisateur", font=("Arial", 12, "bold")).pack(pady=15)
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        for label, var_name, show in [
            ("Prénom :", "entry_prenom", ""),
            ("Nom :", "entry_nom", ""),
            ("Adresse Email :", "entry_email", ""),
            ("Mot de passe :", "entry_mdp", "*"),
        ]:
            tk.Label(form_frame, text=label, anchor="w").pack(fill="x", pady=(5, 0))
            entry = tk.Entry(form_frame, show=show)
            entry.pack(fill="x", pady=2)
            setattr(self, var_name, entry)

        tk.Label(form_frame, text="Rôle du compte :", anchor="w").pack(fill="x", pady=(5, 0))
        try:
            roles_disponibles = UserService.obtenir_noms_roles()
        except Exception:
            roles_disponibles = ["Admin", "Manager", "Employee"]
        combo_role = ttk.Combobox(form_frame, values=roles_disponibles, state="readonly")
        if roles_disponibles:
            combo_role.current(len(roles_disponibles) - 1)
        combo_role.pack(fill="x", pady=2)

        def valider_et_enregistrer():
            try:
                UserService.inscrire_utilisateur(
                    self.entry_prenom.get(), self.entry_nom.get(),
                    self.entry_email.get(), self.entry_mdp.get(),
                    combo_role.get()
                )
                messagebox.showinfo("Succès", "L'utilisateur a été créé !", parent=popup)
                self.charger_utilisateurs()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie incomplète", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible d'ajouter l'utilisateur : {e}", parent=popup)

        tk.Button(
            popup, text="Enregistrer", command=valider_et_enregistrer,
            bg="#28A745", fg="white", font=("Arial", 10, "bold")
        ).pack(pady=20)

    def modification_utilisateur(self):
        if not PermissionService.peut(self._role, "modifier_utilisateur"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour modifier un utilisateur.")
            return

        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur.")
            return

        valeurs = self.tableau.item(selection[0], 'values')
        user_id, prenom_actuel, nom_actuel, email_actuel, role_actuel = valeurs

        popup = tk.Toplevel(self.root)
        popup.title("Modifier un utilisateur")
        popup.geometry("350x350")
        popup.grab_set()

        tk.Label(popup, text="Modifier l'Utilisateur", font=("Arial", 12, "bold")).pack(pady=15)
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        for label, valeur in [("Prénom :", prenom_actuel), ("Nom :", nom_actuel), ("Adresse Email :", email_actuel)]:
            tk.Label(form_frame, text=label, anchor="w").pack(fill="x", pady=(5, 0))
            e = tk.Entry(form_frame)
            e.insert(0, valeur)
            e.pack(fill="x", pady=2)

        # On récupère les références des Entry via les widgets du form_frame
        entries = [w for w in form_frame.winfo_children() if isinstance(w, tk.Entry)]
        entry_prenom, entry_nom, entry_email = entries

        tk.Label(form_frame, text="Rôle du compte :", anchor="w").pack(fill="x", pady=(5, 0))
        try:
            roles_disponibles = UserService.obtenir_noms_roles()
        except Exception:
            roles_disponibles = ["Admin", "Manager", "Employee"]
        combo_role = ttk.Combobox(form_frame, values=roles_disponibles, state="readonly")
        combo_role.pack(fill="x", pady=2)
        if role_actuel in roles_disponibles:
            combo_role.set(role_actuel)
        elif roles_disponibles:
            combo_role.current(0)

        def enregistrer_modification():
            try:
                UserService.modifier_utilisateur(
                    user_id, entry_prenom.get(), entry_nom.get(),
                    entry_email.get(), combo_role.get()
                )
                messagebox.showinfo("Succès", "L'utilisateur a été mis à jour !", parent=popup)
                self.charger_utilisateurs()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie incomplète", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible de modifier l'utilisateur : {e}", parent=popup)

        tk.Button(
            popup, text="Enregistrer les modifications", command=enregistrer_modification,
            bg="#007ACC", fg="white", font=("Arial", 10, "bold")
        ).pack(pady=20)

    def suppression_utilisateur(self):
        if not PermissionService.peut(self._role, "supprimer_utilisateur"):
            messagebox.showwarning("Accès refusé", "Vous n'avez pas les droits pour supprimer un utilisateur.")
            return

        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur.")
            return

        valeurs = self.tableau.item(selection[0], 'values')
        user_id, prenom, nom, _, _ = valeurs

        # Empêcher la suppression de son propre compte
        if str(user_id) == str(SessionService.id()):
            messagebox.showerror("Opération interdite", "Vous ne pouvez pas supprimer votre propre compte.")
            return

        confirm = messagebox.askyesno(
            "Confirmation de suppression",
            f"Voulez-vous vraiment supprimer définitivement l'utilisateur {prenom} {nom} ?",
            parent=self.root
        )
        if confirm:
            try:
                UserService.supprimer_utilisateur(user_id)
                messagebox.showinfo("Succès", "L'utilisateur a bien été supprimé !", parent=self.root)
                self.charger_utilisateurs()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Initialise la fenêtre de gestion des utilisateurs."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self._role = SessionService.role()

        self.root.title("Gestion des Utilisateurs")
        self.root.geometry("680x450")
        self.root.configure(bg="#F8F9FA")

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            self.dashboard_parent.refresh()

        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)

        tk.Label(
            root, text="Base des Utilisateurs & Collaborateurs",
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=(15, 5), anchor="w", padx=20)

        colonnes = ('id', 'prenom', 'nom', 'email', 'role')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings', selectmode="browse")

        self.tableau.heading('id', text='ID')
        self.tableau.heading('prenom', text='Prénom')
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('email', text='Adresse Email')
        self.tableau.heading('role', text='Rôle')

        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('prenom', width=120)
        self.tableau.column('nom', width=120)
        self.tableau.column('email', width=220)
        self.tableau.column('role', width=130)
        self.tableau.pack(fill="both", expand=True, padx=20, pady=10)

        zone_boutons = tk.Frame(root, bg="#F8F9FA")
        zone_boutons.pack(fill="x", side=tk.BOTTOM, pady=15, padx=10)
        style_btn = {"font": ("Arial", 9, "bold"), "fg": "white",
                     "relief": "flat", "padx": 15, "pady": 6, "cursor": "hand2"}

        if PermissionService.peut(self._role, "ajouter_utilisateur"):
            tk.Button(zone_boutons, text="Ajouter", command=self.ajouter_utilisateur,
                      bg="#27AE60", **style_btn).pack(side=tk.LEFT, padx=10)

        if PermissionService.peut(self._role, "modifier_utilisateur"):
            tk.Button(zone_boutons, text="Modifier", command=self.modification_utilisateur,
                      bg="#2980B9", **style_btn).pack(side=tk.LEFT, padx=10)

        if PermissionService.peut(self._role, "supprimer_utilisateur"):
            tk.Button(zone_boutons, text="Supprimer", command=self.suppression_utilisateur,
                      bg="#C0392B", **style_btn).pack(side=tk.LEFT, padx=10)

        tk.Button(zone_boutons, text="Retour", command=retour_dashboard_window,
                  bg="#7F8C8D", **style_btn).pack(side=tk.RIGHT, padx=10)

        self.charger_utilisateurs()
