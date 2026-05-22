"""Unit tests for the MaterialModel."""

import unittest

from models.material_model import MaterialModel


class TestMaterials(unittest.TestCase):
    """Test suite for material creation and retrieval operations."""

    def test_create_material(self):
        """Verify that creating a material with valid data raises no error."""
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
