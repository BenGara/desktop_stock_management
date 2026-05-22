"""Model handling material assignment operations."""

from database import get_connection


class AssignmentModel:
    """Provides static methods to manage material assignments."""

    @staticmethod
    def assign_material(material_id, employee_id):
        """Assign a material to an employee.

        Raises ValueError if the material does not exist, is broken,
        or is already assigned to someone else.
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
        """Return all active assignments from the database."""
        connection = get_connection()

        assignments = connection.execute(
            "SELECT * FROM assignments WHERE active = 1"
        ).fetchall()

        connection.close()

        return assignments
