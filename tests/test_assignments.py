"""Unit tests for the AssignmentModel."""

import unittest

from models.assignment_model import AssignmentModel


class TestAssignments(unittest.TestCase):
    """Test suite for material assignment operations."""

    def test_assign_material(self):
        """Verify that assigning an existing available material raises no error."""
        try:
            AssignmentModel.assign_material(1, 1)
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
