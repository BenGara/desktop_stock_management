"""Tests unitaires pour AssignmentModel — règles de gestion des affectations."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.assignment_model import AssignmentModel


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(role_id) REFERENCES roles(id)
        );
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        );
        CREATE TABLE materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            quantity INTEGER DEFAULT 0,
            status TEXT DEFAULT 'available',
            purchase_date TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );
        CREATE TABLE assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
            returned_at TEXT,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(material_id) REFERENCES materials(id),
            FOREIGN KEY(employee_id) REFERENCES users(id)
        );
        CREATE TABLE breakdowns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            reported_by INTEGER,
            description TEXT,
            status TEXT DEFAULT 'open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(material_id) REFERENCES materials(id)
        );
        INSERT INTO roles(name) VALUES ('ADMIN'), ('MANAGER'), ('EMPLOYEE');
        INSERT INTO categories(name, description) VALUES ('Laptop', 'Portables');
        INSERT INTO users(firstname, lastname, email, password, role_id)
            VALUES ('Alice', 'Dupont', 'alice@test.local', 'hash', 1);
        -- id=1 : disponible, id=2 : en panne, id=3 : déjà affecté
        INSERT INTO materials(name, serial_number, category_id, quantity, status, purchase_date) VALUES
            ('Dell Latitude', 'SN-AVAIL-001',  1, 5, 'available', '2024-01-01'),
            ('LG Monitor',   'SN-BROKEN-002', 1, 1, 'broken',    '2024-02-01'),
            ('HP Printer',   'SN-ASSIGN-003', 1, 1, 'assigned',  '2024-03-01');
        -- Affectation active existante pour le matériel id=3
        INSERT INTO assignments(material_id, employee_id, active) VALUES (3, 1, 1);
    """)
    return conn


class TestBase(unittest.TestCase):
    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)


class TestAssignMaterial(TestBase):
    """Vérifie les règles métier lors de l'affectation d'un matériel."""

    def test_affectation_materiel_disponible(self):
        """Un matériel avec status='available' doit pouvoir être affecté sans erreur."""
        AssignmentModel.assign_material(1, 1)
        assignments = AssignmentModel.get_all_assignments()
        material_ids = [a["material_id"] for a in assignments]
        self.assertIn(1, material_ids)

    def test_affectation_materiel_en_panne_interdit(self):
        """Un matériel avec status='broken' doit lever ValueError."""
        with self.assertRaises(ValueError) as ctx:
            AssignmentModel.assign_material(2, 1)
        self.assertIn("broken", str(ctx.exception).lower())

    def test_affectation_double_interdit(self):
        """Un matériel déjà affecté doit lever ValueError."""
        with self.assertRaises(ValueError) as ctx:
            AssignmentModel.assign_material(3, 1)
        self.assertIn("already assigned", str(ctx.exception).lower())

    def test_affectation_materiel_inexistant(self):
        """Un material_id inexistant doit lever ValueError."""
        with self.assertRaises(ValueError) as ctx:
            AssignmentModel.assign_material(9999, 1)
        self.assertIn("not found", str(ctx.exception).lower())

    def test_affectation_change_statut_en_assigned(self):
        """Après affectation, le statut du matériel doit passer à 'assigned'."""
        AssignmentModel.assign_material(1, 1)
        mat = self._conn.execute("SELECT status FROM materials WHERE id = 1").fetchone()
        self.assertEqual(mat["status"], "assigned")


class TestGetAllAssignments(TestBase):
    """Tests de récupération des affectations."""

    def test_get_all_assignments_retourne_liste(self):
        result = AssignmentModel.get_all_assignments()
        self.assertIsInstance(result, list)

    def test_get_all_assignments_contient_actif(self):
        """La fixture insère 1 affectation active ; elle doit apparaître."""
        result = AssignmentModel.get_all_assignments()
        self.assertEqual(len(result), 1)

    def test_get_all_assignments_uniquement_actifs(self):
        """get_all_assignments ne doit retourner que les affectations actives."""
        self._conn.execute("UPDATE assignments SET active = 0 WHERE id = 1")
        self._conn.commit()
        result = AssignmentModel.get_all_assignments()
        self.assertEqual(len(result), 0)


class TestProcessMaterialReturn(TestBase):
    """Tests du retour de matériel."""

    def test_retour_cloture_affectation(self):
        """Après retour, l'affectation doit être inactive (active=0)."""
        AssignmentModel.process_material_return(1, "Disponible")
        aff = self._conn.execute("SELECT active FROM assignments WHERE id = 1").fetchone()
        self.assertEqual(aff["active"], 0)

    def test_retour_met_a_jour_statut_materiel(self):
        """Après retour, le statut du matériel doit correspondre au statut déclaré."""
        AssignmentModel.process_material_return(1, "Disponible")
        mat = self._conn.execute("SELECT status FROM materials WHERE id = 3").fetchone()
        self.assertEqual(mat["status"], "Disponible")

    def test_retour_affectation_inexistante_leve_erreur(self):
        """process_material_return avec un ID invalide doit lever ValueError."""
        with self.assertRaises(ValueError):
            AssignmentModel.process_material_return(9999, "Disponible")

    def test_retour_en_panne_cree_enregistrement_breakdown(self):
        """Si l'état au retour est 'En panne', un enregistrement breakdown doit être créé."""
        AssignmentModel.process_material_return(1, "En panne")
        breakdown = self._conn.execute(
            "SELECT * FROM breakdowns WHERE material_id = 3"
        ).fetchone()
        self.assertIsNotNone(breakdown)


if __name__ == "__main__":
    unittest.main()
