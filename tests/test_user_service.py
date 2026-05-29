"""Tests unitaires pour UserModel et UserService."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import UserModel
from services.user_service import UserService
from services.auth_service import AuthService


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
        INSERT INTO roles(name) VALUES ('ADMIN'), ('MANAGER'), ('EMPLOYEE');
        -- Mot de passe : admin123
        INSERT INTO users(firstname, lastname, email, password, role_id)
        VALUES ('Alice', 'Dupont', 'alice@test.local',
                '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1);
    """)
    return conn


class TestBase(unittest.TestCase):
    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)


class TestUserModel(TestBase):
    """Tests directs sur UserModel."""

    def test_create_user_valide(self):
        UserModel.create_user("Bob", "Martin", "bob@test.local",
                               AuthService.hash_password("bob123"), 3)
        user = UserModel.get_user_by_email("bob@test.local")
        self.assertIsNotNone(user)

    def test_get_user_by_email_trouve(self):
        """get_user_by_email doit renvoyer Alice pour alice@test.local."""
        user = UserModel.get_user_by_email("alice@test.local")
        self.assertIsNotNone(user)
        self.assertEqual(user["firstname"], "Alice")

    def test_get_user_by_email_inexistant_retourne_none(self):
        user = UserModel.get_user_by_email("nope@test.local")
        self.assertIsNone(user)

    def test_get_all_users_retourne_liste(self):
        users = UserModel.get_all_users()
        self.assertIsInstance(users, list)
        self.assertGreaterEqual(len(users), 1)

    def test_get_all_role_names_retourne_liste(self):
        roles = UserModel.get_all_role_names()
        self.assertIn("ADMIN", roles)
        self.assertIn("EMPLOYEE", roles)

    def test_update_user_modifie_donnees(self):
        user = UserModel.get_user_by_email("alice@test.local")
        UserModel.update_user(user["id"], "Alicia", "Durand", "alice@test.local", 3)
        updated = UserModel.get_user_by_email("alice@test.local")
        self.assertEqual(updated["firstname"], "Alicia")

    def test_modification_mdp_change_mot_de_passe(self):
        user = UserModel.get_user_by_email("alice@test.local")
        new_hash = AuthService.hash_password("nouveauMdp!")
        UserModel.modification_mdp(user["id"], new_hash)
        updated = UserModel.get_user_by_email("alice@test.local")
        self.assertEqual(updated["password"], new_hash)

    def test_delete_user_supprime_utilisateur(self):
        UserModel.create_user("Temp", "User", "temp@test.local",
                               AuthService.hash_password("temp"), 3)
        user = UserModel.get_user_by_email("temp@test.local")
        UserModel.delete_user(user["id"])
        self.assertIsNone(UserModel.get_user_by_email("temp@test.local"))


class TestUserService(TestBase):
    """Tests des validations métier dans UserService."""

    def test_inscrire_utilisateur_valide(self):
        UserService.inscrire_utilisateur("Clara", "Dupont", "clara@test.local", "pass123", "Employee")
        user = UserModel.get_user_by_email("clara@test.local")
        self.assertIsNotNone(user)

    def test_inscrire_champ_vide_leve_erreur(self):
        with self.assertRaises(ValueError) as ctx:
            UserService.inscrire_utilisateur("", "Dupont", "x@x.com", "pass", "Employee")
        self.assertIn("remplis", str(ctx.exception))

    def test_inscrire_mdp_vide_leve_erreur(self):
        with self.assertRaises(ValueError):
            UserService.inscrire_utilisateur("Tom", "Lee", "tom@x.com", "   ", "Employee")

    def test_inscrire_role_admin_donne_id_1(self):
        UserService.inscrire_utilisateur("Boss", "Admin", "boss@test.local", "boss123", "Admin")
        user = UserModel.get_user_by_email("boss@test.local")
        self.assertEqual(user["role_id"], 1)

    def test_inscrire_role_employee_donne_id_3(self):
        UserService.inscrire_utilisateur("Emp", "Test", "emp@test.local", "emp123", "Employee")
        user = UserModel.get_user_by_email("emp@test.local")
        self.assertEqual(user["role_id"], 3)

    def test_modifier_utilisateur_sans_id_leve_erreur(self):
        with self.assertRaises(ValueError):
            UserService.modifier_utilisateur(None, "A", "B", "c@d.com", "Employee")

    def test_modifier_utilisateur_champ_vide_leve_erreur(self):
        """Un champ obligatoire vide lors de la modification doit lever ValueError."""
        user = UserModel.get_user_by_email("alice@test.local")
        with self.assertRaises(ValueError):
            UserService.modifier_utilisateur(user["id"], "", "Durand", "alice@test.local", "Employee")

    def test_supprimer_utilisateur_sans_id_leve_erreur(self):
        with self.assertRaises(ValueError):
            UserService.supprimer_utilisateur(None)

    def test_obtenir_noms_roles_capitalises(self):
        roles = UserService.obtenir_noms_roles()
        for role in roles:
            self.assertEqual(role, role.capitalize())

    def test_convertir_role_en_id_manager(self):
        role_id = UserService._convertir_role_en_id("Manager")
        self.assertEqual(role_id, 2)

    def test_convertir_role_en_id_inconnu_donne_3(self):
        role_id = UserService._convertir_role_en_id("Invité")
        self.assertEqual(role_id, 3)


if __name__ == "__main__":
    unittest.main()
