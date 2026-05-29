import tkinter as tk
from tkinter import ttk, messagebox
from services.breakdown_service import BreakdownService

class BreakdownWindow:
    """Interface de déclaration et de suivi des pannes de matériel."""

    def __init__(self, root, dashboard_parent):
        self.root = root
        self.dashboard_parent = dashboard_parent
        self.root.title("Suivi des Pannes")
        self.root.geometry("750x480")
        self.root.configure(bg="#F8F9FA")
        self.root.grab_set()

        # Titre principal
        tk.Label(self.root, text="Gestion et Suivi des Pannes", font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#2C3E50").pack(pady=10)

        # ---- PARTIE HAUTE : FORMULAIRE DE DÉCLARATION ----
        form_frame = tk.LabelFrame(self.root, text="Déclarer une nouvelle panne", font=("Arial", 10, "bold"), bg="#F8F9FA", fg="#34495E", padx=10, pady=5)
        form_frame.pack(fill="x", padx=20, pady=5)

        try:
            self.dict_mats = BreakdownService.obtenir_tous_materiels_combobox()
            liste_mats = list(self.dict_mats.keys())
        except Exception:
            liste_mats = []

        tk.Label(form_frame, text="Matériel concerné :", bg="#F8F9FA").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_mat = ttk.Combobox(form_frame, values=liste_mats, state="readonly", width=30)
        self.combo_mat.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Description du problème :", bg="#F8F9FA").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_desc = tk.Entry(form_frame, width=35)
        self.entry_desc.grid(row=0, column=3, padx=5, pady=5)

        btn_declarer = tk.Button(form_frame, text="Signaler", command=self.ajouter_panne, bg="#E74C3C", fg="white", font=("Arial", 9, "bold"), relief="flat")
        btn_declarer.grid(row=0, column=4, padx=10, pady=5, ipady=2)

        # ---- PARTIE CENTRALE : TABLEAU DES PANNES ACTUELLES ----
        self.tableau = ttk.Treeview(self.root, columns=('id', 'materiel', 'desc', 'statut', 'date'), show='headings')
        self.tableau.heading('id', text='ID Panne')
        self.tableau.heading('materiel', text='Équipement')
        self.tableau.heading('desc', text='Description du problème')
        self.tableau.heading('statut', text='État de la réparation')
        self.tableau.heading('date', text='Date de signalement')
        
        self.tableau.column('id', width=60, anchor="center")
        self.tableau.column('materiel', width=180)
        self.tableau.column('desc', width=250)
        self.tableau.column('statut', width=120, anchor="center")
        self.tableau.column('date', width=100, anchor="center")
        self.tableau.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- PARTIE BASSE : ACTIONS SUR LA PANNE SÉLECTIONNÉE ----
        actions_frame = tk.Frame(self.root, bg="#F8F9FA")
        actions_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(actions_frame, text="Changer l'état :", bg="#F8F9FA", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.combo_statut = ttk.Combobox(actions_frame, values=["En cours de réparation", "Réparé (Retour au stock)", "Mis hors service"], state="readonly", width=22)
        self.combo_statut.pack(side=tk.LEFT, padx=5)
        self.combo_statut.current(0)

        btn_maj = tk.Button(actions_frame, text="Mettre à jour l'état", command=self.modifier_statut, bg="#2980B9", fg="white", font=("Arial", 9, "bold"), relief="flat")
        btn_maj.pack(side=tk.LEFT, padx=5)

        btn_retour = tk.Button(
            text="Retour", command=self.quitter, 
            bg="#7F8C8D", fg="white", font=("Arial", 9, "bold"), 
            relief="flat", cursor="hand2", width=12
        )
        btn_retour.pack(side=tk.LEFT, ipady=4)        
        self.charger_pannes()
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

    def charger_pannes(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        try:
            for p in BreakdownService.obtenir_pannes_formatees():
                # On stocke l'ID matériel en valeur cachée
                self.tableau.insert('', tk.END, iid=p[0], values=(p[0], p[1], p[2], p[3], p[4]), tags=(p[5],))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement : {e}", parent=self.root)

    def ajouter_panne(self):
        try:
            BreakdownService.déclarer_panne(self.combo_mat.get(), self.entry_desc.get())
            messagebox.showinfo("Succès", "Panne enregistrée ! Le matériel est configuré 'En panne'.", parent=self.root)
            self.entry_desc.delete(0, tk.END)
            self.charger_pannes()
        except ValueError as ve:
            messagebox.showwarning("Saisie", str(ve), parent=self.root)

    def modifier_statut(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une panne dans la liste.", parent=self.root)
            return
        
        breakdown_id = selection[0]
        material_id = self.tableau.item(breakdown_id, 'tags')[0]
        nouvel_etat = self.combo_statut.get()

        try:
            BreakdownService.changer_statut_panne(breakdown_id, material_id, nouvel_etat)
            messagebox.showinfo("Mis à jour", "L'état de la panne et le stock ont été actualisés.", parent=self.root)
            self.charger_pannes()
        except Exception as e:
            messagebox.showerror("Erreur", str(e), parent=self.root)

    def quitter(self):
        self.root.destroy()
        self.dashboard_parent.root.deiconify()
        if hasattr(self.dashboard_parent, 'charger_materiels'):
            self.dashboard_parent.charger_materiels()