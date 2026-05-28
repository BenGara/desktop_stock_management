"""Modèle de gestion de la création et de la récupération des utilisateurs."""

from database import get_connection


class UserModel:
    """Fournit des méthodes pour gérer les utilisateurs de l'application."""

    # Méthodes de création d'utilisateur
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
            (firstname,lastname,email,password,role_id)
        )

        connection.commit()
        connection.close()

    # Méthodes de récupération d'utilisateur
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
    
    @staticmethod
    def get_all_users():
        """Renvoie une liste de tous les utilisateurs."""
        connection = get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()
        
        cursor.execute("SELECT users.id, users.firstname, users.lastname, users.email, roles.name AS role FROM users INNER JOIN roles ON users.role_id = roles.id")
        users = cursor.fetchall()

        cursor.close()
        connection.close()
        return users
    
    @staticmethod
    def get_all_role_names():
        """Récupère la liste de tous les noms de rôles existants."""
        connection = get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM roles")
        roles = [row[0] for row in cursor.fetchall()] 
        
        connection.close()
        return roles
    
    @staticmethod
    def update_user(user_id, firstname, lastname, email, role_id):
        """Met à jour les informations d'un utilisateur dans la base de données."""
        connection = get_connection()

        connection.execute(
            '''
            UPDATE users
            SET firstname = ?, lastname = ?, email = ?, role_id = ?
            WHERE id = ?
            ''',
            (
                firstname,
                lastname,
                email,
                role_id,
                user_id
            )
        )

        connection.commit()
        connection.close()
        
    @staticmethod
    def modification_mdp(user_id, new_password):
        """Met à jour le mot de passe d'un utilisateur dans la base de données."""
        connection = get_connection()

        connection.execute(
            '''
            UPDATE users
            SET password = ?
            WHERE id = ?
            ''',
            (new_password,user_id)
        )

        connection.commit()
        connection.close()
    
    # Méthodes de suppression d'utilisateur
    @staticmethod
    def delete_user(user_id):
        """Supprime un utilisateur de la base de données."""
        connection = get_connection()

        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        connection.commit()
        connection.close()