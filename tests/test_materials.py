"""Tests unitaires pour MaterialModel."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.material_model import MaterialModel


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
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
        INSERT INTO categories(name, description) VALUES
            ('Laptop', 'Ordinateurs portables'),
            ('Monitor', 'Écrans'),
            ('Printer', 'Imprimantes');
        INSERT INTO materials(name, serial_number, category_id, quantity, status, purchase_date) VALUES
            ('Dell Latitude', 'SN-AVAIL-001', 1, 5, 'available', '2024-01-01'),
            ('LG Monitor',   'SN-BROKEN-002', 2, 1, 'broken',    '2024-02-01'),
            ('HP Printer',   'SN-ASSIGN-003', 3, 1, 'assigned',  '2024-03-01');
    """)
    return conn


class TestBase(unittest.TestCase):
    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)


class TestMaterialModelCreation(TestBase):
    """Tests de création de matériel."""

    def test_creation_materiel_valide(self):
        MaterialModel.create_material("Clavier Logitech", "SN-NEW-001", 1, 3, "available", "2024-05-01")
        self.assertTrue(MaterialModel.is_serial_number_exists("SN-NEW-001"))

    def test_serial_number_unique_detecte_existant(self):
        self.assertTrue(MaterialModel.is_serial_number_exists("SN-AVAIL-001"))

    def test_serial_number_inexistant_retourne_false(self):
        self.assertFalse(MaterialModel.is_serial_number_exists("SN-AUCUN-999"))

    def test_serial_number_unique_avec_exclusion(self):
        # SN-AVAIL-001 appartient au matériel id=1 ; l'exclure doit renvoyer False
        self.assertFalse(MaterialModel.is_serial_number_exists("SN-AVAIL-001", exclude_id=1))

    def test_creation_double_serial_leve_exception(self):
        """Insérer deux fois le même numéro de série doit lever IntegrityError."""
        with self.assertRaises(sqlite3.IntegrityError):
            self._conn.execute(
                "INSERT INTO materials(name, serial_number, category_id, quantity, status, purchase_date) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("Doublon", "SN-AVAIL-001", 1, 1, "available", "2024-01-01")
            )


class TestMaterialModelLecture(TestBase):
    """Tests de récupération des matériels."""

    def test_get_all_materials_retourne_liste(self):
        materials = MaterialModel.get_all_materials()
        self.assertIsInstance(materials, list)

    def test_get_all_materials_contient_les_seeds(self):
        """La liste doit contenir les 3 matériels insérés en fixture."""
        materials = MaterialModel.get_all_materials()
        self.assertEqual(len(materials), 3)

    def test_get_all_categories_names_retourne_liste(self):
        cats = MaterialModel.get_all_categories_names()
        self.assertIsInstance(cats, list)
        self.assertGreater(len(cats), 0)


class TestMaterialModelMiseAJour(TestBase):
    """Tests de mise à jour et suppression."""

    def test_update_material_modifie_les_donnees(self):
        materials = MaterialModel.get_all_materials()
        mat_id = materials[0][0]
        MaterialModel.update_material_full(mat_id, "Dell Latitude PRO", "SN-AVAIL-001", 1, 10, "available", "2024-01-15")
        updated = [m for m in MaterialModel.get_all_materials() if m[0] == mat_id]
        self.assertEqual(updated[0][1], "Dell Latitude PRO")

    def test_delete_material_supprime_la_ligne(self):
        MaterialModel.create_material("Souris Temp", "SN-DEL-999", 1, 1, "available", "2024-01-01")
        self.assertTrue(MaterialModel.is_serial_number_exists("SN-DEL-999"))
        materials = MaterialModel.get_all_materials()
        mat_id = [m for m in materials if m[2] == "SN-DEL-999"][0][0]
        MaterialModel.delete_material(mat_id)
        self.assertFalse(MaterialModel.is_serial_number_exists("SN-DEL-999"))


if __name__ == "__main__":
    unittest.main()
