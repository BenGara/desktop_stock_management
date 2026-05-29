"""Service de gestion de la session utilisateur.

Stocke l'utilisateur actuellement connecté en mémoire
et expose des accesseurs simples utilisés par toute l'application.

Usage :
    from services.session_service import SessionService

    SessionService.ouvrir(user_row)   # à l'authentification
    SessionService.role()             # -> 'ADMIN' | 'MANAGER' | 'EMPLOYEE'
    SessionService.fermer()           # à la déconnexion
"""


class SessionService:
    """Singleton léger qui conserve les données de l'utilisateur connecté."""

    _utilisateur = None   # Ligne sqlite3.Row ou dict retournée par UserModel

    # Ouverture / Fermeture
    @classmethod
    def ouvrir(cls, utilisateur) -> None:
        """Enregistre l'utilisateur connecté en session.

        Args:
            utilisateur: Ligne retournée par AuthService.login()
                         (sqlite3.Row avec au minimum 'role_id' et 'id').
        """
        cls._utilisateur = utilisateur

    @classmethod
    def fermer(cls) -> None:
        """Réinitialise la session (déconnexion)."""
        cls._utilisateur = None

    # Accesseurs
    @classmethod
    def est_connecte(cls) -> bool:
        """Retourne True si une session est active."""
        return cls._utilisateur is not None

    @classmethod
    def utilisateur(cls):
        """Retourne la ligne complète de l'utilisateur connecté, ou None."""
        return cls._utilisateur

    @classmethod
    def id(cls):
        """Retourne l'identifiant (int) de l'utilisateur connecté."""
        if cls._utilisateur is None:
            return None
        return cls._utilisateur["id"]

    @classmethod
    def role(cls) -> str:
        """Retourne le nom du rôle en MAJUSCULES, ou chaîne vide si hors session.

        La colonne 'role_name' est ajoutée par AuthService.login() via la
        jointure avec la table roles. Si elle est absente pour rétrocompatibilité,
        on retourne 'EMPLOYEE' par défaut.
        """
        if cls._utilisateur is None:
            return ""
        # Supporte sqlite3.Row (accès par nom) et dict
        try:
            return str(cls._utilisateur["role_name"]).upper()
        except (KeyError, IndexError):
            return "EMPLOYEE"

    @classmethod
    def prenom(cls) -> str:
        """Retourne le prénom de l'utilisateur connecté."""
        if cls._utilisateur is None:
            return ""
        try:
            return cls._utilisateur["firstname"]
        except (KeyError, IndexError):
            return ""

    @classmethod
    def nom_complet(cls) -> str:
        """Retourne 'Prénom Nom' de l'utilisateur connecté."""
        if cls._utilisateur is None:
            return ""
        try:
            return f"{cls._utilisateur['firstname']} {cls._utilisateur['lastname']}"
        except (KeyError, IndexError):
            return ""
