import unittest
import os
import csv

# Attempt to import from the project structure
try:
    from rpg_game.core.item import Item
    from rpg_game.core.equipment import Equipment
    from rpg_game.data.item_loader import load_equipment_from_csv
except ImportError:
    # Fallback for running tests directly or if PYTHONPATH is not set
    import sys
    # Add the parent directory of 'rpg_game' to sys.path
    # This assumes the tests are in 'rpg_game/tests/'
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.core.item import Item
    from rpg_game.core.equipment import Equipment
    from rpg_game.core.consumable import Consumable
    from rpg_game.core.material import Material
    from rpg_game.core.weapon import Weapon
    from rpg_game.data.item_loader import load_equipment_from_csv, load_consumables_and_materials_from_csv, load_weapons_from_csv


# Define the path for the test CSV file within the tests directory
TEST_EQUIPMENT_CSV_FILENAME = "test_equipment_data.csv"
TEST_CONSUMABLES_MATERIALS_CSV_FILENAME = "test_consumables_materials_data.csv"
TEST_WEAPONS_CSV_FILENAME = "test_weapons_data.csv"

class TestBasicItem(unittest.TestCase):
    """Basic tests for the Item class."""
    def test_item_creation_and_str(self):
        item = Item("Health Potion", "Restores 10 HP.")
        self.assertEqual(item.name, "Health Potion")
        self.assertEqual(item.description, "Restores 10 HP.")
        self.assertEqual(str(item), "Health Potion: Restores 10 HP.")

