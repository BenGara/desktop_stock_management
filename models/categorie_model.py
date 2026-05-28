"""Modèle de gestion de la création et de la récupération des données pour les catégories."""

from multiprocessing import connection
from database import get_connection

class CategorieModel:
    """Fournit des méthodes pour gérer les catégories de matériels en stock."""

    @staticmethod
    def create_categorie(name, description):
        """Insère une nouvelle catégorie dans la base de données.

        Génère une erreur ValueError si le nom de catégorie existe déjà.
        """
        connection = get_connection()

        existing = connection.execute(
            "SELECT * FROM categories WHERE name = ?",
            (name,)
        ).fetchone()

        if existing:
            connection.close()
            raise ValueError("Category name already exists")

        connection.execute(
            '''
            INSERT INTO categories(name, description)
            VALUES (?, ?)
            ''',
            (name, description)
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_categories():
        """Renvoie toutes les catégories de la base de données."""
        connection = get_connection()
        
        connection.row_factory = None 
        
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, description FROM categories")
        categories = cursor.fetchall()

        connection.close()
        
        return categories
    
    @staticmethod
    def update_categorie(category_id, new_name, new_description):
        """Met à jour le nom et la description d'une catégorie dans la base de données.

        Génère une erreur ValueError si le nouveau nom ou la nouvelle description de catégorie existe déjà.
        """
        connection = get_connection()

        existing = connection.execute(
            "SELECT * FROM categories WHERE (name = ? OR description = ?) AND id != ?",
            (new_name, new_description, category_id)
        ).fetchone()

        if existing:
            connection.close()
            raise ValueError("Category name or description already exists")

        connection.execute(
            '''
            UPDATE categories
            SET name = ?, description = ?
            WHERE id = ?
            ''',
            (new_name, new_description, category_id)
        )

        connection.commit()
        connection.close()
    
    @staticmethod
    def delete_categorie(category_id):
        """Supprime une catégorie de la base de données."""
        connection = get_connection()
        
        connection.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )

        connection.commit()
        connection.close()