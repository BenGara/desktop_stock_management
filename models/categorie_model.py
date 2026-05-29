"""Modèle pour la gestion des catégories en base de données."""

import database

class CategorieModel:
    """Fournit les méthodes SQL pour interagir avec la table des catégories."""

    @staticmethod
    def is_category_name_exists(name, exclude_id=None):
        """Vérifie si un nom de catégorie existe déjà en base de données."""
        connection = database.get_connection()
        if exclude_id:
            query = "SELECT 1 FROM categories WHERE name = ? AND id != ?"
            existing = connection.execute(query, (name, exclude_id)).fetchone()
        else:
            query = "SELECT 1 FROM categories WHERE name = ?"
            existing = connection.execute(query, (name,)).fetchone()
        return existing is not None

    @staticmethod
    def create_category(name, description):
        """Insère une nouvelle catégorie dans la base de données."""
        connection = database.get_connection()
        connection.execute(
            '''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            ''',
            (name, description)
        )
        connection.commit()
    @staticmethod
    def get_all_categories():
        """Récupère toutes les catégories de la base de données."""
        connection = database.get_connection()
        connection.row_factory = None
        cursor = connection.cursor()
        
        cursor.execute("SELECT id, name, description FROM categories")
        categories = cursor.fetchall()
        
        cursor.close()
        return categories

    @staticmethod
    def update_category(category_id, name, description):
        """Met à jour une catégorie existante."""
        connection = database.get_connection()
        connection.execute(
            '''
            UPDATE categories
            SET name = ?, description = ?
            WHERE id = ?
            ''',
            (name, description, category_id)
        )
        connection.commit()
    @staticmethod
    def delete_category(category_id):
        """Supprime une catégorie de la base de données."""
        connection = database.get_connection()
        connection.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        connection.commit()
