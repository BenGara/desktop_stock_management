import tkinter as tk
from tkinter import ttk, messagebox
from services.assignment_service import AssignmentService

class AssignmentWindow:
    """Fenêtre d'affectation d'un équipement informatique à un employé."""

    def __init__(self, root, dashboard_parent):
        self.root = root
        self.dashboard_parent = dashboard_parent
        
        self.root.title("Affectation de Matériel")
        self.root.geometry("400x380")
        self.root.configure(bg="#F8F9FA")
        self.root.grab_set()
        
        def retour_dashboard_window():
            self.root.destroy()
            self.dashboard_parent.root.deiconify()
            self.dashboard_parent.refresh()

        # Titre
        tk.Label(
            self.root, text="Attribuer un Équipement", 
            font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50"
        ).pack(pady=20)

        # Conteneur formulaire
        form_frame = tk.Frame(self.root, bg="#F8F9FA")
        form_frame.pack(padx=30, fill="x")

        # --- CHARGEMENT DES DONNÉES ---
        try:
            self.dict_materiels = AssignmentService.obtenir_materiels_disponibles()
            self.dict_employes = AssignmentService.obtenir_employes_actifs()
            
            liste_mats = list(self.dict_materiels.keys())
            liste_emps = list(self.dict_employes.keys())
        except Exception as e:
            messagebox.showerror("Erreur Données", f"Impossible de charger les listes : {e}")
            liste_mats, liste_emps = [], []

        # --- CHAMP : SÉLECTION MATÉRIEL ---
        tk.Label(form_frame, text="Choisir le matériel disponible :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.combo_mat = ttk.Combobox(form_frame, values=liste_mats, state="readonly")
        self.combo_mat.pack(fill="x", ipady=3)
        if liste_mats:
            self.combo_mat.current(0)

        # --- CHAMP : SÉLECTION EMPLOYÉ ---
        tk.Label(form_frame, text="Choisir l'employé bénéficiaire :", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 2))
        self.combo_emp = ttk.Combobox(form_frame, values=liste_emps, state="readonly")
        self.combo_emp.pack(fill="x", ipady=3)
        if liste_emps:
            self.combo_emp.current(0)

        # --- BOUTON DE VALIDATION ---
        btn_valider = tk.Button(
            self.root, text="Valider l'affectation", command=self.enregistrer_affectation,
            bg="#27AE60", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2"
        )
        # J'ai réduit un peu le pady du bouton du haut pour que le bouton Retour ne soit pas trop collé en bas
        btn_valider.pack(fill="x", padx=30, pady=(25, 10), ipady=6)

        # --- NOUVEAU BOUTON : RETOUR ---
        # Il utilise les mêmes paramètres visuels que ton bouton retour de la page matériel
        btn_retour = tk.Button(
            self.root, text="Retour", command=self.quitter,
            bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), relief="flat", cursor="hand2"
        )
        btn_retour.pack(fill="x", padx=30, pady=(0, 20), ipady=5)

        # Protocole de fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)
        
    def enregistrer_affectation(self):
        """Appelle le service pour enregistrer l'affectation et met à jour l'application."""
        choix_mat = self.combo_mat.get()
        choix_emp = self.combo_emp.get()

        try:
            AssignmentService.affecter_materiel(choix_mat, choix_emp)
            messagebox.showinfo("Succès", f"L'équipement a bien été affecté !", parent=self.root)
            
            # Fermer la fenêtre et rafraîchir l'inventaire sur le tableau de bord parent si nécessaire
            self.quitter()
            
        except ValueError as ve:
            messagebox.showwarning("Attention", str(ve), parent=self.root)
        except Exception as e:
            messagebox.showerror("Erreur système", f"Une erreur est survenue : {e}", parent=self.root)

    def quitter(self):
        self.root.destroy()
        self.dashboard_parent.root.deiconify()
        if hasattr(self.dashboard_parent, 'charger_materiels'):
            self.dashboard_parent.charger_materiels()