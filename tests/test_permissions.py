"""Tests unitaires pour les services de permissions et de session.

Exécution :
    python -m pytest tests/test_permissions.py -v
"""

import unittest
from unittest.mock import MagicMock

from services.permission_service import PermissionService
from services.session_service import SessionService


# Helpers
def _make_user(role_name: str, user_id: int = 1) -> dict:
    """Crée un faux utilisateur sous forme de dict (simule sqlite3.Row)."""
    return {
        "id": user_id,
        "firstname": "Test",
        "lastname": "User",
        "email": "test@stock.local",
        "password": "hashed",
        "role_id": {"ADMIN": 1, "MANAGER": 2, "EMPLOYEE": 3}.get(role_name.upper(), 3),
        "role_name": role_name.upper(),
    }


# Tests PermissionService
class TestPermissionServiceAdmin(unittest.TestCase):
    """Vérifie que le rôle ADMIN dispose de toutes les permissions critiques."""

    def test_admin_peut_voir_utilisateurs(self):
        self.assertTrue(PermissionService.peut("ADMIN", "voir_utilisateurs"))

    def test_admin_peut_ajouter_utilisateur(self):
        self.assertTrue(PermissionService.peut("ADMIN", "ajouter_utilisateur"))

    def test_admin_peut_supprimer_utilisateur(self):
        self.assertTrue(PermissionService.peut("ADMIN", "supprimer_utilisateur"))

    def test_admin_peut_supprimer_materiel(self):
        self.assertTrue(PermissionService.peut("ADMIN", "supprimer_materiel"))

    def test_admin_peut_supprimer_categorie(self):
        self.assertTrue(PermissionService.peut("ADMIN", "supprimer_categorie"))

    def test_admin_peut_voir_statistiques(self):
        self.assertTrue(PermissionService.peut("ADMIN", "voir_statistiques"))

    def test_admin_peut_gerer_pannes(self):
        self.assertTrue(PermissionService.peut("ADMIN", "gerer_pannes"))

    def test_admin_casse_insensible(self):
        """La vérification doit fonctionner quelle que soit la casse."""
        self.assertTrue(PermissionService.peut("admin", "voir_utilisateurs"))
        self.assertTrue(PermissionService.peut("Admin", "ajouter_materiel"))


class TestPermissionServiceManager(unittest.TestCase):
    """Vérifie les droits du MANAGER : accès stock mais pas gestion utilisateurs."""

    def test_manager_peut_ajouter_materiel(self):
        self.assertTrue(PermissionService.peut("MANAGER", "ajouter_materiel"))

    def test_manager_peut_modifier_materiel(self):
        self.assertTrue(PermissionService.peut("MANAGER", "modifier_materiel"))

    def test_manager_peut_voir_categories(self):
        self.assertTrue(PermissionService.peut("MANAGER", "voir_categories"))

    def test_manager_peut_creer_affectation(self):
        self.assertTrue(PermissionService.peut("MANAGER", "creer_affectation"))

    def test_manager_peut_retourner_materiel(self):
        self.assertTrue(PermissionService.peut("MANAGER", "retourner_materiel"))

    def test_manager_peut_voir_journal(self):
        self.assertTrue(PermissionService.peut("MANAGER", "voir_journal"))

    def test_manager_ne_peut_pas_voir_utilisateurs(self):
        self.assertFalse(PermissionService.peut("MANAGER", "voir_utilisateurs"))

    def test_manager_ne_peut_pas_ajouter_utilisateur(self):
        self.assertFalse(PermissionService.peut("MANAGER", "ajouter_utilisateur"))

    def test_manager_ne_peut_pas_supprimer_materiel(self):
        self.assertFalse(PermissionService.peut("MANAGER", "supprimer_materiel"))

    def test_manager_ne_peut_pas_supprimer_categorie(self):
        self.assertFalse(PermissionService.peut("MANAGER", "supprimer_categorie"))


class TestPermissionServiceEmployee(unittest.TestCase):
    """Vérifie les droits de l'EMPLOYEE : accès restreint en lecture."""

    def test_employee_peut_voir_materiels(self):
        self.assertTrue(PermissionService.peut("EMPLOYEE", "voir_materiels"))

    def test_employee_peut_voir_dashboard(self):
        self.assertTrue(PermissionService.peut("EMPLOYEE", "voir_dashboard"))

    def test_employee_peut_declarer_panne(self):
        self.assertTrue(PermissionService.peut("EMPLOYEE", "declarer_panne"))

    def test_employee_ne_peut_pas_ajouter_materiel(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "ajouter_materiel"))

    def test_employee_ne_peut_pas_modifier_materiel(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "modifier_materiel"))

    def test_employee_ne_peut_pas_supprimer_materiel(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "supprimer_materiel"))

    def test_employee_ne_peut_pas_voir_utilisateurs(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "voir_utilisateurs"))

    def test_employee_ne_peut_pas_voir_categories(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "voir_categories"))

    def test_employee_ne_peut_pas_voir_journal(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "voir_journal"))

    def test_employee_ne_peut_pas_voir_statistiques(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "voir_statistiques"))

    def test_employee_ne_peut_pas_creer_affectation(self):
        self.assertFalse(PermissionService.peut("EMPLOYEE", "creer_affectation"))


