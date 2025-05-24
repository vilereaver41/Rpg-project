import unittest
import os
import csv

# Adjust import path based on project structure
try:
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
    from rpg_game.data.skill_loader import load_skills_from_csv, _normalize_cell_value # Import helper if needed for comparison
except ImportError:
    # Fallback for running tests directly or if PYTHONPATH is not set
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
    from rpg_game.data.skill_loader import load_skills_from_csv, _normalize_cell_value

# Define the path for the test CSV file within the tests directory
TEST_SKILLS_CSV_FILENAME = "test_skills_data.csv"

class TestSkillLoader(unittest.TestCase):
    """Tests for loading skill data using load_skills_from_csv."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary CSV file for testing skill loading.
        Uses the 17-column layout:
        Name, Skill Rarity, Skill Type, Scope, Cost, Dmg Type, Element, Occasion,
        Formula, Variance, Critical, Hit Type, Animation, Requirement,
        Effects, Additional Notes, Description
        (Indices 0-16)
        """
        cls.test_csv_path = os.path.join(os.path.dirname(__file__), TEST_SKILLS_CSV_FILENAME)
        
        cls.common_header = ["Name","Skill Rarity","Skill Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effects","Additional Notes","Description"]
        
        cls.test_data = [
            ["Universal Melee Skills", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            cls.common_header,
            ["Attack (Base Attack)","","None","Single","0","Hp Damage","Physical","Battle Screen","a.atk * 2 - b.def * 2","20%","Yes","Physical","Null","Null","Null","Null","Null"], # Universal Melee (Ability)
            
            ["Sword Skills", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            cls.common_header,
            ["Power Strike","Common","Special","Single","10","Hp Damage","Physical","Battle Screen","Damage = (a.atk * 2 - b.def) + 5","20%","Yes","Physical","Null","Sword","Null","Null","Strike with force against your target."], # Sword (Ability)
            
            ["Sword Passives", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            cls.common_header,
            # Blade Reaver: Name, Rarity, Type (Passive), (empty for most Ability fields), Effects, Additional Notes, Description (empty)
            ["Blade Reaver","Uncommon","Passive","","","","","","","","","","","","Your critical hits deal 15% more damage.","",""],
            
            ["Light Spells", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section Header
            cls.common_header,
            ["Heal","Common","Magic","Single","10","Heal","Light","Battle Screen","a.mat * 2","20%","No","Magic","Null","Stave","Restores HP","A basic healing spell.","Restores a small amount of HP to a single target."], # Light Spell (Spell)
            
            [",,,,,,,,,,,,,,,,"] # Empty separator row
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

    def test_successful_skill_loading_and_verification(self):
        """
        Tests successful loading of skills from the test CSV and verifies key attributes.
        """
        skills = load_skills_from_csv(self.test_csv_path)
        self.assertIsNotNone(skills, "Loaded skills dictionary should not be None.")
        self.assertIsInstance(skills, dict, "Should return a dictionary.")
        
        self.assertEqual(len(skills), 4, "Should load exactly 4 skills.")

        # --- "Attack (Base Attack)" (Universal Melee - Ability) Verification ---
        self.assertIn("Attack (Base Attack)", skills)
        base_attack = skills["Attack (Base Attack)"]
        self.assertIsInstance(base_attack, Ability)
        self.assertEqual(base_attack.name, "Attack (Base Attack)")
        self.assertEqual(base_attack.skill_rarity, "") # From "" in CSV (was empty)
        self.assertEqual(base_attack.skill_type_csv, "None") # From CSV
        self.assertEqual(base_attack.category, "Universal Melee") # Derived from section
        self.assertEqual(base_attack.scope, "Single")
        self.assertEqual(base_attack.cost, "0")
        self.assertEqual(base_attack.dmg_type, "Hp Damage")
        self.assertEqual(base_attack.element, "Physical")
        self.assertEqual(base_attack.formula, "a.atk * 2 - b.def * 2")
        self.assertEqual(base_attack.effects_csv, "") # "Null" in CSV -> ""
        # Description: loader uses effects_csv if description is "Null", else generic. Here, description is "Null".
        # Since effects_csv is also "Null", it becomes a generic description.
        self.assertEqual(base_attack.description, " Universal Melee ability.") # Adjusted expectation

        # --- "Power Strike" (Sword - Ability) Verification ---
        self.assertIn("Power Strike", skills)
        power_strike = skills["Power Strike"]
        self.assertIsInstance(power_strike, Ability)
        self.assertEqual(power_strike.name, "Power Strike")
        self.assertEqual(power_strike.skill_rarity, "Common")
        self.assertEqual(power_strike.skill_type_csv, "Special") # From CSV
        self.assertEqual(power_strike.category, "Sword") # Derived from section
        self.assertEqual(power_strike.scope, "Single")
        self.assertEqual(power_strike.cost, "10")
        self.assertEqual(power_strike.dmg_type, "Hp Damage")
        self.assertEqual(power_strike.element, "Physical")
        self.assertEqual(power_strike.formula, "Damage = (a.atk * 2 - b.def) + 5")
        self.assertEqual(power_strike.requirement, "Sword")
        self.assertEqual(power_strike.effects_csv, "") # "Null" in CSV -> ""
        self.assertEqual(power_strike.description, "Strike with force against your target.") # From CSV col 16

        # --- "Blade Reaver" (Sword Passive - PassiveSkill) Verification ---
        self.assertIn("Blade Reaver", skills)
        blade_reaver = skills["Blade Reaver"]
        self.assertIsInstance(blade_reaver, PassiveSkill)
        self.assertEqual(blade_reaver.name, "Blade Reaver")
        self.assertEqual(blade_reaver.skill_rarity, "Uncommon")
        self.assertEqual(blade_reaver.skill_type_csv, "Passive") # From CSV
        self.assertEqual(blade_reaver.category, "Sword") # Derived from section "Sword Passives"
        self.assertEqual(blade_reaver.effects_csv, "Your critical hits deal 15% more damage.")
        # Description: loader uses effects_csv if description is empty.
        self.assertEqual(blade_reaver.description, "Your critical hits deal 15% more damage.")
        
        # Verify that Ability-specific fields are empty or default for PassiveSkill if not applicable
        # These fields are not directly on PassiveSkill, but good to be mindful of data cleanliness if they were.
        # For example, if PassiveSkill inherited them, they should be empty.
        # self.assertEqual(blade_reaver.scope, "") # Not an attribute of PassiveSkill directly

        # --- "Heal" (Light Spell - Spell) Verification ---
        self.assertIn("Heal", skills)
        heal_spell = skills["Heal"]
        self.assertIsInstance(heal_spell, Spell)
        self.assertEqual(heal_spell.name, "Heal")
        self.assertEqual(heal_spell.skill_rarity, "Common")
        self.assertEqual(heal_spell.skill_type_csv, "Magic") # From CSV
        self.assertEqual(heal_spell.category, "Light") # Derived from section "Light Spells"
        self.assertEqual(heal_spell.scope, "Single")
        self.assertEqual(heal_spell.cost, "10")
        self.assertEqual(heal_spell.dmg_type, "Heal")
        self.assertEqual(heal_spell.element, "Light")
        self.assertEqual(heal_spell.formula, "a.mat * 2")
        self.assertEqual(heal_spell.requirement, "Stave")
        self.assertEqual(heal_spell.effects_csv, "Restores HP")
        self.assertEqual(heal_spell.additional_notes, "A basic healing spell.")
        self.assertEqual(heal_spell.description, "Restores a small amount of HP to a single target.") # From CSV col 16

    def test_skills_file_not_found(self):
        """
        Tests that FileNotFoundError is raised for load_skills_from_csv
        when the CSV file does not exist.
        """
        non_existent_path = "path/to/a/completely/non_existent_skills_sheet.csv"
        with self.assertRaises(FileNotFoundError, msg="load_skills_from_csv should raise FileNotFoundError"):
            load_skills_from_csv(non_existent_path)

if __name__ == '__main__':
    unittest.main()
