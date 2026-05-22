"""Modèle de gestion des déclarations des pannes des matériels."""

from database import get_connection


class BreakdownModel:
    """Fournit des méthodes pour gérer les pannes des matériels."""

    @staticmethod
    def declare_breakdown(material_id, reported_by, description):
        """Enregistre une panne pour un matériel
        et le note comme défectueux.
        """
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
        """Renvoie tous les enregistrements de pannes de la base de données."""
        connection = get_connection()

        breakdowns = connection.execute(
            "SELECT * FROM breakdowns"
        ).fetchall()

        connection.close()

        return breakdowns
