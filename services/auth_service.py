"""Service pour gérer la logique d'authentification."""

import hashlib

from models.user_model import UserModel


class AuthService:
    """Fournit des méthodes pour le hachage des mots de passe
    et la connexion des utilisateurs.
    """

    @staticmethod
    def hash_password(password):
        """Renvoie le hachage hexadécimal SHA-256
        du mot de passe en clair fourni.
        """
        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    @staticmethod
    def login(email, password):
        """Authentifie un utilisateur à l'aide de son adresse e-mail
        et de son mot de passe.

        Renvoie la ligne de l'utilisateur en cas de succès,
        ou None si les identifiants sont invalides.
        """
        user = UserModel.get_user_by_email(email)

        if not user:
            return None

        hashed_password = AuthService.hash_password(password)

        if user["password"] != hashed_password:
            return None

        return user