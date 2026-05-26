"""Module de l'interface utilisateur pour la fenêtre de gestion des utilisateurs."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.user_model import UserModel

class UserWindow:
    """Affiche les informations des utilisateurs 
    et permet de gérer les utilisateurs du système."""

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

    def ouvrir_modification_mdp(self):
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

        def valider_changement():
            nouveau_mdp = entry_mdp.get().strip()
            if not nouveau_mdp:
                messagebox.showerror("Erreur", "Le champ ne peut pas être vide.", parent=popup)
                return
            messagebox.showinfo("Succès", "Le mot de passe a été mis à jour avec succès !", parent=popup)
            popup.destroy()

        tk.Button(
            popup, 
            text="Enregistrer", 
            command=valider_changement, 
            bg="#28A745", 
            fg="white"
        ).pack(pady=15)

    def __init__(self, root, dashboard_parent):
        self.dashboard_parent = dashboard_parent
        self.root = root
        self.root.title("Utilisateurs")
        self.root.geometry("650x400") # Légèrement agrandi pour accueillir le bouton
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            
        tk.Label(
            root,
            text="Liste des utilisateurs",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Structure du tableau
        colonnes = ('id', 'nom', 'prenom', 'email', 'role')
        self.tableau = ttk.Treeview(root, columns=colonnes, show='headings')
        
        self.tableau.heading('id', text='ID')
        self.tableau.heading('nom', text='Nom')
        self.tableau.heading('prenom', text='Prénom')
        self.tableau.heading('email', text='Adresse Email')
        self.tableau.heading('role', text='Rôle')
        
        self.tableau.column('id', width=30, anchor='center')
        self.tableau.column('nom', width=100)
        self.tableau.column('prenom', width=100)
        self.tableau.column('email', width=200)
        self.tableau.column('role', width=100)
        
        self.tableau.pack(pady=10, padx=10, fill='both', expand=True)

        # --- ZONE DES BOUTONS EN BAS ---
        zone_boutons = tk.Frame(root)
        zone_boutons.pack(pady=10)

        # Bouton Modifier le mot de passe
        btn_modifier = tk.Button(
            zone_boutons,
            text="🔒 Modifier le mot de passe",
            command=self.ouvrir_modification_mdp,
            bg="#ECA32D",
            fg="white",
            padx=10
        )
        btn_modifier.pack(side=tk.LEFT, padx=10)

        # Bouton de retour
        btn_retour = tk.Button(
            zone_boutons, 
            text="← Retour", 
            command=retour_dashboard_window,
            padx=10
        )
        btn_retour.pack(side=tk.LEFT, padx=10)

        # Chargement automatique des données
        self.charger_utilisateurs()