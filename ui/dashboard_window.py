<<<<<<< HEAD
"""Module de l'interface utilisateur pour la fenêtre principale du tableau de bord."""

import tkinter as tk
from tkinter import messagebox

from ui.journal_window import JournalWindow
from ui.user_window import UserWindow
from ui.materiel_window import MaterielWindow
from ui.categorie_window import CategorieWindow
from ui.assignment_window import AssignmentWindow
from ui.breakdown_window import BreakdownWindow
from ui.employee_equipment_window import EmployeeEquipmentWindow
from ui.return_window import ReturnWindow

from models.stat_model import StatModel

from services.auth_service import AuthService


class DashboardWindow:
    """Affiche un tableau de bord moderne avec une navigation par barre latérale."""

    def refresh(self):
        """Actualise les indicateurs statistiques de la zone centrale sans risquer de planter."""
        if StatModel is None:
            self.lbl_val_stock.config(text="Erreur Import StatModel")
            return

        # Stat 1 : En Stock
        try:
            stock_stats = StatModel.get_stock_stats()
            if stock_stats and len(stock_stats) >= 2:
                self.lbl_val_stock.config(text=f"{stock_stats[0]} ({stock_stats[1]} ref)")
            else:
                self.lbl_val_stock.config(text="0 (0 ref)")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Stock : {e}")
            self.lbl_val_stock.config(text="Non dispo")

        # Stat 2 : Affectés
        try:
            assigned_stats = StatModel.get_materiel_affecte_stats()
            if assigned_stats:
                self.lbl_val_assigned.config(text=f"{assigned_stats[0]}")
            else:
                self.lbl_val_assigned.config(text="0")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Affectés : {e}")
            self.lbl_val_assigned.config(text="Non dispo")

        # Stat 3 : En panne
        try:
            broken_stats = StatModel.get_materiel_panne_stats()
            if broken_stats:
                self.lbl_val_broken.config(text=f"{broken_stats[0]}")
            else:
                self.lbl_val_broken.config(text="0")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Pannes : {e}")
            self.lbl_val_broken.config(text="Non dispo")

    def set_title(self, title):
        """Met à jour le titre de la fenêtre."""
        self.root.title(title)

    def gerer_deconnexion(self):
        """Méthode de déconnexion externalisée avec confirmation."""
        confirm = messagebox.askyesno(
            "Déconnexion", 
            "Êtes-vous sûr de vouloir fermer votre session ?",
            parent=self.root
        )
        if confirm:
            AuthService.deconnexion()  # Réinitialise la session côté service
            self.root.destroy()
            self.login_root.deiconify()  # Réaffiche proprement la fenêtre de login sous Windows

    def __init__(self, root, login_root):
        """Initialise le design du tableau de bord."""
        self.root = root
        self.login_root = login_root
        
        self.root.title("Tableau de Bord - Gestion des Stocks")
        self.root.geometry("900x800")
        self.root.configure(bg="#F8F9FA")

        # Fonctions de navigation internes sécurisées
        def show_user_window():
            self.root.withdraw()
            UserWindow(tk.Toplevel(self.root), self)

        def show_materiel_window():
            self.root.withdraw()
            MaterielWindow(tk.Toplevel(self.root), self)

        def show_categorie_window():
            self.root.withdraw()
            CategorieWindow(tk.Toplevel(self.root), self)

        def show_log_window():
            self.root.withdraw()
            JournalWindow(tk.Toplevel(self.root), self)

        def show_assignment_window():
            self.root.withdraw()
            AssignmentWindow(tk.Toplevel(self.root), self)
            
        def show_breakdown_window():
            self.root.withdraw()
            BreakdownWindow(tk.Toplevel(self.root), self)
            
        def show_employee_equipment_window():
            self.root.withdraw()
            popup = tk.Toplevel
            EmployeeEquipmentWindow(tk.Toplevel(self.root), AuthService.get_connected_user_id(), AuthService.get_connected_user_name())

        def show_return_window():
            self.root.withdraw()
            ReturnWindow(tk.Toplevel(self.root), self)

        # Gestion de la fermeture brusque via la croix rouge du système (X)
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        # =====================================================================
        # 1. BARRE LATÉRALE DE NAVIGATION (SIDEBAR) - À GAUCHE
        # =====================================================================
        sidebar = tk.Frame(self.root, bg="#2C3E50", width=220)
        sidebar.pack(side=tk.LEFT, fill="y")
        sidebar.pack_propagate(False)

        # En-tête / Titre de l'application
        tk.Label(
            sidebar, text="STOCK MANAGER", bg="#2C3E50", fg="#ECF0F1",
            font=("Arial", 12, "bold"), pady=20
        ).pack(fill="x")

        tk.Frame(sidebar, bg="#34495E", height=2).pack(fill="x", padx=15, pady=(0, 15))

        style_btn = {
            "bg": "#34495E", "fg": "white", "font": ("Arial", 10),
            "relief": "flat", "pady": 12, "cursor": "hand2",
            "anchor": "w", "padx": 20
        }
        
        # Remplacement des émojis par des caractères textuels simples compatibles Windows
        btn_user = tk.Button(sidebar, text="Utilisateurs", command=show_user_window, **style_btn)
        btn_user.pack(fill="x", padx=10, pady=4)

        btn_mat = tk.Button(sidebar, text="Matériels", command=show_materiel_window, **style_btn)
        btn_mat.pack(fill="x", padx=10, pady=4)

        btn_cat = tk.Button(sidebar, text="Catégories", command=show_categorie_window, **style_btn)
        btn_cat.pack(fill="x", padx=10, pady=4)

        btn_log = tk.Button(sidebar, text="Journal d'activités", command=show_log_window, **style_btn)
        btn_log.pack(fill="x", padx=10, pady=4)
        
        btn_return = tk.Button(sidebar, text="Retours de matériel", command=show_return_window, **style_btn)
        btn_return.pack(fill="x", padx=10, pady=4)

        btn_assignment = tk.Button(sidebar, text="Affectation de matériel", command=show_assignment_window, **style_btn)
        btn_assignment.pack(fill="x", padx=10, pady=4)
        
        btn_panne = tk.Button(sidebar, text="Matériels en panne", command=show_breakdown_window, **style_btn)
        btn_panne.pack(fill="x", padx=10, pady=4)
        
        btn_mes_mats = tk.Button(sidebar, text="Mes équipements", command=show_employee_equipment_window, **style_btn)
        btn_mes_mats.pack(fill="x", padx=10, pady=4)

        btn_logout = tk.Button(
            sidebar, text="Déconnexion", command=self.gerer_deconnexion,
            bg="#C0392B", fg="white", font=("Arial", 10, "bold"),
            relief="flat", pady=12, cursor="hand2"
        )
        btn_logout.pack(side=tk.BOTTOM, fill="x", padx=10, pady=20)

        # =====================================================================
        # 2. ZONE DE CONTENU PRINCIPALE - À DROITE
        # =====================================================================
        main_content = tk.Frame(self.root, bg="#F8F9FA", padx=35, pady=25)
        main_content.pack(side=tk.RIGHT, fill="both", expand=True)

        tk.Label(
            main_content, text="Vue d'ensemble du Parc", bg="#F8F9FA", fg="#2C3E50",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 4))
        
        tk.Label(
            main_content, text="Suivi en temps réel des indicateurs clés de votre stock informatique.", 
            bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 30))

        # Grille pour organiser les 3 cartes
        cards_frame = tk.Frame(main_content, bg="#F8F9FA")
        cards_frame.pack(fill="x")

        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)

        # --- CARTE 1 : EN STOCK ---
        card_stock = tk.LabelFrame(cards_frame, text=" Équipements Disponibles ", bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove")
        card_stock.grid(row=0, column=0, padx=10, sticky="nsew")
        self.lbl_val_stock = tk.Label(card_stock, text="-", bg="white", fg="#27AE60", font=("Arial", 18, "bold"))
        self.lbl_val_stock.pack(pady=10)

        # --- CARTE 2 : AFFECTÉS ---
        card_assigned = tk.LabelFrame(cards_frame, text=" Matériels Déployés ", bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove")
        card_assigned.grid(row=0, column=1, padx=10, sticky="nsew")
        self.lbl_val_assigned = tk.Label(card_assigned, text="-", bg="white", fg="#D35400", font=("Arial", 18, "bold"))
        self.lbl_val_assigned.pack(pady=10)

        # --- CARTE 3 : EN PANNE ---
        card_broken = tk.LabelFrame(cards_frame, text=" En Maintenance ", bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove")
        card_broken.grid(row=0, column=2, padx=10, sticky="nsew")
        self.lbl_val_broken = tk.Label(card_broken, text="-", bg="white", fg="#C0392B", font=("Arial", 18, "bold"))
        self.lbl_val_broken.pack(pady=10)

        # Exécution du rafraîchissement des compteurs
        self.refresh()
=======
"""Module de l'interface utilisateur pour la fenêtre principale du tableau de bord."""

import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from services.session_service import SessionService
from services.permission_service import PermissionService
from models.stat_model import StatModel


class DashboardWindow:
    """Tableau de bord adaptatif : le menu latéral s'affiche selon le rôle."""

    # Initialisation
    def __init__(self, root, login_root):
        """Initialise le tableau de bord en tenant compte du rôle connecté."""
        self.root = root
        self.login_root = login_root

        role = SessionService.role()
        nom = SessionService.nom_complet()

        self.root.title("Tableau de Bord — Gestion des Stocks")
        self.root.geometry("900x500")
        self.root.configure(bg="#F8F9FA")
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        self._construire_sidebar(role, nom)
        self._construire_zone_principale(role)
        self.refresh()

    # Construction de l'interface
    def _construire_sidebar(self, role: str, nom: str):
        """Construit la barre de navigation latérale filtrée par rôle."""
        sidebar = tk.Frame(self.root, bg="#2C3E50", width=220)
        sidebar.pack(side=tk.LEFT, fill="y")
        sidebar.pack_propagate(False)

        # En-tête
        tk.Label(
            sidebar, text="STOCK MANAGER", bg="#2C3E50", fg="#ECF0F1",
            font=("Arial", 12, "bold"), pady=15
        ).pack(fill="x")

        # Badge utilisateur
        badge_frame = tk.Frame(sidebar, bg="#1A252F", pady=8)
        badge_frame.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(
            badge_frame, text=nom or "Utilisateur", bg="#1A252F", fg="#BDC3C7",
            font=("Arial", 9, "bold"), wraplength=180
        ).pack()
        tk.Label(
            badge_frame, text=role.capitalize(), bg="#1A252F", fg="#7F8C8D",
            font=("Arial", 8)
        ).pack()

        tk.Frame(sidebar, bg="#34495E", height=1).pack(fill="x", padx=15, pady=(0, 10))

        style_btn = {
            "bg": "#34495E", "fg": "white", "font": ("Arial", 10),
            "relief": "flat", "pady": 12, "cursor": "hand2",
            "anchor": "w", "padx": 20
        }

        # Entrées de menu filtrées par permission
        peut = lambda p: PermissionService.peut(role, p)

        if peut("voir_utilisateurs"):
            tk.Button(
                sidebar, text="Utilisateurs",
                command=self._ouvrir_utilisateurs, **style_btn
            ).pack(fill="x", padx=10, pady=3)

        if peut("voir_materiels"):
            tk.Button(
                sidebar, text="Matériels",
                command=self._ouvrir_materiels, **style_btn
            ).pack(fill="x", padx=10, pady=3)

        if peut("voir_categories"):
            tk.Button(
                sidebar, text="Catégories",
                command=self._ouvrir_categories, **style_btn
            ).pack(fill="x", padx=10, pady=3)

        if peut("voir_affectations"):
            tk.Button(
                sidebar, text="Retours de matériel",
                command=self._ouvrir_retours, **style_btn
            ).pack(fill="x", padx=10, pady=3)

        if peut("voir_journal"):
            tk.Button(
                sidebar, text="Journal d'activités",
                command=self._ouvrir_journal, **style_btn
            ).pack(fill="x", padx=10, pady=3)

        # Bouton déconnexion (toujours visible)
        tk.Button(
            sidebar, text="Déconnexion", command=self.gerer_deconnexion,
            bg="#C0392B", fg="white", font=("Arial", 10, "bold"),
            relief="flat", pady=12, cursor="hand2"
        ).pack(side=tk.BOTTOM, fill="x", padx=10, pady=20)

    def _construire_zone_principale(self, role: str):
        """Construit la zone de contenu centrale avec les cartes de statistiques."""
        main_content = tk.Frame(self.root, bg="#F8F9FA", padx=35, pady=25)
        main_content.pack(side=tk.RIGHT, fill="both", expand=True)

        tk.Label(
            main_content, text="Vue d'ensemble du Parc", bg="#F8F9FA", fg="#2C3E50",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            main_content,
            text="Suivi en temps réel des indicateurs clés de votre stock informatique.",
            bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 20))

        # Message de bienvenue avec rôle
        tk.Label(
            main_content,
            text=f"Connecté en tant que : {role.capitalize()}",
            bg="#F8F9FA", fg="#95A5A6", font=("Arial", 9, "italic")
        ).pack(anchor="w", pady=(0, 20))

        # Cartes de statistiques (visibles pour ADMIN et MANAGER uniquement)
        if PermissionService.peut(role, "voir_statistiques"):
            cards_frame = tk.Frame(main_content, bg="#F8F9FA")
            cards_frame.pack(fill="x")
            cards_frame.columnconfigure(0, weight=1)
            cards_frame.columnconfigure(1, weight=1)
            cards_frame.columnconfigure(2, weight=1)

            card_stock = tk.LabelFrame(
                cards_frame, text=" Équipements Disponibles ",
                bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove"
            )
            card_stock.grid(row=0, column=0, padx=10, sticky="nsew")
            self.lbl_val_stock = tk.Label(
                card_stock, text="-", bg="white", fg="#27AE60", font=("Arial", 18, "bold")
            )
            self.lbl_val_stock.pack(pady=10)

            card_assigned = tk.LabelFrame(
                cards_frame, text=" Matériels Déployés ",
                bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove"
            )
            card_assigned.grid(row=0, column=1, padx=10, sticky="nsew")
            self.lbl_val_assigned = tk.Label(
                card_assigned, text="-", bg="white", fg="#D35400", font=("Arial", 18, "bold")
            )
            self.lbl_val_assigned.pack(pady=10)

            card_broken = tk.LabelFrame(
                cards_frame, text=" En Maintenance ",
                bg="white", font=("Arial", 9, "bold"), padx=15, pady=15, relief="groove"
            )
            card_broken.grid(row=0, column=2, padx=10, sticky="nsew")
            self.lbl_val_broken = tk.Label(
                card_broken, text="-", bg="white", fg="#C0392B", font=("Arial", 18, "bold")
            )
            self.lbl_val_broken.pack(pady=10)
        else:
            # Message simplifié pour l'employé
            tk.Label(
                main_content,
                text="Consultez vos matériels affectés via le menu 'Matériels'.",
                bg="#F8F9FA", fg="#2C3E50", font=("Arial", 11)
            ).pack(anchor="w", pady=20)

            # Attributs factices pour éviter les erreurs dans refresh()
            self.lbl_val_stock = None
            self.lbl_val_assigned = None
            self.lbl_val_broken = None

    # Navigation
    def _ouvrir_fenetre(self, FenetreClass, *args):
        """Méthode générique : cache le dashboard et ouvre une sous-fenêtre."""
        self.root.withdraw()
        FenetreClass(tk.Toplevel(self.root), self, *args)

    def _ouvrir_utilisateurs(self):
        from ui.user_window import UserWindow
        self._ouvrir_fenetre(UserWindow)

    def _ouvrir_materiels(self):
        from ui.materiel_window import MaterielWindow
        self._ouvrir_fenetre(MaterielWindow)

    def _ouvrir_categories(self):
        from ui.categorie_window import CategorieWindow
        self._ouvrir_fenetre(CategorieWindow)

    def _ouvrir_retours(self):
        from ui.return_window import ReturnWindow
        self._ouvrir_fenetre(ReturnWindow)

    def _ouvrir_journal(self):
        from ui.journal_window import JournalWindow
        self._ouvrir_fenetre(JournalWindow)

    # Actions
    def gerer_deconnexion(self):
        """Déconnecte l'utilisateur et réaffiche l'écran de connexion."""
        confirm = messagebox.askyesno(
            "Déconnexion",
            "Êtes-vous sûr de vouloir fermer votre session ?",
            parent=self.root
        )
        if confirm:
            AuthService.deconnexion()
            self.root.destroy()
            self.login_root.deiconify()

    def refresh(self):
        """Actualise les indicateurs statistiques (ADMIN/MANAGER uniquement)."""
        if self.lbl_val_stock is None:
            return  # Rôle Employé : pas de cartes à mettre à jour

        try:
            stock_stats = StatModel.get_stock_stats()
            if stock_stats and len(stock_stats) >= 2:
                self.lbl_val_stock.config(text=f"{stock_stats[0]} ({stock_stats[1]} ref)")
            else:
                self.lbl_val_stock.config(text="0 (0 ref)")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Stock : {e}")
            self.lbl_val_stock.config(text="Non dispo")

        try:
            assigned_stats = StatModel.get_materiel_affecte_stats()
            self.lbl_val_assigned.config(text=str(assigned_stats[0]) if assigned_stats else "0")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Affectés : {e}")
            self.lbl_val_assigned.config(text="Non dispo")

        try:
            broken_stats = StatModel.get_materiel_panne_stats()
            self.lbl_val_broken.config(text=str(broken_stats[0]) if broken_stats else "0")
        except Exception as e:
            print(f"[Dashboard] Erreur Stat Pannes : {e}")
            self.lbl_val_broken.config(text="Non dispo")

    def set_title(self, title: str):
        """Met à jour le titre de la fenêtre."""
        self.root.title(title)
>>>>>>> 9dd5e7a97797f8abb2c067adc1e9cd48006b0721
