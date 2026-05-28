"""Modèle de gestion de la création et de la récupération des données."""

from multiprocessing import connection

from database import get_connection


class MaterialModel:
    """Fournit des méthodes pour gérer les matériels en stock."""

    @staticmethod
    def create_material(name, serial_number, category_id, quantity):
        """Insère un nouveau matériel dans la base de données.

        Génère une erreur ValueError si le numéro de série existe déjà.
        """
        connection = get_connection()

        existing = connection.execute(
            "SELECT * FROM materials WHERE serial_number = ?",
            (serial_number,)
        ).fetchone()

        if existing:
            connection.close()
            raise ValueError("Serial number already exists")

        connection.execute(
            '''
            INSERT INTO materials(
                name,
                serial_number,
                category_id,
                quantity
            )
            VALUES (?, ?, ?, ?)
            ''',
            (
                name,
                serial_number,
                category_id,
                quantity
            )
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_materials():
        """Renvoie tous les matériels de la base de données."""
        connection = get_connection()
        
        connection.row_factory = None 
        
        cursor = connection.cursor()


        cursor.execute("SELECT materials.id, materials.name, materials.serial_number, categories.name AS category_name, materials.quantity, materials.status, materials.purchase_date FROM materials INNER JOIN categories ON materials.category_id = categories.id")
        materials = cursor.fetchall()

        cursor.close()
        connection.close()

        return materials
    
    @staticmethod
    def get_all_categories_names():
        """Renvoie tous les noms de catégories de la base de données."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return categories

    @staticmethod
    def delete_material(material_id):
        """Supprime un matériel de la base de données."""
        connection = get_connection()
        
        connection.execute(
            "DELETE FROM materials WHERE id = ?",
            (material_id,)
        )

        connection.commit()
        connection.close()
        
    @staticmethod
    def update_material(material_id, new_status):
        """Met à jour le statut d'un matériel dans la base de données."""
        connection = get_connection()
        
        connection.execute(
            "UPDATE materials SET status = ? WHERE id = ?",
            (new_status, material_id)
        )

        connection.commit()
        connection.close()