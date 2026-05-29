import tkinter as tk
from tkinter import ttk, messagebox
from models.assignment_model import AssignmentModel

class EmployeeEquipmentWindow:
    """Espace personnel de l'employé pour visualiser ses équipements."""

    def __init__(self, root, connected_user_id, connected_user_name):
        self.root = root
        self.user_id = connected_user_id
        
        self.root.title("Mon Matériel Informatique")
        self.root.geometry("600x400")
        self.root.configure(bg="#F8F9FA")

        # Message de bienvenue personnalisé
        tk.Label(
            self.root, text=f"Bienvenue, {connected_user_name}", 
            font=("Arial", 12, "italic"), bg="#F8F9FA", fg="#7F8C8D"
        ).pack(anchor="w", padx=20, pady=(15, 0))

        tk.Label(
            self.root, text="Liste des équipements qui vous sont attribués :", 
            font=("Arial", 11, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(anchor="w", padx=20, pady=(5, 10))

        # Tableau d'affichage allégé (Pas de boutons d'administration d'ici)
        self.tableau = ttk.Treeview(self.root, columns=('nom', 'serial', 'categorie', 'date_aff'), show='headings')
        self.tableau.heading('nom', text='Nom du Matériel')
        self.tableau.heading('serial', text='Numéro de Série')
        self.tableau.heading('categorie', text='Catégorie')
        self.tableau.heading('date_aff', text='Assigné le')
        
        self.tableau.column('nom', width=150)
        self.tableau.column('serial', width=130, anchor="center")
        self.tableau.column('categorie', width=120)
        self.tableau.column('date_aff', width=120, anchor="center")
        self.tableau.pack(fill="both", expand=True, padx=20, pady=10)

    # ---- BARRE INFÉRIEURE DE BOUTONS ----
        zone_basse = tk.Frame(self.root, bg="#F8F9FA")
        zone_basse.pack(side=tk.BOTTOM, fill="x", padx=20, pady=15)

        # 1. BOUTON RETOUR (Correction : ajout de zone_basse en premier argument)
        btn_retour = tk.Button(
            zone_basse, text="Retour", command=self.quitter,
            bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), 
            relief="flat", cursor="hand2", width=12
        )
        btn_retour.pack(side=tk.LEFT, ipady=4)

        # 2. BOUTON DÉCONNEXION (Correction : rangé dans zone_basse au lieu de self.root directement)
        btn_deco = tk.Button(
            zone_basse, text="Se déconnecter", command=self.deconnexion,
            bg="#C0392B", fg="white", font=("Arial", 9, "bold"), 
            relief="flat", cursor="hand2", width=15
        )
        btn_deco.pack(side=tk.RIGHT, ipady=4)
        
        self.charger_mes_equipements()

    def charger_mes_equipements(self):
        try:
            mes_mats = AssignmentModel.get_materials_by_user(self.user_id)
            for row in mes_mats:
                # Formatage esthétique de la catégorie
                cat_formatee = row[2].capitalize() if row[2] else "Général"
                self.tableau.insert('', tk.END, values=(row[0], row[1], cat_formatee, row[3]))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération de vos équipements : {e}", parent=self.root)

    def deconnexion(self):
        if messagebox.askyesno("Déconnexion", "Souhaitez-vous fermer votre session ?", parent=self.root):
            self.root.destroy()
            # Ici, vous pouvez rappeler votre fenêtre d'authentification (ex: LoginWindow)
            
    # Ajoute cette méthode tout à la fin de ta classe EmployeeEquipmentWindow :
    def quitter(self):
        self.root.destroy()
        if self.parent and hasattr(self.parent, 'root'):
            self.parent.root.deiconify()