"""test dungeon master module"""
import unittest
from unittest.mock import Mock
from parameterized import parameterized
from game.controller.dungeon_controller import DungeonMaster

class TestDungeonMaster(unittest.TestCase):
    """Test DungeonMaster class"""

    def setUp(self):
        """Set up environment required for tests"""
        self.dungeon_master = DungeonMaster()

    @parameterized.expand([
        ["You enter a quirky test location.", "You enter a quirky test location.\n\n"],
        ["", ""],
    ])
    def test_brief(self, brief, expected):
        """Test brief method"""
        mock_location = Mock()
        attrs = {
            "brief": brief,
            "visited": False
        }
        mock_location.configure_mock(**attrs)
        self.dungeon_master.all_name_locations.append(("test", mock_location))
        self.assertEqual(self.dungeon_master.brief("test"), expected)
