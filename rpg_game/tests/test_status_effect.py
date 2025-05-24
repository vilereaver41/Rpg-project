import unittest
import os
import csv

# Adjust import path based on project structure
try:
    from rpg_game.core.status_effect import StatusEffect
    from rpg_game.data.status_effect_loader import load_status_effects_from_csv
except ImportError:
    # Fallback for running tests directly or if PYTHONPATH is not set
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.core.status_effect import StatusEffect
    from rpg_game.data.status_effect_loader import load_status_effects_from_csv

# Define the path for the test CSV file within the tests directory
TEST_STATUS_EFFECTS_CSV_FILENAME = "test_status_effects_data.csv"

class TestStatusEffectLoader(unittest.TestCase):
    """Tests for loading status effect data using load_status_effects_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing status effect loading.
        Expected columns for data rows (0-indexed):
        Name (0), Element (1), Duration (2), Effect (3), Notes (4)
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_STATUS_EFFECTS_CSV_FILENAME)
        
        cls.test_data = [
            ["Positive States", "", "", "", ""], # Section Header
            # Name, Element, Duration, Effect (effect_description), Notes
            ["Distorted Reality","Magic","2 ~ 3","Eva + 30% - Ctr Atk + 20% - Luck * 110% Atk Count + 1","Some positive note"],
            ["Enlightened","Magic","2 ~ 3","M.Atk & M.Def * 120% - Mgc Eva & MP Rgn + 10% - Resist States - Confusion, Sleep, Fear","Another note"],
            [",,,,"] # Empty separator row, should be skipped by loader
            ["Negative States", "", "", "", ""], # Section Header
            ["Poison","Nature","3 ~ 3","HP Rgn - 10%","A nasty poison"],
            ["Silence","Null Element","2 ~ 2","Seal Skill Type Magic","A silencing debuff"] # Note: loader expects notes in col 4.
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

    def test_successful_status_effect_loading_and_verification(self):
        """
        Tests successful loading of status effects from the test CSV and verifies key attributes.
        """
        status_effects = load_status_effects_from_csv(self.test_csv_path)
        self.assertIsNotNone(status_effects, "Loaded status effects dictionary should not be None.")
        self.assertIsInstance(status_effects, dict, "Should return a dictionary.")
        
        self.assertEqual(len(status_effects), 4, "Should load exactly 4 status effects.")

        # --- "Distorted Reality" (Positive) Verification ---
        self.assertIn("Distorted Reality", status_effects)
        dr = status_effects["Distorted Reality"]
        self.assertIsInstance(dr, StatusEffect)
        self.assertEqual(dr.name, "Distorted Reality")
        self.assertEqual(dr.effect_type, "Positive")
        self.assertEqual(dr.element, "Magic")
        self.assertEqual(dr.duration_str, "2 ~ 3")
        self.assertEqual(dr.effect_description, "Eva + 30% - Ctr Atk + 20% - Luck * 110% Atk Count + 1")
        self.assertEqual(dr.notes, "Some positive note")
        # Check generated description (loader logic: f"{effect_type} effect. {effect_description}")
        self.assertEqual(dr.description, "Positive effect. Eva + 30% - Ctr Atk + 20% - Luck * 110% Atk Count + 1")

        # --- "Enlightened" (Positive) Verification ---
        self.assertIn("Enlightened", status_effects)
        enl = status_effects["Enlightened"]
        self.assertIsInstance(enl, StatusEffect)
        self.assertEqual(enl.name, "Enlightened")
        self.assertEqual(enl.effect_type, "Positive")
        self.assertEqual(enl.element, "Magic")
        self.assertEqual(enl.duration_str, "2 ~ 3")
        self.assertEqual(enl.effect_description, "M.Atk & M.Def * 120% - Mgc Eva & MP Rgn + 10% - Resist States - Confusion, Sleep, Fear")
        self.assertEqual(enl.notes, "Another note")
        self.assertEqual(enl.description, "Positive effect. M.Atk & M.Def * 120% - Mgc Eva & MP Rgn + 10% - Resist States - Confusion, Sleep, Fear")

        # --- "Poison" (Negative) Verification ---
        self.assertIn("Poison", status_effects)
        poi = status_effects["Poison"]
        self.assertIsInstance(poi, StatusEffect)
        self.assertEqual(poi.name, "Poison")
        self.assertEqual(poi.effect_type, "Negative")
        self.assertEqual(poi.element, "Nature")
        self.assertEqual(poi.duration_str, "3 ~ 3")
        self.assertEqual(poi.effect_description, "HP Rgn - 10%")
        self.assertEqual(poi.notes, "A nasty poison")
        self.assertEqual(poi.description, "Negative effect. HP Rgn - 10%")

        # --- "Silence" (Negative) Verification ---
        self.assertIn("Silence", status_effects)
        sil = status_effects["Silence"]
        self.assertIsInstance(sil, StatusEffect)
        self.assertEqual(sil.name, "Silence")
        self.assertEqual(sil.effect_type, "Negative")
        self.assertEqual(sil.element, "Null Element")
        self.assertEqual(sil.duration_str, "2 ~ 2")
        self.assertEqual(sil.effect_description, "Seal Skill Type Magic")
        self.assertEqual(sil.notes, "A silencing debuff") # Loader expects notes in col 4
        self.assertEqual(sil.description, "Negative effect. Seal Skill Type Magic")


    def test_status_effects_file_not_found(self):
        """
        Tests that FileNotFoundError is raised for load_status_effects_from_csv
        when the CSV file does not exist.
        """
        non_existent_path = "path/to/a/completely/non_existent_status_effects_sheet.csv"
        with self.assertRaises(FileNotFoundError, msg="load_status_effects_from_csv should raise FileNotFoundError"):
            load_status_effects_from_csv(non_existent_path)

if __name__ == '__main__':
    unittest.main()
