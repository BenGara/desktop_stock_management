"""Tests unitaires pour CategorieModel et CategorieService."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.categorie_model import CategorieModel
from services.categorie_service import CategorieService


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        );
        INSERT INTO categories(name, description) VALUES
            ('Laptop',   'Ordinateurs portables'),
            ('Monitor',  'Écrans'),
            ('Printer',  'Imprimantes');
    """)
    return conn


class TestBase(unittest.TestCase):
    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)


class TestCategorieModel(TestBase):
    """Tests directs sur CategorieModel."""

    def test_create_category(self):
        CategorieModel.create_category("Serveur", "Serveurs rack")
        self.assertTrue(CategorieModel.is_category_name_exists("Serveur"))

    def test_is_category_name_exists_trouve_existant(self):
        self.assertTrue(CategorieModel.is_category_name_exists("Laptop"))

    def test_is_category_name_exists_absent_retourne_false(self):
        self.assertFalse(CategorieModel.is_category_name_exists("Catégorie Inexistante"))

    def test_is_category_name_exists_avec_exclusion(self):
        cats = CategorieModel.get_all_categories()
        laptop = [c for c in cats if c[1] == "Laptop"][0]
        self.assertFalse(CategorieModel.is_category_name_exists("Laptop", exclude_id=laptop[0]))

    def test_get_all_categories_retourne_liste(self):
        """get_all_categories doit renvoyer exactement les 3 catégories de la fixture."""
        cats = CategorieModel.get_all_categories()
        self.assertIsInstance(cats, list)
        self.assertEqual(len(cats), 3)

    def test_update_category(self):
        cats = CategorieModel.get_all_categories()
        cat_id = cats[0][0]
        CategorieModel.update_category(cat_id, "Laptop Pro", "Portables pro")
        cats_after = CategorieModel.get_all_categories()
        updated = [c for c in cats_after if c[0] == cat_id][0]
        self.assertEqual(updated[1], "Laptop Pro")

    def test_delete_category(self):
        CategorieModel.create_category("Temporaire", "À supprimer")
        cats = CategorieModel.get_all_categories()
        cat_id = [c for c in cats if c[1] == "Temporaire"][0][0]
        CategorieModel.delete_category(cat_id)
        self.assertFalse(CategorieModel.is_category_name_exists("Temporaire"))


class TestCategorieService(TestBase):
    """Tests des validations métier dans CategorieService."""

    def test_ajouter_categorie_valide(self):
        CategorieService.ajouter_categorie("Switch Réseau", "Équipements réseau")
        self.assertTrue(CategorieModel.is_category_name_exists("Switch Réseau"))

    def test_ajouter_categorie_nom_vide_leve_erreur(self):
        with self.assertRaises(ValueError) as ctx:
            CategorieService.ajouter_categorie("  ", "Description")
        self.assertIn("obligatoire", str(ctx.exception))

    def test_ajouter_categorie_doublon_leve_erreur(self):
        """Ajouter une catégorie au nom déjà existant doit lever ValueError."""
        with self.assertRaises(ValueError) as ctx:
            CategorieService.ajouter_categorie("Laptop", "Doublon")
        self.assertIn("existe déjà", str(ctx.exception))

    def test_modifier_categorie_sans_id_leve_erreur(self):
        with self.assertRaises(ValueError):
            CategorieService.modifier_categorie(None, "Nom", "Desc")

    def test_modifier_categorie_nom_vide_leve_erreur(self):
        cats = CategorieModel.get_all_categories()
        cat_id = cats[0][0]
        with self.assertRaises(ValueError):
            CategorieService.modifier_categorie(cat_id, "   ", "Desc")

    def test_modifier_categorie_doublon_leve_erreur(self):
        cats = CategorieModel.get_all_categories()
        laptop = [c for c in cats if c[1] == "Laptop"][0]
        with self.assertRaises(ValueError):
            CategorieService.modifier_categorie(laptop[0], "Monitor", "Desc")

    def test_supprimer_categorie_sans_id_leve_erreur(self):
        with self.assertRaises(ValueError):
            CategorieService.supprimer_categorie(None)

    def test_obtenir_toutes_categories_formate_nom(self):
        categories = CategorieService.obtenir_toutes_categories()
        for _, nom, _ in categories:
            self.assertEqual(nom, nom.capitalize())


if __name__ == "__main__":
    unittest.main()
