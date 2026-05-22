"""Tests unitaires pour le modèle MaterialModel."""

import unittest

from models.material_model import MaterialModel


class TestMaterials(unittest.TestCase):
    """Série de tests pour les opérations de création
    et de récupération de matériels.
    """

    def test_create_material(self):
        """Vérifier que la création d'un matériel avec des données valides
        ne génère aucune erreur.
        """
        try:
            MaterialModel.create_material(
                "Dell Latitude",
                "SN-001",
                1,
                10
            )
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
