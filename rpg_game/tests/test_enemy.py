import unittest
import os
import csv

# Corrected imports to match the project structure and new requirements
try:
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.skill import Skill # Base Skill class for mocking
    from rpg_game.core.item import Item   # Base Item class for mocking
    from rpg_game.data.enemy_loader import load_enemies_from_csv, parse_list_from_string
except ImportError:
    # Fallback for running tests directly or if PYTHONPATH is not set
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.skill import Skill
    from rpg_game.core.item import Item
    from rpg_game.data.enemy_loader import load_enemies_from_csv, parse_list_from_string


# Define the path for the test CSV file within the tests directory
TEST_CSV_FILENAME = "test_enemies_data.csv"

class TestEnemyLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing and mock data for skills and items.
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_CSV_FILENAME)
        
        cls.test_data = [
            ["Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"],
            ["Squirrelkin", "1-2", "Common", "Physical", "45", "0", "5", "1", "3", "8", "2", "2", "Yes", "Acorn Toss,", "", "Squirrelkin Pelt, Rusty Knife,"],
            ["Goblin Crook", "2-4", "Common", "Goblinoid", "300", "10", "8", "4", "2", "2", "6", "2", "Yes", "Backhand, Crack Pot, Drink Potion", "", "Goblin loot bag, All Leather Armor Items. Skinning Knife, Iron Dagger"],
            ["River Sprite", "5-7", "Uncommon", "Water", "450", "1000", "10", "5", "25", "20", "12", "5", "Yes", "Water Jet, Healing Wave,", "", "Smooth Pebble, River Moss, Magic Essence,"]
        ]

        with open(cls.test_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cls.test_data)

        # Mock skills_data and items_data
        cls.mock_skills_data = {
            "Acorn Toss": Skill(name="Acorn Toss", description="Throws an acorn.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
            "Backhand": Skill(name="Backhand", description="A quick backhand.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
            "Crack Pot": Skill(name="Crack Pot", description="Smashes a pot.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
            "Drink Potion": Skill(name="Drink Potion", description="Drinks a potion.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
            "Water Jet": Skill(name="Water Jet", description="Shoots a jet of water.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
            "Healing Wave": Skill(name="Healing Wave", description="A wave of healing energy.", skill_rarity="Common", skill_type_csv="Active", category="Monster"),
        }
        cls.mock_items_data = {
            "Squirrelkin Pelt": Item(name="Squirrelkin Pelt", description="Pelt of a squirrelkin."),
            "Rusty Knife": Item(name="Rusty Knife", description="A rusty knife."),
            "Goblin loot bag": Item(name="Goblin loot bag", description="A small bag of loot."),
            "All Leather Armor Items. Skinning Knife": Item(name="All Leather Armor Items. Skinning Knife", description="Leather armor and a knife."), # Note: name from CSV is long
            "Iron Dagger": Item(name="Iron Dagger", description="A standard iron dagger."),
            "Smooth Pebble": Item(name="Smooth Pebble", description="A smooth pebble."),
            "River Moss": Item(name="River Moss", description="Moss from a river."),
            "Magic Essence": Item(name="Magic Essence", description="Concentrated magic essence."),
        }


    @classmethod
    def tearDownClass(cls):
        """
        Removes the temporary CSV file after all tests are run.
        """
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)

    def test_successful_loading_and_basic_verification(self):
        """
        Tests successful loading of enemies from the test CSV and verifies key attributes,
        including linked Skill and Item objects.
        """
        enemies = load_enemies_from_csv(self.test_csv_path, self.mock_skills_data, self.mock_items_data)
        self.assertIsNotNone(enemies, "Loaded enemies dictionary should not be None.")
        self.assertIsInstance(enemies, dict, "Should return a dictionary.")
        self.assertEqual(len(enemies), 3, "Should load exactly 3 enemies.") # Squirrelkin, Goblin Crook, River Sprite

        # --- Squirrelkin Verification ---
        self.assertIn("Squirrelkin", enemies)
        squirrelkin = enemies["Squirrelkin"]
        self.assertIsInstance(squirrelkin, Enemy)
        self.assertEqual(squirrelkin.name, "Squirrelkin")
        self.assertEqual(squirrelkin.max_hp, 45)
        # Abilities
        self.assertIsInstance(squirrelkin.abilities_spells, list)
        self.assertEqual(len(squirrelkin.abilities_spells), 1)
        self.assertIsInstance(squirrelkin.abilities_spells[0], Skill)
        self.assertEqual(squirrelkin.abilities_spells[0].name, "Acorn Toss")
        # Loot
        self.assertIsInstance(squirrelkin.loot, list)
        self.assertEqual(len(squirrelkin.loot), 2)
        self.assertIsInstance(squirrelkin.loot[0], Item)
        self.assertEqual(squirrelkin.loot[0].name, "Squirrelkin Pelt")
        self.assertIsInstance(squirrelkin.loot[1], Item)
        self.assertEqual(squirrelkin.loot[1].name, "Rusty Knife")
        self.assertIsNone(squirrelkin.zone_name, "Squirrelkin's zone_name should be None as test CSV has no zone markers.")


        # --- Goblin Crook Verification ---
        self.assertIn("Goblin Crook", enemies)
        goblin_crook = enemies["Goblin Crook"]
        self.assertIsInstance(goblin_crook, Enemy)
        self.assertEqual(goblin_crook.name, "Goblin Crook")
        self.assertEqual(goblin_crook.max_hp, 300)
        # Abilities
        self.assertIsInstance(goblin_crook.abilities_spells, list)
        self.assertEqual(len(goblin_crook.abilities_spells), 3)
        expected_goblin_skills = ["Backhand", "Crack Pot", "Drink Potion"]
        loaded_goblin_skill_names = [skill.name for skill in goblin_crook.abilities_spells]
        for skill_name in expected_goblin_skills:
            self.assertIn(skill_name, loaded_goblin_skill_names)
            self.assertTrue(any(isinstance(s, Skill) for s in goblin_crook.abilities_spells if s.name == skill_name))
        # Loot
        self.assertIsInstance(goblin_crook.loot, list)
        self.assertEqual(len(goblin_crook.loot), 3)
        expected_goblin_loot = ["Goblin loot bag", "All Leather Armor Items. Skinning Knife", "Iron Dagger"]
        loaded_goblin_loot_names = [item.name for item in goblin_crook.loot]
        for item_name in expected_goblin_loot:
            self.assertIn(item_name, loaded_goblin_loot_names)
            self.assertTrue(any(isinstance(i, Item) for i in goblin_crook.loot if i.name == item_name))
        self.assertIsNone(goblin_crook.zone_name, "Goblin Crook's zone_name should be None as test CSV has no zone markers.")


        # --- River Sprite Verification ---
        self.assertIn("River Sprite", enemies)
        river_sprite = enemies["River Sprite"]
        self.assertIsInstance(river_sprite, Enemy)
        # Abilities
        self.assertIsInstance(river_sprite.abilities_spells, list)
        self.assertEqual(len(river_sprite.abilities_spells), 2)
        expected_rs_skills = ["Water Jet", "Healing Wave"]
        loaded_rs_skill_names = [skill.name for skill in river_sprite.abilities_spells]
        for skill_name in expected_rs_skills:
            self.assertIn(skill_name, loaded_rs_skill_names)
        # Loot
        self.assertIsInstance(river_sprite.loot, list)
        self.assertEqual(len(river_sprite.loot), 3)
        expected_rs_loot = ["Smooth Pebble", "River Moss", "Magic Essence"]
        loaded_rs_loot_names = [item.name for item in river_sprite.loot]
        for item_name in expected_rs_loot:
            self.assertIn(item_name, loaded_rs_loot_names)
        self.assertIsNone(river_sprite.zone_name, "River Sprite's zone_name should be None as test CSV has no zone markers.")


    def test_file_not_found(self):
        """
        Tests that FileNotFoundError is raised when the CSV file does not exist.
        The loader should let FileNotFoundError propagate.
        """
        non_existent_path = "path/to/non_existent_enemy_sheet.csv"
        # Pass empty dicts for skills_data and items_data as they are required by the signature
        with self.assertRaises(FileNotFoundError, msg="load_enemies_from_csv should raise FileNotFoundError for a non-existent file"):
            load_enemies_from_csv(non_existent_path, {}, {})


    def test_parse_list_from_string(self):
        """Tests the helper function parse_list_from_string."""
        self.assertEqual(parse_list_from_string("item1, item2, item3"), ["item1", "item2", "item3"])
        self.assertEqual(parse_list_from_string("item1,item2, item3 "), ["item1", "item2", "item3"])
        self.assertEqual(parse_list_from_string("item1"), ["item1"])
        self.assertEqual(parse_list_from_string("item1,"), ["item1"]) # Trailing comma
        self.assertEqual(parse_list_from_string("item1, item2,"), ["item1", "item2"]) # Trailing comma
        self.assertEqual(parse_list_from_string(""), [])
        self.assertEqual(parse_list_from_string(","), []) # Only comma
        self.assertEqual(parse_list_from_string(" , "), []) # Whitespace and comma
        self.assertEqual(parse_list_from_string("item1,,item2"), ["item1", "item2"]) # Empty item between commas

if __name__ == '__main__':
    unittest.main()
