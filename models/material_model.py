"""Modèle de gestion de la création et de la récupération des données."""

import database


class MaterialModel:
    """Fournit des méthodes pour gérer les matériels en stock."""

    @staticmethod
    def is_serial_number_exists(serial_number, exclude_id=None):
        """Vérifie si un numéro de série existe déjà en base de données."""
        connection = database.get_connection()
        if exclude_id:
            query = "SELECT 1 FROM materials WHERE serial_number = ? AND id != ?"
            existing = connection.execute(query, (serial_number, exclude_id)).fetchone()
        else:
            query = "SELECT 1 FROM materials WHERE serial_number = ?"
            existing = connection.execute(query, (serial_number,)).fetchone()
        return existing is not None

    @staticmethod
    def create_material(name, serial_number, category_id, quantity, status, purchase_date):
        """Insère un nouveau matériel dans la base de données."""
        connection = database.get_connection()
        connection.execute(
            '''
            INSERT INTO materials(name, serial_number, category_id, quantity, status, purchase_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (name, serial_number, category_id, quantity, status, purchase_date)
        )
        connection.commit()
    @staticmethod
    def get_all_materials():
        """Renvoie tous les matériels de la base de données."""
        connection = database.get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()

        cursor.execute("SELECT materials.id, materials.name, materials.serial_number, categories.name AS category_name, materials.quantity, materials.status, materials.purchase_date FROM materials INNER JOIN categories ON materials.category_id = categories.id")
        materials = cursor.fetchall()

        cursor.close()
        return materials
    
    @staticmethod
    def get_all_categories_names():
        """Renvoie tous les noms de catégories de la base de données."""
        connection = database.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return categories
        
    @staticmethod
    def update_material_full(material_id, name, serial_number, category_id, quantity, status, purchase_date):
        """Met à jour l'ensemble des informations d'un matériel dans la base de données."""
        connection = database.get_connection()
        connection.execute(
            '''
            UPDATE materials 
            SET name = ?, serial_number = ?, category_id = ?, quantity = ?, status = ?, purchase_date = ?
            WHERE id = ?
            ''',
            (name, serial_number, category_id, quantity, status, purchase_date, material_id)
        )
        connection.commit()
                
    @staticmethod
    def delete_material(material_id):
        """Supprime un matériel de la base de données."""
        connection = database.get_connection()
        connection.execute("DELETE FROM materials WHERE id = ?", (material_id,))
        connection.commit()
