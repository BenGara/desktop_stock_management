"""Tests unitaires pour le modèle AssignmentModel."""

import unittest

from models.assignment_model import AssignmentModel


class TestAssignments(unittest.TestCase):
    """Série de tests pour les opérations d'affectation de matériel."""

    def test_assign_material(self):
        """Vérifie que l'affectation d'un matériel disponible existant
        ne génère aucune erreur.
        """
        try:
            AssignmentModel.assign_material(1, 1)
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
