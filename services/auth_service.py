"""Service pour gérer la logique d'authentification."""

import hashlib

import database
from services.session_service import SessionService


class AuthService:
    """Fournit des méthodes pour le hachage des mots de passe
    et la connexion des utilisateurs.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Renvoie le hachage hexadécimal SHA-256 du mot de passe en clair."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(email: str, password: str):
        """Authentifie un utilisateur et ouvre la session."""
        connection = database.get_connection()

        # La jointure expose 'role_name' sans passer par UserModel
        user = connection.execute(
            """
            SELECT users.*, roles.name AS role_name
            FROM users
            INNER JOIN roles ON users.role_id = roles.id
            WHERE users.email = ?
            """,
            (email,)
        ).fetchone()

        if not user:
            return None

        if user["password"] != AuthService.hash_password(password):
            return None

        # Enregistre l'utilisateur en session
        SessionService.ouvrir(user)
        return user

    @staticmethod
    def deconnexion() -> None:
        """Ferme la session de l'utilisateur actuel."""
        SessionService.fermer()
