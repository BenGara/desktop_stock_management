"""Service layer handling authentication logic."""

import hashlib

from models.user_model import UserModel


class AuthService:
    """Provides static methods for password hashing and user login."""

    @staticmethod
    def hash_password(password):
        """Return the SHA-256 hex digest of the given plain-text password."""
        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    @staticmethod
    def login(email, password):
        """Authenticate a user by email and password.

        Returns the user row on success, or None if credentials are invalid.
        """
        user = UserModel.get_user_by_email(email)

        if not user:
            return None

        hashed_password = AuthService.hash_password(password)

        if user["password"] != hashed_password:
            return None

        return user
