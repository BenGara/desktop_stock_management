"""Model handling material breakdown declarations."""

from database import get_connection


class BreakdownModel:
    """Provides static methods to manage material breakdowns."""

    @staticmethod
    def declare_breakdown(material_id, reported_by, description):
        """Record a breakdown for a material and mark it as broken."""
        connection = get_connection()

        connection.execute(
            '''
            INSERT INTO breakdowns(
                material_id,
                reported_by,
                description
            )
            VALUES (?, ?, ?)
            ''',
            (
                material_id,
                reported_by,
                description
            )
        )

        connection.execute(
            '''
            UPDATE materials
            SET status = 'broken'
            WHERE id = ?
            ''',
            (material_id,)
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_breakdowns():
        """Return all breakdown records from the database."""
        connection = get_connection()

        breakdowns = connection.execute(
            "SELECT * FROM breakdowns"
        ).fetchall()

        connection.close()

        return breakdowns
