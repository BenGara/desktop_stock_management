"""Module de l'interface utilisateur pour la fenêtre de gestion des utilisateurs."""

import tkinter as tk
from tkinter import ttk, messagebox
from services.user_service import UserService

class UserWindow:
    """Affiche les informations des utilisateurs et permet de gérer les utilisateurs du système."""

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
        """Ouvre un popup avec un formulaire complet pour ajouter un utilisateur."""
        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un nouvel utilisateur")
        popup.geometry("350x400")
        popup.grab_set()

        tk.Label(popup, text="Nouvel Utilisateur", font=("Arial", 12, "bold")).pack(pady=15)
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        tk.Label(form_frame, text="Prénom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_prenom = tk.Entry(form_frame)
        entry_prenom.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Nom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Adresse Email :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_email = tk.Entry(form_frame)
        entry_email.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Mot de passe :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_mdp = tk.Entry(form_frame, show="*")
        entry_mdp.pack(fill="x", pady=2)

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
            prenom = entry_prenom.get()
            nom = entry_nom.get()
            email = entry_email.get()
            mdp = entry_mdp.get()
            role_texte = combo_role.get()

            try:
                UserService.inscrire_utilisateur(prenom, nom, email, mdp, role_texte)
                messagebox.showinfo("Succès", f"L'utilisateur {prenom.strip()} {nom.strip()} a été créé !", parent=popup)
                self.charger_utilisateurs()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie incomplète", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible d'ajouter l'utilisateur : {e}", parent=popup)

        btn_enregistrer = tk.Button(
            popup, text="Enregistrer", command=valider_et_enregistrer, 
            bg="#28A745", fg="white", font=("Arial", 10, "bold")
        )
        btn_enregistrer.pack(pady=20)


    def modification_utilisateur(self):
        """Ouvre un popup pré-rempli pour modifier l'utilisateur sélectionné."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur.")
            return

        # Récupération des valeurs de la ligne sélectionnée
        valeurs = self.tableau.item(selection[0], 'values')
        user_id, prenom_actuel, nom_actuel, email_actuel, role_actuel = valeurs

        # Création de la fenêtre Popup de modification
        popup = tk.Toplevel(self.root)
        popup.title("Modifier un utilisateur")
        popup.geometry("350x350")
        popup.grab_set()

        tk.Label(popup, text="Modifier l'Utilisateur", font=("Arial", 12, "bold")).pack(pady=15)
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        # Injection des valeurs existantes dans les champs
        tk.Label(form_frame, text="Prénom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_prenom = tk.Entry(form_frame)
        entry_prenom.insert(0, prenom_actuel)
        entry_prenom.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Nom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.insert(0, nom_actuel)
        entry_nom.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Adresse Email :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_email = tk.Entry(form_frame)
        entry_email.insert(0, email_actuel)
        entry_email.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Rôle du compte :", anchor="w").pack(fill="x", pady=(5, 0))
        try:
            roles_disponibles = UserService.obtenir_noms_roles()
        except Exception:
            roles_disponibles = ["Admin", "Manager", "Employee"]
            
        combo_role = ttk.Combobox(form_frame, values=roles_disponibles, state="readonly")
        combo_role.pack(fill="x", pady=2)
        
        # Sélectionner le rôle actuel de l'utilisateur dans la Combobox
        if role_actuel in roles_disponibles:
            combo_role.set(role_actuel)
        elif roles_disponibles:
            combo_role.current(0)

        def enregistrer_modification():
            prenom = entry_prenom.get()
            nom = entry_nom.get()
            email = entry_email.get()
            role_texte = combo_role.get()

            try:
                # Appel du service métier pour la modification
                UserService.modifier_utilisateur(user_id, prenom, nom, email, role_texte)
                messagebox.showinfo("Succès", "L'utilisateur a été mis à jour !", parent=popup)
                self.charger_utilisateurs()
                popup.destroy()
            except ValueError as ve:
                messagebox.showwarning("Saisie incomplète", str(ve), parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible de modifier l'utilisateur : {e}", parent=popup)

        btn_enregistrer = tk.Button(
            popup, text="Enregistrer les modifications", command=enregistrer_modification,
            bg="#007ACC", fg="white", font=("Arial", 10, "bold")
        )
        btn_enregistrer.pack(pady=20)

    def suppression_utilisateur(self):
        """Supprime l'utilisateur sélectionné après confirmation."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur.")
            return

        valeurs = self.tableau.item(selection[0], 'values')
        user_id, prenom, nom, _, _ = valeurs

        confirm = messagebox.askyesno(
            "Confirmation de suppression", 
            f"Voulez-vous vraiment supprimer définitivement l'utilisateur {prenom} {nom} ?",
            parent=self.root
        )
        
        if confirm:
            try:
                # Appel du service métier pour la suppression
                UserService.supprimer_utilisateur(user_id)
                messagebox.showinfo("Succès", "L'utilisateur a bien été supprimé !", parent=self.root)
                self.charger_utilisateurs()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}", parent=self.root)

    def __init__(self, root, dashboard_parent):
        """Initialise la fenêtre de gestion des utilisateurs."""
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Gestion des Utilisateurs")
        self.root.geometry("750x450")

        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()

        tk.Label(root, text="Liste des Utilisateurs", font=("Arial", 14, "bold")).pack(pady=10)

        colonnes = ('id', 'prenom', 'nom', 'email', 'role')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
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

        zone_boutons = tk.Frame(root)
        zone_boutons.pack(fill="x", side=tk.BOTTOM, pady=20)

        btn_ajouter = tk.Button(
            zone_boutons, text="Ajouter", command=self.ajouter_utilisateur,
            bg="#28A745", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_ajouter.pack(side=tk.LEFT, padx=10)

        btn_modifier = tk.Button(
            zone_boutons, text="Modifier", command=self.modification_utilisateur,
            bg="#007ACC", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_modifier.pack(side=tk.LEFT, padx=10)

        btn_supprimer = tk.Button(
            zone_boutons, text="Supprimer", command=self.suppression_utilisateur,
            bg="#DC3545", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2"
        )
        btn_supprimer.pack(side=tk.LEFT, padx=10)

        btn_retour = tk.Button(zone_boutons, text="Retour", command=retour_dashboard_window, padx=20)
        btn_retour.pack(side=tk.RIGHT, padx=10)

        self.charger_utilisateurs()