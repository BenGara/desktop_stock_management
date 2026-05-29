"""Service de gestion des permissions basé sur les rôles (RBAC).

Définit les droits d'accès pour chaque rôle du système :
- ADMIN       : accès complet à toutes les fonctionnalités
- MANAGER     : gestion du stock, matériels, catégories, affectations, retours
- EMPLOYEE    : lecture seule de ses matériels affectés

Utilisation :
    from services.permission_service import PermissionService
    if PermissionService.peut(role, 'ajouter_materiel'):
        ...
"""

# Matrice des permissions : permission -> set des rôles autorisés
_PERMISSIONS = {
    # Tableau de bord
    "voir_dashboard":           {"ADMIN", "MANAGER", "EMPLOYEE"},

    # Utilisateurs
    "voir_utilisateurs":        {"ADMIN"},
    "ajouter_utilisateur":      {"ADMIN"},
    "modifier_utilisateur":     {"ADMIN"},
    "supprimer_utilisateur":    {"ADMIN"},

    # Matériels
    "voir_materiels":           {"ADMIN", "MANAGER", "EMPLOYEE"},
    "ajouter_materiel":         {"ADMIN", "MANAGER"},
    "modifier_materiel":        {"ADMIN", "MANAGER"},
    "supprimer_materiel":       {"ADMIN"},

    # Catégories
    "voir_categories":          {"ADMIN", "MANAGER"},
    "ajouter_categorie":        {"ADMIN", "MANAGER"},
    "modifier_categorie":       {"ADMIN", "MANAGER"},
    "supprimer_categorie":      {"ADMIN"},

    # Affectations
    "voir_affectations":        {"ADMIN", "MANAGER"},
    "creer_affectation":        {"ADMIN", "MANAGER"},
    "retourner_materiel":       {"ADMIN", "MANAGER"},

    # Journal / Historique
    "voir_journal":             {"ADMIN", "MANAGER"},

    # Statistiques
    "voir_statistiques":        {"ADMIN", "MANAGER"},

    # Pannes
    "declarer_panne":           {"ADMIN", "MANAGER", "EMPLOYEE"},
    "gerer_pannes":             {"ADMIN", "MANAGER"},
}


class PermissionService:
    """Fournit les méthodes de vérification des droits d'accès."""

    @staticmethod
    def peut(role: str, permission: str) -> bool:
        """Retourne True si le rôle possède la permission demandée."""
        if not role or not permission:
            return False
        roles_autorises = _PERMISSIONS.get(permission, set())
        return role.upper() in roles_autorises

    @staticmethod
    def peut_ou_erreur(role: str, permission: str) -> None:
        """Lève PermissionError si le rôle n'a pas la permission."""
        if not PermissionService.peut(role, permission):
            raise PermissionError(
                f"Accès refusé : le rôle '{role}' "
                f"ne dispose pas de la permission '{permission}'."
            )

    @staticmethod
    def permissions_du_role(role: str) -> list:
        """Retourne la liste de toutes les permissions accordées à un rôle."""
        role_upper = role.upper() if role else ""
        return [
            perm
            for perm, roles in _PERMISSIONS.items()
            if role_upper in roles
        ]

    @staticmethod
    def roles_valides() -> list:
        """Retourne la liste des rôles reconnus par le système."""
        return ["ADMIN", "MANAGER", "EMPLOYEE"]