class TestPermissionServiceEdgeCases(unittest.TestCase):
    """Cas limites et robustesse du PermissionService."""

    def test_role_vide_renvoie_false(self):
        self.assertFalse(PermissionService.peut("", "voir_dashboard"))

    def test_role_none_renvoie_false(self):
        self.assertFalse(PermissionService.peut(None, "voir_dashboard"))

    def test_permission_inconnue_renvoie_false(self):
        self.assertFalse(PermissionService.peut("ADMIN", "permission_inexistante"))

    def test_permission_vide_renvoie_false(self):
        self.assertFalse(PermissionService.peut("ADMIN", ""))

    def test_peut_ou_erreur_autorise(self):
        """Ne doit pas lever d'exception pour un rôle autorisé."""
        try:
            PermissionService.peut_ou_erreur("ADMIN", "voir_utilisateurs")
        except PermissionError:
            self.fail("peut_ou_erreur a levé PermissionError à tort pour ADMIN.")

    def test_peut_ou_erreur_refuse(self):
        """Doit lever PermissionError pour un rôle non autorisé."""
        with self.assertRaises(PermissionError):
            PermissionService.peut_ou_erreur("EMPLOYEE", "voir_utilisateurs")

    def test_permissions_du_role_admin_non_vide(self):
        perms = PermissionService.permissions_du_role("ADMIN")
        self.assertIsInstance(perms, list)
        self.assertGreater(len(perms), 0)

    def test_permissions_du_role_employee_contient_voir_dashboard(self):
        perms = PermissionService.permissions_du_role("EMPLOYEE")
        self.assertIn("voir_dashboard", perms)

    def test_roles_valides(self):
        roles = PermissionService.roles_valides()
        self.assertIn("ADMIN", roles)
        self.assertIn("MANAGER", roles)
        self.assertIn("EMPLOYEE", roles)


# Tests SessionService
class TestSessionService(unittest.TestCase):
    """Vérifie la gestion de la session utilisateur."""

    def setUp(self):
        """Réinitialise la session avant chaque test."""
        SessionService.fermer()

    def tearDown(self):
        """Nettoie après chaque test."""
        SessionService.fermer()

    def test_session_fermee_par_defaut(self):
        self.assertFalse(SessionService.est_connecte())

    def test_id_none_sans_session(self):
        self.assertIsNone(SessionService.id())

    def test_role_vide_sans_session(self):
        self.assertEqual(SessionService.role(), "")

    def test_ouvrir_session_admin(self):
        user = _make_user("ADMIN", user_id=1)
        SessionService.ouvrir(user)
        self.assertTrue(SessionService.est_connecte())
        self.assertEqual(SessionService.id(), 1)
        self.assertEqual(SessionService.role(), "ADMIN")

    def test_ouvrir_session_manager(self):
        user = _make_user("MANAGER", user_id=5)
        SessionService.ouvrir(user)
        self.assertEqual(SessionService.role(), "MANAGER")
        self.assertEqual(SessionService.id(), 5)

    def test_ouvrir_session_employee(self):
        user = _make_user("EMPLOYEE", user_id=10)
        SessionService.ouvrir(user)
        self.assertEqual(SessionService.role(), "EMPLOYEE")

    def test_fermer_session(self):
        user = _make_user("ADMIN")
        SessionService.ouvrir(user)
        SessionService.fermer()
        self.assertFalse(SessionService.est_connecte())
        self.assertIsNone(SessionService.id())
        self.assertEqual(SessionService.role(), "")

    def test_nom_complet(self):
        user = {"id": 1, "firstname": "Alice", "lastname": "Dupont",
                "email": "alice@test.fr", "password": "x", "role_name": "ADMIN"}
        SessionService.ouvrir(user)
        self.assertEqual(SessionService.nom_complet(), "Alice Dupont")

    def test_prenom(self):
        user = _make_user("MANAGER")
        user["firstname"] = "Benjamin"
        SessionService.ouvrir(user)
        self.assertEqual(SessionService.prenom(), "Benjamin")

    def test_session_remplace_precedente(self):
        """Ouvrir une nouvelle session écrase l'ancienne."""
        SessionService.ouvrir(_make_user("ADMIN", user_id=1))
        SessionService.ouvrir(_make_user("EMPLOYEE", user_id=99))
        self.assertEqual(SessionService.id(), 99)
        self.assertEqual(SessionService.role(), "EMPLOYEE")


# Tests d'intégration Permission + Session
class TestIntegrationPermissionSession(unittest.TestCase):
    """Scénarios complets : connexion → vérification de permission."""

    def setUp(self):
        SessionService.fermer()

    def tearDown(self):
        SessionService.fermer()

    def test_admin_connecte_peut_supprimer_utilisateur(self):
        SessionService.ouvrir(_make_user("ADMIN"))
        role = SessionService.role()
        self.assertTrue(PermissionService.peut(role, "supprimer_utilisateur"))

    def test_manager_connecte_ne_peut_pas_supprimer_utilisateur(self):
        SessionService.ouvrir(_make_user("MANAGER"))
        role = SessionService.role()
        self.assertFalse(PermissionService.peut(role, "supprimer_utilisateur"))

    def test_employee_connecte_ne_peut_pas_modifier_materiel(self):
        SessionService.ouvrir(_make_user("EMPLOYEE"))
        role = SessionService.role()
        self.assertFalse(PermissionService.peut(role, "modifier_materiel"))

    def test_employee_connecte_peut_voir_materiels(self):
        SessionService.ouvrir(_make_user("EMPLOYEE"))
        role = SessionService.role()
        self.assertTrue(PermissionService.peut(role, "voir_materiels"))

    def test_apres_deconnexion_toutes_permissions_refusees(self):
        """Après fermeture de session, aucune permission ne devrait être accordée."""
        SessionService.ouvrir(_make_user("ADMIN"))
        SessionService.fermer()
        role = SessionService.role()
        self.assertFalse(PermissionService.peut(role, "voir_dashboard"))
        self.assertFalse(PermissionService.peut(role, "voir_materiels"))
        self.assertFalse(PermissionService.peut(role, "voir_utilisateurs"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