class TestEquipmentLoader(unittest.TestCase):
    """Tests for loading equipment data using load_equipment_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing equipment loading.
        Column structure: Armor,(empty),Tier,Recipe,Equip Type,Attack,Defense,M.Attack,M.Defense,Agility,Luck,Max Hp,Max Mp,Extra Increases,Additional Changes,Source
        Indices:          0    ,1      ,2   ,3     ,4          ,5     ,6      ,7       ,8        ,9      ,10   ,11    ,12    ,13               ,14                  ,15
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_EQUIPMENT_CSV_FILENAME)
        
        # Data based on the subtask description
        cls.test_data = [
            ["Armor","","Tier","Recipe","Equip Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max Hp","Max Mp","Extra Increases","Additional Changes","Source"], # Header
            ["Leather Cap","Dropped","Common","","Helmet","","1","","","","2","","","","",""], # Source is empty, col 15
            ["Crystal Bark Shield","Dropped","Uncommon","1x Rockwood Defender 3x Crystal Bark 1x Vial of Enchanting Essence","Shield","-2","5","","5","-2","","","","Def & M.Def * 104% - Mgc Ref + 2% - Crit Eva + 4%","",""], # Source is empty, col 15
            ["Whash Silk Cover","Crafted","Uncommon","1x Squirrelkin Cloak 3x Mature wash vine 2x Mature Wash Blossom 1x Wash Seed pod","Armor","3","6","3","6","5","2","10","","Eva + 10%","",""], # Source is empty, col 15
            ["Bone Tooth Necklace","Crafted","Common","","Accesory","1","1","","","-1","-1","","","","",""], # Source is empty, col 15
            ["Leather set","","","","","","","","","","","","","","",""] # Skippable section header
        ]
        # The provided sample data has empty "Source" (column 15).
        # Let's add one with a source for better testing.
        cls.test_data.append(
            ["Iron Helm","Blacksmith","Common","3x Iron Ingot","Helmet","","3","","","","","10","","Toughness +1","","Blacksmith Store"]
        )


        with open(cls.test_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cls.test_data)

    @classmethod
    def tearDownClass(cls):
        """
        Removes the temporary CSV file after all tests are run.
        """
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)

    def test_successful_loading_and_verification(self):
        """
        Tests successful loading of equipment from the test CSV and verifies key attributes.
        """
        equipment = load_equipment_from_csv(self.test_csv_path)
        self.assertIsNotNone(equipment, "Loaded equipment dictionary should not be None.")
        self.assertIsInstance(equipment, dict, "Should return a dictionary.")
        
        # Expected number of items (excluding header and "Leather set")
        # Leather Cap, Crystal Bark Shield, Whash Silk Cover, Bone Tooth Necklace, Iron Helm = 5 items
        self.assertEqual(len(equipment), 5, "Should load the correct number of items.")

        # --- Leather Cap Verification ---
        self.assertIn("Leather Cap", equipment)
        lc = equipment["Leather Cap"]
        self.assertIsInstance(lc, Equipment)
        self.assertEqual(lc.name, "Leather Cap")
        self.assertEqual(lc.tier, "Common")
        self.assertEqual(lc.equip_type, "Helmet")
        self.assertEqual(lc.recipe, "")
        self.assertEqual(lc.source, "") # From test data
        self.assertEqual(lc.attack_bonus, 0) # Default
        self.assertEqual(lc.defense_bonus, 1)
        self.assertEqual(lc.magic_attack_bonus, 0) # Default
        self.assertEqual(lc.magic_defense_bonus, 0) # Default
        self.assertEqual(lc.agility_bonus, 2)
        self.assertEqual(lc.luck_bonus, 0) # Default
        self.assertEqual(lc.max_hp_bonus, 0) # Default
        self.assertEqual(lc.max_mp_bonus, 0) # Default
        self.assertEqual(lc.extra_increases, "")
        self.assertEqual(lc.description, "A piece of Common Helmet.")

        # --- Crystal Bark Shield Verification ---
        self.assertIn("Crystal Bark Shield", equipment)
        cbs = equipment["Crystal Bark Shield"]
        self.assertIsInstance(cbs, Equipment)
        self.assertEqual(cbs.name, "Crystal Bark Shield")
        self.assertEqual(cbs.tier, "Uncommon")
        self.assertEqual(cbs.equip_type, "Shield")
        self.assertEqual(cbs.recipe, "1x Rockwood Defender 3x Crystal Bark 1x Vial of Enchanting Essence")
        self.assertEqual(cbs.source, "") # From test data
        self.assertEqual(cbs.attack_bonus, -2)
        self.assertEqual(cbs.defense_bonus, 5)
        self.assertEqual(cbs.magic_attack_bonus, 0) # Default
        self.assertEqual(cbs.magic_defense_bonus, 5)
        self.assertEqual(cbs.agility_bonus, -2)
        self.assertEqual(cbs.extra_increases, "Def & M.Def * 104% - Mgc Ref + 2% - Crit Eva + 4%")
        self.assertEqual(cbs.description, "A piece of Uncommon Shield.")

        # --- Whash Silk Cover Verification ---
        self.assertIn("Whash Silk Cover", equipment)
        wsc = equipment["Whash Silk Cover"]
        self.assertEqual(wsc.name, "Whash Silk Cover")
        self.assertEqual(wsc.tier, "Uncommon")
        self.assertEqual(wsc.equip_type, "Armor") # equip_type is Armor, though it's a cloak
        self.assertEqual(wsc.recipe, "1x Squirrelkin Cloak 3x Mature wash vine 2x Mature Wash Blossom 1x Wash Seed pod")
        self.assertEqual(wsc.source, "") # From test data
        self.assertEqual(wsc.attack_bonus, 3)
        self.assertEqual(wsc.defense_bonus, 6)
        self.assertEqual(wsc.magic_attack_bonus, 3)
        self.assertEqual(wsc.magic_defense_bonus, 6)
        self.assertEqual(wsc.agility_bonus, 5)
        self.assertEqual(wsc.luck_bonus, 2)
        self.assertEqual(wsc.max_hp_bonus, 10)
        self.assertEqual(wsc.extra_increases, "Eva + 10%")
        self.assertEqual(wsc.description, "A piece of Uncommon Armor.")


        # --- Bone Tooth Necklace Verification ---
        self.assertIn("Bone Tooth Necklace", equipment)
        btn = equipment["Bone Tooth Necklace"]
        self.assertEqual(btn.name, "Bone Tooth Necklace")
        self.assertEqual(btn.tier, "Common")
        self.assertEqual(btn.equip_type, "Accesory") # Sic, from data
        self.assertEqual(btn.recipe, "")
        self.assertEqual(btn.source, "") # From test data
        self.assertEqual(btn.attack_bonus, 1)
        self.assertEqual(btn.defense_bonus, 1)
        self.assertEqual(btn.magic_attack_bonus, 0)
        self.assertEqual(btn.magic_defense_bonus, 0)
        self.assertEqual(btn.agility_bonus, -1)
        self.assertEqual(btn.luck_bonus, -1)
        self.assertEqual(btn.extra_increases, "")
        self.assertEqual(btn.description, "A piece of Common Accesory.")

        # --- Iron Helm Verification (item with a source) ---
        self.assertIn("Iron Helm", equipment)
        ih = equipment["Iron Helm"]
        self.assertEqual(ih.name, "Iron Helm")
        self.assertEqual(ih.tier, "Common")
        self.assertEqual(ih.equip_type, "Helmet")
        self.assertEqual(ih.recipe, "3x Iron Ingot")
        self.assertEqual(ih.source, "Blacksmith Store")
        self.assertEqual(ih.defense_bonus, 3)
        self.assertEqual(ih.max_hp_bonus, 10)
        self.assertEqual(ih.extra_increases, "Toughness +1")
        self.assertEqual(ih.description, "A piece of Common Helmet.")


    def test_file_not_found(self):
        """
        Tests that FileNotFoundError is (ideally) raised when the CSV file does not exist.
        The current item_loader catches FileNotFoundError and returns {}.
        This test is written for the *desired* behavior of re-raising.
        If this test fails, it means item_loader.py's load_equipment_from_csv
        needs to be changed to re-raise FileNotFoundError.
        """
        non_existent_path = "path/to/a/completely/non_existent_equipment_sheet.csv"
        
        # Based on the subtask: "Assert that FileNotFoundError is raised"
        # This requires load_equipment_from_csv to NOT catch FileNotFoundError, or to re-raise it.
        # The previous implementation of load_equipment_from_csv returns {}
        # I will write the test as requested, expecting FileNotFoundError.
        with self.assertRaises(FileNotFoundError, msg="load_equipment_from_csv should raise FileNotFoundError for a non-existent file"):
            load_equipment_from_csv(non_existent_path)


class TestConsumableMaterialLoader(unittest.TestCase):
    """Tests for loading consumables and materials using load_consumables_and_materials_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing consumables and materials loading.
        CSV Structure:
        Potions: Name,,Effect Notes,,
        Special Consumable: Name,Rarity,,Effect Notes,
        Food: Name,Rarity,Effect,Recipe,
        Raw Ingriedient: Name,Rarity,,
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_CONSUMABLES_MATERIALS_CSV_FILENAME)
        
        cls.test_data = [
            # Section Headers
            ["Potions","","","",""],
            # Name (col 0), (empty col 1), Effect Notes (col 2)
            ["Crude Health Potion","","Restores 50 Hp","",""],
            
            ["Special Consumable","","","",""],
            # Name (col 0), Rarity (col 1), (empty col 2), Effect Notes (col 3)
            ["Crystal Glow Berry","Rare","","Permanent Hp up +10 ,Limit 10",""],
            
            ["Food","","","",""],
            # Name (col 0), Rarity (col 1), Effect (col 2), Recipe (col 3)
            ["Dried Meat","Common","Restores 20 HP Atk + 1 M.Atk + 1","1x Raw Meat 1x Handful of herbs",""],
            
            ["Raw Ingriedient","","","",""], # Note: CSV uses "Ingriedient"
            # Name (col 0), Rarity (col 1)
            ["Chomper Filet","Common","","",""],
            ["Bog Iron Ore","Uncommon","","",""] # Extra material to test count
        ]

        with open(cls.test_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cls.test_data)

    @classmethod
    def tearDownClass(cls):
        """
        Removes the temporary CSV file after all tests are run.
        """
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)

    def test_successful_loading_and_verification(self):
        """
        Tests successful loading of consumables and materials from the test CSV.
        """
        items = load_consumables_and_materials_from_csv(self.test_csv_path)
        self.assertIsNotNone(items, "Loaded items dictionary should not be None.")
        self.assertIsInstance(items, dict, "Should return a dictionary.")
        
        # Expected: Crude Health Potion, Crystal Glow Berry, Dried Meat, Chomper Filet, Bog Iron Ore = 5 items
        self.assertEqual(len(items), 5, "Should load the correct number of items (excluding section headers).")

        # --- Crude Health Potion Verification ---
        self.assertIn("Crude Health Potion", items)
        chp = items["Crude Health Potion"]
        self.assertIsInstance(chp, Consumable)
        self.assertEqual(chp.name, "Crude Health Potion")
        self.assertEqual(chp.category, "Potion")
        # The loader uses effect_notes for both description and effect_description for potions
        self.assertEqual(chp.description, "Restores 50 Hp") 
        self.assertEqual(chp.effect_description, "Restores 50 Hp")
        self.assertEqual(chp.rarity, "Common") # Default for potions in loader
        self.assertEqual(chp.recipe, "") # Default

        # --- Crystal Glow Berry Verification ---
        self.assertIn("Crystal Glow Berry", items)
        cgb = items["Crystal Glow Berry"]
        self.assertIsInstance(cgb, Consumable)
        self.assertEqual(cgb.name, "Crystal Glow Berry")
        self.assertEqual(cgb.category, "Special Consumable")
        self.assertEqual(cgb.rarity, "Rare")
        # Loader uses effect_notes for description and effect_description
        self.assertEqual(cgb.description, "Permanent Hp up +10 ,Limit 10")
        self.assertEqual(cgb.effect_description, "Permanent Hp up +10 ,Limit 10")
        self.assertEqual(cgb.recipe, "") # Default

        # --- Dried Meat Verification ---
        self.assertIn("Dried Meat", items)
        dm = items["Dried Meat"]
        self.assertIsInstance(dm, Consumable)
        self.assertEqual(dm.name, "Dried Meat")
        self.assertEqual(dm.category, "Food")
        self.assertEqual(dm.rarity, "Common")
        # Loader uses effect for description and effect_description
        self.assertEqual(dm.description, "Restores 20 HP Atk + 1 M.Atk + 1")
        self.assertEqual(dm.effect_description, "Restores 20 HP Atk + 1 M.Atk + 1")
        self.assertEqual(dm.recipe, "1x Raw Meat 1x Handful of herbs")

        # --- Chomper Filet Verification ---
        self.assertIn("Chomper Filet", items)
        cf = items["Chomper Filet"]
        self.assertIsInstance(cf, Material)
        self.assertEqual(cf.name, "Chomper Filet")
        self.assertEqual(cf.rarity, "Common")
        # Loader creates a generic description for materials
        self.assertEqual(cf.description, "Common crafting material: Chomper Filet.")
        
        # --- Bog Iron Ore Verification (extra material) ---
        self.assertIn("Bog Iron Ore", items)
        bio = items["Bog Iron Ore"]
        self.assertIsInstance(bio, Material)
        self.assertEqual(bio.name, "Bog Iron Ore")
        self.assertEqual(bio.rarity, "Uncommon")
        self.assertEqual(bio.description, "Uncommon crafting material: Bog Iron Ore.")


    def test_consumables_materials_file_not_found(self):
        """
        Tests that FileNotFoundError is raised for load_consumables_and_materials_from_csv
        when the CSV file does not exist.
        """
        non_existent_path = "path/to/a/completely/non_existent_consumables_sheet.csv"
        with self.assertRaises(FileNotFoundError, msg="load_consumables_and_materials_from_csv should raise FileNotFoundError"):
            load_consumables_and_materials_from_csv(non_existent_path)


