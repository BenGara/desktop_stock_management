"""Modèle de gestion des opérations d'affectation des matériels."""

import database


class AssignmentModel:
    """Fournit des méthodes pour gérer les affectations des matériels."""

    @staticmethod
    def assign_material(material_id, employee_id):
        """Attribue un matériel à un employé.

        Génère une erreur ValueError si le matériel n'existe pas, est cassé
        ou est déjà attribué à quelqu'un d'autre.
        """
        connection = database.get_connection()

        material = connection.execute(
            "SELECT * FROM materials WHERE id = ?",
            (material_id,)
        ).fetchone()

        if not material:
                raise ValueError("Material not found")

        if material["status"] == "broken":
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
    @staticmethod
    def get_all_assignments():
        """Renvoie toutes les affectations actives de la base de données."""
        connection = database.get_connection()

        assignments = connection.execute(
            "SELECT * FROM assignments WHERE active = 1"
        ).fetchall()

        return assignments
    
    # À intégrer dans ton modèle de gestion des affectations/matériels
    @staticmethod
    def get_active_assignments():
        """Renvoie la liste des matériels actuellement affectés (non retournés)."""
        connection = database.get_connection()
        cursor = connection.cursor()
        # Jointure pour avoir des infos claires à l'écran (Nom utilisateur, Nom Matériel, Numéro de série)
        query = """
            SELECT a.id, u.firstname || ' ' || u.lastname AS utilisateur, m.name, m.serial_number, a.assignment_date
            FROM assignments a
            INNER JOIN users u ON a.user_id = u.id
            INNER JOIN materials m ON a.material_id = m.id
            WHERE a.active = 1
        """
        cursor.execute(query)
        assignments = cursor.fetchall()
        return assignments

    @staticmethod
    def process_material_return(assignment_id, material_status):
        """Clôture l'affectation et met à jour le statut du matériel."""
        connection = database.get_connection()
        cursor = connection.cursor()
        
        # 1. On récupère le material_id lié à cette affectation avant de la clôturer
        cursor.execute("SELECT material_id FROM assignments WHERE id = ?", (assignment_id,))
        row = cursor.fetchone()
        if not row:
                raise ValueError("Affectation introuvable.")
        material_id = row[0]

        # 2. On passe l'affectation à inactive
        cursor.execute("UPDATE assignments SET active = 0 WHERE id = ?", (assignment_id,))
        
        # 3. On met à jour le statut du matériel (ex: 'Disponible' ou 'En panne')
        cursor.execute("UPDATE materials SET status = ? WHERE id = ?", (material_status, material_id))
        
        # 4. Optionnel : Si le matériel est déclaré en panne, on l'ajoute à la table breakdowns
        if material_status == "En panne":
            cursor.execute(
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
                    1,
                    "Retour en panne"
                )
            )

        connection.commit()
