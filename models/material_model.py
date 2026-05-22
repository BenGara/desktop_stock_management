"""Modèle de gestion de la création et de la récupération des données."""

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

        materials = connection.execute(
            "SELECT * FROM materials"
        ).fetchall()

        connection.close()

        return materials
