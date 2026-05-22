"""Model handling user creation and retrieval."""

from database import get_connection


class UserModel:
    """Provides static methods to manage application users."""

    @staticmethod
    def create_user(firstname, lastname, email, password, role_id):
        """Insert a new user into the database."""
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
        """Return the user row matching the given email, or None."""
        connection = get_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        return user
