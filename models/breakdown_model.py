import database

class BreakdownModel:
    """Gère la table 'breakdowns' et l'historique des pannes."""

    @staticmethod
    def declare_breakdown(material_id, description):
        """Enregistre une nouvelle panne et bascule le matériel en statut 'EN_PANNE'."""
        connection = database.get_connection()
        cursor = connection.cursor()
        try:
            # 1. Insérer la panne
            cursor.execute(
                '''
                INSERT INTO breakdowns (material_id, description, status, report_date)
                VALUES (?, ?, 'EN_COURS', DATE('now'))
                ''',
                (material_id, description)
            )
            # 2. Mettre à jour le statut du matériel concerné
            cursor.execute("UPDATE materials SET status = 'EN_PANNE' WHERE id = ?", (material_id,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_all_breakdowns():
        """Récupère la liste des pannes avec les détails du matériel."""
        connection = database.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT b.id, m.name, m.serial_number, b.description, b.status, b.report_date, b.material_id
            FROM breakdowns b
            INNER JOIN materials m ON b.material_id = m.id
            '''
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @staticmethod
    def update_breakdown_status(breakdown_id, material_id, new_status):
        """Met à jour le statut d'une panne et répercute le changement sur le matériel."""
        connection = database.get_connection()
        cursor = connection.cursor()
        try:
            # 1. Mise à jour de la panne
            cursor.execute("UPDATE breakdowns SET status = ? WHERE id = ?", (new_status, breakdown_id))
            
            # 2. Répercussion intelligente sur le matériel
            if new_status == "REPARE":
                cursor.execute("UPDATE materials SET status = 'EN_STOCK' WHERE id = ?", (material_id,))
            elif new_status == "MIS_HORS_SERVICE":
                cursor.execute("UPDATE materials SET status = 'HORS_SERVICE' WHERE id = ?", (material_id,))
                
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()