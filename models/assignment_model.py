"""Modèle de gestion des opérations d'affectation des matériels."""

from database import get_connection


class AssignmentModel:
    """Fournit des méthodes pour gérer les affectations des matériels."""

    @staticmethod
    def assign_material(material_id, employee_id):
        """Attribue un matériel à un employé.

        Génère une erreur ValueError si le matériel n'existe pas, est cassé
        ou est déjà attribué à quelqu'un d'autre.
        """
        connection = get_connection()

        material = connection.execute(
            "SELECT * FROM materials WHERE id = ?",
            (material_id,)
        ).fetchone()

        if not material:
            connection.close()
            raise ValueError("Material not found")

        if material["status"] == "broken":
            connection.close()
            raise ValueError(
                "Broken material cannot be assigned"
            )

        existing_assignment = connection.execute(
            '''
            SELECT * FROM assignments
            WHERE material_id = ?
            AND active = 1
            ''',
            (material_id,)
        ).fetchone()

        if existing_assignment:
            connection.close()
            raise ValueError(
                "Material already assigned"
            )

        connection.execute(
            '''
            INSERT INTO assignments(
                material_id,
                employee_id
            )
            VALUES (?, ?)
            ''',
            (material_id, employee_id)
        )

        connection.execute(
            '''
            UPDATE materials
            SET status = 'assigned'
            WHERE id = ?
            ''',
            (material_id,)
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_assignments():
        """Renvoie toutes les affectations actives de la base de données."""
        connection = get_connection()

        assignments = connection.execute(
            "SELECT * FROM assignments WHERE active = 1"
        ).fetchall()

        connection.close()

        return assignments
