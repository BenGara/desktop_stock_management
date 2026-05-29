"""Tests unitaires pour BreakdownModel — gestion des pannes."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.breakdown_model import BreakdownModel


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
        CREATE TABLE breakdowns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            reported_by INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(material_id) REFERENCES materials(id),
            FOREIGN KEY(reported_by) REFERENCES users(id)
        );
        INSERT INTO roles(name) VALUES ('ADMIN');
        INSERT INTO categories(name, description) VALUES ('Laptop', 'Portables');
        INSERT INTO users(firstname, lastname, email, password, role_id)
            VALUES ('Admin', 'Sys', 'admin@test.local', 'hash', 1);
        INSERT INTO materials(name, serial_number, category_id, quantity, status, purchase_date) VALUES
            ('Dell Latitude', 'SN-001', 1, 5, 'available', '2024-01-01'),
            ('LG Monitor',   'SN-002', 1, 2, 'available', '2024-02-01');
    """)
    return conn


class TestBase(unittest.TestCase):
    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)


class TestDeclareBreakdown(TestBase):
    """Tests d'enregistrement de pannes."""

    def test_declaration_panne_valide(self):
        BreakdownModel.declare_breakdown(1, 1, "Écran cassé")
        pannes = BreakdownModel.get_all_breakdowns()
        self.assertGreater(len(pannes), 0)

    def test_declaration_panne_change_statut_materiel(self):
        """Après déclaration de panne, le statut du matériel doit devenir 'broken'."""
        BreakdownModel.declare_breakdown(1, 1, "Clavier défaillant")
        mat = self._conn.execute("SELECT status FROM materials WHERE id = 1").fetchone()
        self.assertEqual(mat["status"], "broken")

    def test_plusieurs_pannes_enregistrees(self):
        BreakdownModel.declare_breakdown(1, 1, "Panne 1")
        BreakdownModel.declare_breakdown(2, 1, "Panne 2")
        pannes = BreakdownModel.get_all_breakdowns()
        self.assertGreaterEqual(len(pannes), 2)

    def test_description_panne_stockee(self):
        """La description de la panne doit être correctement stockée en base."""
        BreakdownModel.declare_breakdown(1, 1, "Description précise de la panne")
        panne = self._conn.execute(
            "SELECT description FROM breakdowns WHERE material_id = 1 ORDER BY id DESC LIMIT 1"
        ).fetchone()
        self.assertEqual(panne["description"], "Description précise de la panne")


class TestGetAllBreakdowns(TestBase):
    """Tests de récupération des pannes."""

    def test_get_all_breakdowns_retourne_liste_vide_si_aucune(self):
        """Sans panne enregistrée, get_all_breakdowns doit renvoyer une liste vide."""
        pannes = BreakdownModel.get_all_breakdowns()
        self.assertEqual(len(pannes), 0)

    def test_get_all_breakdowns_retourne_toutes_les_pannes(self):
        """Après 2 insertions, get_all_breakdowns doit renvoyer exactement 2 entrées."""
        BreakdownModel.declare_breakdown(1, 1, "Panne A")
        BreakdownModel.declare_breakdown(2, 1, "Panne B")
        pannes = BreakdownModel.get_all_breakdowns()
        self.assertEqual(len(pannes), 2)


if __name__ == "__main__":
    unittest.main()
