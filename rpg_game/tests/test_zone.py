import unittest
import os
import csv
import shutil

# Adjust import path based on project structure
try:
    from rpg_game.core.enemy import Enemy
    from rpg_game.world.zone import Zone
    from rpg_game.data.enemy_loader import load_enemies_from_csv
    from rpg_game.core.skill import Skill # For mock data
    from rpg_game.core.item import Item   # For mock data
except ImportError:
    # Fallback for running tests directly or if PYTHONPATH is not set
    import sys
    # Assuming this test file is in rpg_game/tests/
    # Add parent of rpg_game to path, then rpg_game itself is a package
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.core.enemy import Enemy
    from rpg_game.world.zone import Zone
    from rpg_game.data.enemy_loader import load_enemies_from_csv
    from rpg_game.core.skill import Skill
    from rpg_game.core.item import Item

# Define the path for the test CSV file within the tests directory
TEST_ZONES_CSV_FILENAME = "test_enemies_with_zones.csv"

class TestZoneLoading(unittest.TestCase):
    """Tests for loading zone data via load_enemies_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing zone and enemy loading.
        """
        # Ensure the directory for test CSVs exists
        cls.test_dir = os.path.dirname(__file__) # Current directory (rpg_game/tests)
        cls.test_csv_path = os.path.join(cls.test_dir, TEST_ZONES_CSV_FILENAME)

        # Mock skills and items data
        cls.mock_skills_data = {
            "MiniBash": Skill(name="MiniBash", description="A small bash.", skill_rarity="Common", skill_type_csv="Active", category="Combat")
        }
        cls.mock_items_data = {
            "Rock": Item(name="Rock", description="A common rock.")
        }
        
        # Standard enemy CSV header
        header = ["Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"]
        
        # Test data including zone markers and enemies
        cls.csv_test_data = [
            header,
            ["Lone Wolf", "1-1", "Common", "Physical", "50", "0", "5", "2", "1", "1", "1", "1", "No", "", "", "Rock"], # Enemy before any zone
            ["Green Woods", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Zone marker
            ["Forest Goblin", "1-2", "Common", "Physical", "30", "0", "3", "1", "1", "1", "1", "1", "No", "MiniBash", "", ""],
            ["Forest Sprite", "1-1", "Uncommon", "Nature", "20", "10", "1", "1", "3", "3", "2", "2", "Yes", "", "", "Rock"],
            ["Old Crypt", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Zone marker
            ["Crypt Bat", "2-2", "Common", "Physical", "25", "0", "4", "1", "1", "1", "1", "1", "No", "", "", ""]
        ]

        with open(cls.test_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cls.csv_test_data)

    @classmethod
    def tearDownClass(cls):
        """
        Removes the temporary CSV file after all tests are run.
        """
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)

    def test_load_zones_and_enemy_association(self):
        """
        Tests that zones are loaded correctly and enemies are associated with the current zone.
        """
        loaded_enemies, loaded_zones = load_enemies_from_csv(self.test_csv_path, self.mock_skills_data, self.mock_items_data)

        # Test zones
        self.assertIsNotNone(loaded_zones, "Loaded zones dictionary should not be None.")
        self.assertIsInstance(loaded_zones, dict, "loaded_zones should be a dictionary.")
        self.assertEqual(len(loaded_zones), 2, "Should load exactly 2 zones.")

        self.assertIn("Green Woods", loaded_zones)
        self.assertIn("Old Crypt", loaded_zones)

        # Verify "Green Woods" zone
        green_woods_zone = loaded_zones["Green Woods"]
        self.assertIsInstance(green_woods_zone, Zone)
        self.assertEqual(green_woods_zone.name, "Green Woods")
        self.assertEqual(len(green_woods_zone.enemy_names), 2)
        self.assertIn("Forest Goblin", green_woods_zone.enemy_names)
        self.assertIn("Forest Sprite", green_woods_zone.enemy_names)

        # Verify "Old Crypt" zone
        old_crypt_zone = loaded_zones["Old Crypt"]
        self.assertIsInstance(old_crypt_zone, Zone)
        self.assertEqual(old_crypt_zone.name, "Old Crypt")
        self.assertEqual(len(old_crypt_zone.enemy_names), 1)
        self.assertIn("Crypt Bat", old_crypt_zone.enemy_names)
        
        # Verify enemies loaded
        self.assertIsNotNone(loaded_enemies, "Loaded enemies dictionary should not be None.")
        self.assertEqual(len(loaded_enemies), 4, "Should load exactly 4 enemies.")
        self.assertIn("Lone Wolf", loaded_enemies)
        self.assertIn("Forest Goblin", loaded_enemies)
        self.assertIn("Forest Sprite", loaded_enemies)
        self.assertIn("Crypt Bat", loaded_enemies)

        # Verify "Lone Wolf" is not in any of the explicitly defined zones' lists
        self.assertNotIn("Lone Wolf", green_woods_zone.enemy_names)
        self.assertNotIn("Lone Wolf", old_crypt_zone.enemy_names)
        
        # Verify enemy zone_name attributes and skill/loot linking
        lone_wolf = loaded_enemies.get("Lone Wolf")
        self.assertIsNotNone(lone_wolf)
        self.assertIsNone(lone_wolf.zone_name, "Lone Wolf should have no zone_name as it's before any zone marker.")

        forest_goblin = loaded_enemies.get("Forest Goblin")
        self.assertIsNotNone(forest_goblin)
        self.assertEqual(forest_goblin.zone_name, "Green Woods")
        self.assertTrue(len(forest_goblin.abilities_spells) == 1)
        self.assertIsInstance(forest_goblin.abilities_spells[0], Skill)
        self.assertEqual(forest_goblin.abilities_spells[0].name, "MiniBash")
        
        forest_sprite = loaded_enemies.get("Forest Sprite")
        self.assertIsNotNone(forest_sprite)
        self.assertEqual(forest_sprite.zone_name, "Green Woods")
        self.assertTrue(len(forest_sprite.loot) == 1)
        self.assertIsInstance(forest_sprite.loot[0], Item)
        self.assertEqual(forest_sprite.loot[0].name, "Rock")

        crypt_bat = loaded_enemies.get("Crypt Bat")
        self.assertIsNotNone(crypt_bat)
        self.assertEqual(crypt_bat.zone_name, "Old Crypt")


    def test_zone_data_structure(self):
        """
        Basic tests for the Zone class data structure and methods.
        """
        zone = Zone(name="Test Zone Alpha")
        self.assertEqual(zone.name, "Test Zone Alpha")
        self.assertEqual(len(zone.enemy_names), 0)
        self.assertEqual(str(zone), "Zone: Test Zone Alpha (Enemies: 0)")

        zone.add_enemy_name("Enemy1")
        self.assertIn("Enemy1", zone.enemy_names)
        self.assertEqual(len(zone.enemy_names), 1)
        self.assertEqual(str(zone), "Zone: Test Zone Alpha (Enemies: 1)")

        zone.add_enemy_name("Enemy2")
        self.assertIn("Enemy2", zone.enemy_names)
        self.assertEqual(len(zone.enemy_names), 2)

        # Test adding duplicate
        zone.add_enemy_name("Enemy1")
        self.assertEqual(len(zone.enemy_names), 2, "Adding a duplicate enemy name should not increase the count.")

        zone_with_initial = Zone(name="Test Zone Beta", enemy_names=["EnemyA", "EnemyB"])
        self.assertEqual(zone_with_initial.name, "Test Zone Beta")
        self.assertEqual(len(zone_with_initial.enemy_names), 2)
        self.assertIn("EnemyA", zone_with_initial.enemy_names)


if __name__ == '__main__':
    unittest.main()
