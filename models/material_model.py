"""Model handling material creation and retrieval."""

from database import get_connection


class MaterialModel:
    """Provides static methods to manage stock materials."""

    @staticmethod
    def create_material(name, serial_number, category_id, quantity):
        """Insert a new material into the database.

        Raises ValueError if the serial number already exists.
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
        """Return all materials from the database."""
        connection = get_connection()

        materials = connection.execute(
            "SELECT * FROM materials"
        ).fetchall()

        connection.close()

        return materials
