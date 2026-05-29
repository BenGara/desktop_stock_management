"""Tests unitaires du service d'authentification (AuthService)."""

import unittest
import sqlite3
import sys, os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth_service import AuthService


def make_db():
    """Crée une base SQLite en mémoire avec le schéma et les données minimales."""
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


class TestAuthServiceHashPassword(unittest.TestCase):
    """Tests du hachage SHA-256 des mots de passe."""

    def test_hash_retourne_une_chaine_hexadecimale(self):
        result = AuthService.hash_password("monMotDePasse")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_hash_identique_pour_meme_mdp(self):
        h1 = AuthService.hash_password("test123")
        h2 = AuthService.hash_password("test123")
        self.assertEqual(h1, h2)

    def test_hash_different_pour_mdp_differents(self):
        h1 = AuthService.hash_password("password1")
        h2 = AuthService.hash_password("password2")
        self.assertNotEqual(h1, h2)

    def test_hash_sensible_a_la_casse(self):
        self.assertNotEqual(
            AuthService.hash_password("Admin"),
            AuthService.hash_password("admin")
        )

    def test_hash_valeur_connue(self):
        expected = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
        self.assertEqual(AuthService.hash_password("admin123"), expected)


class TestAuthServiceLogin(unittest.TestCase):
    """Tests de la méthode de connexion."""

    def setUp(self):
        self._conn = make_db()
        patcher = patch("database.get_connection", return_value=self._conn)
        self.mock_get_conn = patcher.start()
        self.addCleanup(patcher.stop)

    def test_connexion_avec_identifiants_valides(self):
        user = AuthService.login("alice@test.local", "admin123")
        self.assertIsNotNone(user)

    def test_connexion_email_inexistant(self):
        user = AuthService.login("inconnu@test.local", "admin123")
        self.assertIsNone(user)

    def test_connexion_mauvais_mot_de_passe(self):
        user = AuthService.login("alice@test.local", "mauvais_mdp")
        self.assertIsNone(user)

    def test_connexion_email_vide(self):
        user = AuthService.login("", "admin123")
        self.assertIsNone(user)

    def test_connexion_mdp_vide(self):
        user = AuthService.login("alice@test.local", "")
        self.assertIsNone(user)

    def test_connexion_retourne_donnees_utilisateur(self):
        user = AuthService.login("alice@test.local", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "alice@test.local")
        self.assertEqual(user["firstname"], "Alice")


if __name__ == "__main__":
    unittest.main()
