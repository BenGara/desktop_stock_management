"""Module de l'interface utilisateur pour la fenêtre de gestion des utilisateurs."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.user_model import UserModel

class UserWindow:
    """Affiche les informations des utilisateurs 
    et permet de gérer les utilisateurs du système."""

    # chargement des utilisateurs dans le tableau
    def charger_utilisateurs(self):
        """Récupère les utilisateurs du modèle et les insère dans le Treeview"""
        try:
            liste_utilisateurs = UserModel.get_all_users()
            
            for item in self.tableau.get_children():
                self.tableau.delete(item)
                
            for utilisateur in liste_utilisateurs:
                self.tableau.insert('', tk.END, values=utilisateur)
                
        except Exception as e:
            print(f"Erreur lors du chargement des utilisateurs : {e}")

    # Fonction de modification d'utilisateur
    def modification_utilisateur(self):
        """Ouvre le formulaire de modification (Stratégie B) sans émojis."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur.")
            return

        # Récupération des données de la ligne
        valeurs = self.tableau.item(selection[0], 'values')
        user_id = valeurs[0]
        user_nom = valeurs[1]
        user_prenom = valeurs[2]
        user_email = valeurs[3]
        user_role_actuel = valeurs[4]

        # Fenêtre Popup
        popup = tk.Toplevel(self.root)
        popup.title("Modification Utilisateur")
        popup.geometry("360x460")
        popup.grab_set()

        tk.Label(popup, text="Modifier le profil", font=("Arial", 12, "bold")).pack(pady=15)
        
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        # Champ Prénom
        tk.Label(form_frame, text="Prénom :", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
        entry_prenom = tk.Entry(form_frame, font=("Arial", 10))
        entry_prenom.insert(0, user_prenom)
        entry_prenom.pack(fill="x", pady=2)

        # Champ Nom
        tk.Label(form_frame, text="Nom :", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
        entry_nom = tk.Entry(form_frame, font=("Arial", 10))
        entry_nom.insert(0, user_nom)
        entry_nom.pack(fill="x", pady=2)

        # Champ Email
        tk.Label(form_frame, text="Adresse Email :", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
        entry_email = tk.Entry(form_frame, font=("Arial", 10))
        entry_email.insert(0, user_email)
        entry_email.pack(fill="x", pady=2)

        # Champ Rôle
        tk.Label(form_frame, text="Rôle :", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
        roles_disponibles = ["Administrateur", "Gestionnaire de stock", "Employé"]
        combo_role = ttk.Combobox(form_frame, values=roles_disponibles, state="readonly", font=("Arial", 9))
        combo_role.pack(fill="x", pady=2)
        combo_role.set(user_role_actuel)

        # --- SÉPARATEUR VISUEL ---
        separator = tk.Frame(popup, height=1, bg="#D3D3D3")
        separator.pack(fill="x", padx=20, pady=20)

        # --- OPTION B : SOUS-BOUTON POUR LE MOT DE PASSE ---
        def rediriger_vers_mdp():
            # On ferme ce popup et on ouvre directement ton ancienne fonction de changement de mdp
            popup.destroy()
            self.modification_mdp() # Ton autre fonction s'occupe du reste !

        btn_pass = tk.Button(
            popup,
            text="Modifier le mot de passe de ce compte",
            command=rediriger_vers_mdp,
            bg="#6C757D", fg="white", font=("Arial", 9, "italic"),
            bd=0, cursor="hand2", pady=3
        )
        btn_pass.pack(pady=5)

        # --- BOUTON ENREGISTRER LES INFOS DE BASE ---
        def valider_modification():
            prenom = entry_prenom.get().strip()
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()
            role_texte = combo_role.get()

            if not prenom or not nom or not email:
                messagebox.showerror("Erreur", "Tous les champs de profil sont obligatoires.", parent=popup)
                return

            role_id = 3
            if role_texte == "Administrateur": role_id = 1
            elif role_texte == "Gestionnaire de stock": role_id = 2

            try:
                UserModel.update_user(user_id, prenom, nom, email, role_id)                
                messagebox.showinfo("Succès", "Le profil a été mis à jour !", parent=popup)
                self.charger_utilisateurs()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Erreur : {e}", parent=popup)

        btn_enregistrer = tk.Button(
            popup,
            text="Enregistrer les modifications",
            command=valider_modification,
            bg="#28A745", fg="white", font=("Arial", 10, "bold"),
            bd=0, cursor="hand2", pady=8, padx=15
        )
        btn_enregistrer.pack(side=tk.BOTTOM, pady=20)
    
    def modification_mdp(self):
        """Ouvre une Pop-up pour modifier le mot de passe de la ligne sélectionnée."""
        selection = self.tableau.selection()
        
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur dans le tableau.")
            return

        # Extraction des données de la ligne sélectionnée
        valeurs = self.tableau.item(selection[0], 'values')
        user_id = valeurs[0]
        user_nom = valeurs[1]
        user_prenom = valeurs[2]

        # Création de la fenêtre Pop-up
        popup = tk.Toplevel(self.root)
        popup.title("Changement de mot de passe")
        popup.geometry("320x200")
        popup.grab_set() # Bloque la fenêtre principale pendant la saisie

        tk.Label(
            popup, 
            text=f"Nouveau mot de passe pour :\n{user_prenom} {user_nom}", 
            font=("Arial", 10, "bold")
        ).pack(pady=15)

        entry_mdp = tk.Entry(popup, show="*", width=25)
        entry_mdp.pack(pady=5)
        entry_mdp.focus()

        def valider_changement_mdp():
            nouveau_mdp = entry_mdp.get().strip()
            if not nouveau_mdp:
                messagebox.showerror("Erreur", "Le champ ne peut pas être vide.", parent=popup)
                return
            
            try:
                # Connexion à ta méthode 'modification_mdp' présente dans ton UserModel !
                UserModel.modification_mdp(user_id, nouveau_mdp)
                messagebox.showinfo("Succès", "Le mot de passe a été mis à jour avec succès !", parent=popup)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Erreur : {e}", parent=popup)

        tk.Button(
            popup, text="Enregistrer le mot de passe", command=valider_changement_mdp, 
            bg="#007ACC", fg="white", font=("Arial", 9, "bold"), bd=0, pady=5, padx=10, cursor="hand2"
        ).pack(pady=15)
        
    def ajouter_utilisateur(self):
        """Ouvre un popup avec un formulaire complet pour ajouter un utilisateur."""
        # 1. Création de la fenêtre popup
        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un nouvel utilisateur")
        popup.geometry("350x400")
        popup.grab_set() # Bloque la fenêtre principale pendant la saisie

        # Titre du formulaire
        tk.Label(popup, text="Nouvel Utilisateur", font=("Arial", 12, "bold")).pack(pady=15)

        # Conteneur centré pour aligner les labels et les champs de saisie
        form_frame = tk.Frame(popup)
        form_frame.pack(padx=20, fill="x")

        # --- CHAMP PRÉNOM ---
        tk.Label(form_frame, text="Prénom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_prenom = tk.Entry(form_frame)
        entry_prenom.pack(fill="x", pady=2)

        # --- CHAMP NOM ---
        tk.Label(form_frame, text="Nom :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_nom = tk.Entry(form_frame)
        entry_nom.pack(fill="x", pady=2)

        # --- CHAMP EMAIL ---
        tk.Label(form_frame, text="Adresse Email :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_email = tk.Entry(form_frame)
        entry_email.pack(fill="x", pady=2)

        # --- CHAMP MOT DE PASSE ---
        tk.Label(form_frame, text="Mot de passe :", anchor="w").pack(fill="x", pady=(5, 0))
        entry_mdp = tk.Entry(form_frame, show="*") # Masqué par des astérisques
        entry_mdp.pack(fill="x", pady=2)

        # --- CHAMP RÔLE (Menu déroulant) ---
        tk.Label(form_frame, text="Rôle du compte :", anchor="w").pack(fill="x", pady=(5, 0))
        
        # Saisie par liste déroulante Combobox
        roles_disponibles = ["Administrateur", "Gestionnaire de stock", "Employé"]
        combo_role = ttk.Combobox(form_frame, values=roles_disponibles, state="readonly")
        combo_role.current(2) # Sélectionne "Employé" par défaut
        combo_role.pack(fill="x", pady=2)

        # 2. Fonction interne de validation pour le bouton Enregistrer
        def valider_et_enregistrer():
            prenom = entry_prenom.get().strip()
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()
            mdp = entry_mdp.get().strip()
            role_texte = combo_role.get()

            # Vérification des champs vides
            if not prenom or not nom or not email or not mdp:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.", parent=popup)
                return

            # Correspondance entre le texte sélectionné et l'ID du rôle de ta BDD (table roles)
            role_id = 3 # Par défaut employé
            if role_texte == "Administrateur":
                role_id = 1
            elif role_texte == "Gestionnaire de stock":
                role_id = 2

            try:
                # Appel du modèle existant pour l'insertion SQL !
                UserModel.create_user(prenom, nom, email, mdp, role_id)
                
                messagebox.showinfo("Succès", f"L'utilisateur {prenom} {nom} a été créé !", parent=popup)
                
                # Rafraîchit automatiquement le grand tableau en arrière-plan
                self.charger_utilisateurs()
                
                # Ferme le popup
                popup.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible d'ajouter l'utilisateur : {e}", parent=popup)

        # --- BOUTON DE VALIDATION ---
        btn_enregistrer = tk.Button(
            popup, 
            text="Enregistrer", 
            command=valider_et_enregistrer, 
            bg="#28A745", 
            fg="white",
            font=("Arial", 10, "bold")
        )
        btn_enregistrer.pack(pady=20)
        
    def suppression_utilisateur(self):
        """Supprime l'utilisateur sélectionné après confirmation."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un utilisateur à supprimer.")
            return

        valeurs = self.tableau.item(selection[0], 'values')
        user_id = valeurs[0]
        user_nom = valeurs[1]
        user_prenom = valeurs[2]

        confirm = messagebox.askyesno(
            "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur : {user_prenom} {user_nom} ?"
        )

        if confirm:
            try:
                UserModel.delete_user(user_id)
                messagebox.showinfo("Utilisateur supprimé", f"L'utilisateur {user_prenom} {user_nom} a été supprimé.")
                self.charger_utilisateurs()
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible de supprimer l'utilisateur : {e}")


    def __init__(self, root, dashboard_parent):
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Utilisateurs")
        self.root.geometry("650x400")
                
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            
        self.root.protocol("WM_DELETE_WINDOW", retour_dashboard_window)
            
        tk.Label(
            root,
            text="Liste des utilisateurs",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Structure du tableau
        colonnes = ('id', 'nom', 'prenom', 'email', 'role')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
        # En-têtes (Uniquement pour les colonnes que l'on VEUT voir)
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('prenom', text='Prénom')
        self.tableau.heading('email', text='Adresse Email')
        self.tableau.heading('role', text='Rôle')
        
        # Affichage du tableau
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Configuration des tailles de TOUTES les colonnes
        self.tableau.column('id', width=0, minwidth=0, stretch=False)
        self.tableau.column('nom', width=100, minwidth=50)
        self.tableau.column('prenom', width=100, minwidth=50)
        self.tableau.column('email', width=200, minwidth=100)
        self.tableau.column('role', width=100, minwidth=50)
                
        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(pady=10)
        
        # Bouton Ajouter un utilisateur
        btn_ajouter = tk.Button(
            zone_boutons,
            text="Ajouter",
            command=self.ajouter_utilisateur,
            bg="#28A745",
            fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
        )
        btn_ajouter.pack(side=tk.LEFT, padx=10)

        # Bouton Modifier l'utilisateur
        btn_modifier = tk.Button(
            zone_boutons,
            text="Modifier",
            command=self.modification_utilisateur,
            bg="#007ACC",
            fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, cursor="hand2"
            )
        btn_modifier.pack(side=tk.LEFT, padx=10)

        # Bouton Supprimer l'utilisateur
        btn_supprimer = tk.Button(
            zone_boutons,
            text="Supprimer",
            command=self.suppression_utilisateur,
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

        # Chargement automatique des données
        self.charger_utilisateurs()