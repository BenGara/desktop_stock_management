"""Modèle de gestion de la création et de la récupération des utilisateurs."""

from database import get_connection


class UserModel:
    """Fournit des méthodes pour gérer les utilisateurs de l'application."""

    @staticmethod
    def create_user(firstname, lastname, email, password, role_id):
        """Ajoute un nouvel utilisateur dans la base de données."""
        connection = get_connection()

        connection.execute(
            '''
            INSERT INTO users(
                firstname,
                lastname,
                email,
                password,
                role_id
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (
                firstname,
                lastname,
                email,
                password,
                role_id
            )
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_user_by_email(email):
        """Renvoie la ligne correspondant à
        l'adresse e-mail indiquée, ou None.
        """
        connection = get_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        return user