class TestWeaponLoader(unittest.TestCase):
    """Tests for loading weapon data using load_weapons_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing weapon loading.
        Structure: Section Header (e.g., "Swords Level 1-50,,,,,...")
                   Column Header (Name,Level Range,Source,Tier,Attack Type,Attack,Defense,...)
                   Weapon Data rows
                   Empty Separator Row (,,,,,,,,,,,,,,)
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_WEAPONS_CSV_FILENAME)
        
        # Column indices for reference by the loader:
        # Name (0), Lvl Range (1), Source (2), Tier (3), Atk Type (4),
        # Attack (5), Defense (6), M.Attack (7), M.Defense (8),
        # Agility (9), Luck (10), Max HP (11), Max MP (12),
        # Recipe (13), Extra Increases (14)
        cls.test_data = [
            ["Swords Level 1-50", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            ["Name","Level Range","Source","Tier","Attack Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max HP","Max MP","Recipe","Extra Increases"], # Column Header
            ["Iron Sword","7-9","Dropped","Common","Physical","7","1","","","","","","","","Hit + 2%"],
            [",,,,,,,,,,,,,,,"], # Empty Separator Row
            ["Daggers Level 1-50", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            ["Name","Level Range","Source","Tier","Attack Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max HP","Max MP","Recipe","Extra Increases"], # Column Header
            ["Rusty Knife","1-3","Dropped","Trash","Physical","2","","","","1","","","","","Atk Speed +1"]
        ]

        with open(cls.test_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cls.test_data)

    @classmethod
    def tearDownClass(cls):
        """
        Removes the temporary CSV file after all tests are run.
        """
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)

    def test_successful_weapon_loading_and_verification(self):
        """
        Tests successful loading of weapons from the test CSV and verifies key attributes.
        """
        weapons = load_weapons_from_csv(self.test_csv_path)
        self.assertIsNotNone(weapons, "Loaded weapons dictionary should not be None.")
        self.assertIsInstance(weapons, dict, "Should return a dictionary.")
        
        self.assertEqual(len(weapons), 2, "Should load exactly 2 weapons.")

        # --- Iron Sword Verification ---
        self.assertIn("Iron Sword", weapons)
        iron_sword = weapons["Iron Sword"]
        self.assertIsInstance(iron_sword, Weapon)
        self.assertEqual(iron_sword.name, "Iron Sword")
        self.assertEqual(iron_sword.tier, "Common")
        self.assertEqual(iron_sword.source, "Dropped")
        self.assertEqual(iron_sword.attack_type, "Physical")
        self.assertEqual(iron_sword.weapon_category, "Sword") # Derived from section header
        self.assertEqual(iron_sword.attack_bonus, 7)
        self.assertEqual(iron_sword.defense_bonus, 1)
        self.assertEqual(iron_sword.magic_attack_bonus, 0) # Default
        self.assertEqual(iron_sword.agility_bonus, 0) # Default
        self.assertEqual(iron_sword.recipe, "") # Empty in data
        self.assertEqual(iron_sword.extra_increases, "Hit + 2%")
        self.assertEqual(iron_sword.equip_type, "Main Hand") # Defaulted by loader
        # Description: f"{tier} {current_weapon_category} (Lvl: {level_range})."
        self.assertEqual(iron_sword.description, "Common Sword (Lvl: 7-9).")


        # --- Rusty Knife Verification ---
        self.assertIn("Rusty Knife", weapons)
        rusty_knife = weapons["Rusty Knife"]
        self.assertIsInstance(rusty_knife, Weapon)
        self.assertEqual(rusty_knife.name, "Rusty Knife")
        self.assertEqual(rusty_knife.tier, "Trash")
        self.assertEqual(rusty_knife.source, "Dropped")
        self.assertEqual(rusty_knife.attack_type, "Physical")
        self.assertEqual(rusty_knife.weapon_category, "Dagger") # Derived from section header
        self.assertEqual(rusty_knife.attack_bonus, 2)
        self.assertEqual(rusty_knife.defense_bonus, 0) # Default
        self.assertEqual(rusty_knife.agility_bonus, 1)
        self.assertEqual(rusty_knife.recipe, "") # Empty in data
        self.assertEqual(rusty_knife.extra_increases, "Atk Speed +1")
        self.assertEqual(rusty_knife.equip_type, "Main Hand") # Defaulted by loader
        self.assertEqual(rusty_knife.description, "Trash Dagger (Lvl: 1-3).")

    def test_weapons_file_not_found(self):
        """
        Tests that FileNotFoundError is raised for load_weapons_from_csv
        when the CSV file does not exist.
        """
        non_existent_path = "path/to/a/completely/non_existent_weapons_sheet.csv"
        with self.assertRaises(FileNotFoundError, msg="load_weapons_from_csv should raise FileNotFoundError"):
            load_weapons_from_csv(non_existent_path)

if __name__ == '__main__':
    unittest.main()
