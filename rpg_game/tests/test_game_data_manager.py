import unittest
import os
import csv
import shutil # For removing directory tree

# Loader function imports
try:
    from rpg_game.data.game_data_manager import GameDataManager
    # Core data classes
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.item import Item
    from rpg_game.core.equipment import Equipment
    from rpg_game.core.weapon import Weapon
    from rpg_game.core.consumable import Consumable
    from rpg_game.core.material import Material
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
    from rpg_game.core.status_effect import StatusEffect
    # Individual loaders (for reference or potential mocking, not directly used by tests)
    from rpg_game.data.enemy_loader import load_enemies_from_csv
    from rpg_game.data.item_loader import load_equipment_from_csv, load_consumables_and_materials_from_csv, load_weapons_from_csv
    from rpg_game.data.skill_loader import load_skills_from_csv
    from rpg_game.data.status_effect_loader import load_status_effects_from_csv
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from rpg_game.data.game_data_manager import GameDataManager
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.item import Item
    from rpg_game.core.equipment import Equipment
    from rpg_game.core.weapon import Weapon
    from rpg_game.core.consumable import Consumable
    from rpg_game.core.material import Material
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
    from rpg_game.core.status_effect import StatusEffect
    from rpg_game.data.enemy_loader import load_enemies_from_csv
    from rpg_game.data.item_loader import load_equipment_from_csv, load_consumables_and_materials_from_csv, load_weapons_from_csv
    from rpg_game.data.skill_loader import load_skills_from_csv
    from rpg_game.data.status_effect_loader import load_status_effects_from_csv


class TestGameDataManager(unittest.TestCase):
    """Tests for the GameDataManager class."""

    @classmethod
    def setUpClass(cls):
        """
        Creates minimal temporary CSV files for all data types.
        """
        cls.temp_csv_base_path = os.path.join(os.path.dirname(__file__), "temp_gdm_csvs_for_test")
        if os.path.exists(cls.temp_csv_base_path):
            shutil.rmtree(cls.temp_csv_base_path) # Clean up if exists from previous failed run
        os.makedirs(cls.temp_csv_base_path, exist_ok=True)

        # Define CSV file paths
        cls.enemies_csv_path = os.path.join(cls.temp_csv_base_path, "test_enemies_gdm.csv")
        cls.equipment_csv_path = os.path.join(cls.temp_csv_base_path, "test_equipment_gdm.csv")
        cls.consumables_materials_csv_path = os.path.join(cls.temp_csv_base_path, "test_consumables_materials_gdm.csv")
        cls.weapons_csv_path = os.path.join(cls.temp_csv_base_path, "test_weapons_gdm.csv")
        cls.skills_csv_path = os.path.join(cls.temp_csv_base_path, "test_skills_gdm.csv")
        cls.status_effects_csv_path = os.path.join(cls.temp_csv_base_path, "test_buffs_gdm.csv")

        # --- Create test_enemies_gdm.csv ---
        # Name,Level Range,Spawn Chance,Type,Max Hp Lowest Level,Max Mp,Attack,Defense,M.Attack,M.Defense.,Agility,Luck,Has Sprite?,Abilitys & Spells,,Enemy Loot
        enemies_data = [
            ["Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"],
            ["TestGoblin", "1-2", "Common", "Goblinoid", "30", "0", "5", "2", "0", "0", "3", "1", "Yes", "Scratch,Tackle", "", "Gold Coin,Rusty Dagger"]
        ]
        with open(cls.enemies_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(enemies_data)

        # --- Create test_skills_gdm.csv ---
        # Section, Name, Rarity, Type, Scope, Cost, Dmg Type, Element, Occasion, Formula, Variance, Critical, Hit Type, Animation, Requirement, Effects, Additional Notes, Description
        skills_header = ["Name","Skill Rarity","Skill Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effects","Additional Notes","Description"]
        skills_data = [
            ["Goblin Skills", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section for Ability
            skills_header,
            ["Scratch", "Common", "Active", "1 Enemy", "0", "Physical", "Nil", "Battle", "PATK*1", "10%", "No", "Physical", "anim_scratch", "", "Basic scratch", "", "A weak scratch attack."],
            ["Universal Skills", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section for Ability
            skills_header,
            ["Tackle", "Common", "Active", "1 Enemy", "2 TP", "Physical", "Nil", "Battle", "PATK*1.2", "10%", "No", "Physical", "anim_tackle", "", "A basic tackle", "", "A body slam."],
            ["Goblin Passives", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section for Passive
            skills_header,
            ["Tough Skin", "Common", "Passive", "", "", "", "", "", "", "", "", "", "", "", "Defense +1", "", "Naturally tough skin."],
            ["Goblin Magic", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], # Section for Spell
            skills_header,
            ["Mini Heal", "Common", "Active", "Self", "5 MP", "Healing", "Light", "Battle", "MATK*0.5", "5%", "No", "Magical", "anim_mini_heal", "", "Heals a tiny bit.", "", "A very weak healing spell."]
        ]
        with open(cls.skills_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(skills_data)

        # --- Create test_equipment_gdm.csv (Armor, Accessories, Shields) ---
        # Armor,(empty),Tier,Recipe,Equip Type,Attack,Defense,M.Attack,M.Defense,Agility,Luck,Max Hp,Max Mp,Extra Increases,Additional Changes,Source
        equipment_data = [
            ["Armor","","Tier","Recipe","Equip Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max Hp","Max Mp","Extra Increases","Additional Changes","Source"],
            ["Leather Armor","","Common","3 Leather","Armor","","5","","","1","","10","","","","Crafted"]
        ]
        with open(cls.equipment_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(equipment_data)
            
        # --- Create test_consumables_materials_gdm.csv ---
        # Section, Name, Rarity/Effect Notes, Effect/Recipe, Recipe (Food)
        consumables_materials_data = [
            ["Potions","","Effect Notes","",""],
            ["Health Potion","","Restores 25 HP","",""],
            ["Raw Ingriedient","Rarity","","",""], # Note: CSV has "Ingriedient"
            ["Gold Coin","Common","","",""],
            ["Iron Ore", "Common", "", "", ""] # Another material
        ]
        with open(cls.consumables_materials_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(consumables_materials_data)

        # --- Create test_weapons_gdm.csv ---
        # Section Header (e.g. "Daggers Level 1-50")
        # Column Header (Name,Level Range,Source,Tier,Attack Type,Attack,Defense,M.Attack,M.Defense,Agility,Luck,Max HP,Max MP,Recipe,Extra Increases)
        weapons_data = [
            ["Daggers Level 1-50", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["Name","Level Range","Source","Tier","Attack Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max HP","Max MP","Recipe","Extra Increases"],
            ["Rusty Dagger","1-1","Initial","Trash","Physical","3","","","","-1","","","","","A basic, rusty dagger."]
        ]
        with open(cls.weapons_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(weapons_data)

        # --- Create test_buffs_gdm.csv (Status Effects) ---
        # Section Header (Positive States / Negative States)
        # Name,Element,Duration,Effect,Notes
        status_effects_data = [
            ["Positive States","","","",""],
            ["Might","Physical","3 Turns","Attack +10","Feeling strong!"],
            ["Negative States","","","",""],
            ["Slow","Physical","3 Turns","Agility -5","Feeling sluggish."]
        ]
        with open(cls.status_effects_csv_path, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(status_effects_data)

    @classmethod
    def tearDownClass(cls):
        """Removes the temporary directory and all its contents."""
        if os.path.exists(cls.temp_csv_base_path):
            shutil.rmtree(cls.temp_csv_base_path)

    def setUp(self):
        """Initializes a new GameDataManager for each test."""
        self.data_manager = GameDataManager()

    def test_load_all_data_populates_collections(self):
        """Tests that load_all_data correctly populates all data collections."""
        self.data_manager.load_all_data(base_csv_path=self.temp_csv_base_path)

        self.assertTrue(len(self.data_manager.enemies) > 0, "Enemies dictionary should be populated.")
        self.assertEqual(len(self.data_manager.enemies), 1) # TestGoblin

        self.assertTrue(len(self.data_manager.equipment) > 0, "Equipment dictionary should be populated.")
        self.assertEqual(len(self.data_manager.equipment), 1) # Leather Armor
        
        self.assertTrue(len(self.data_manager.consumables) > 0, "Consumables dictionary should be populated.")
        self.assertEqual(len(self.data_manager.consumables), 1) # Health Potion
        
        self.assertTrue(len(self.data_manager.materials) > 0, "Materials dictionary should be populated.")
        self.assertEqual(len(self.data_manager.materials), 2) # Gold Coin, Iron Ore
        
        self.assertTrue(len(self.data_manager.weapons) > 0, "Weapons dictionary should be populated.")
        self.assertEqual(len(self.data_manager.weapons), 1) # Rusty Dagger
        
        self.assertTrue(len(self.data_manager.skills) > 0, "Skills dictionary should be populated.")
        self.assertEqual(len(self.data_manager.skills), 4) # Scratch, Tackle, Tough Skin, Mini Heal
        
        self.assertTrue(len(self.data_manager.status_effects) > 0, "Status effects dictionary should be populated.")
        self.assertEqual(len(self.data_manager.status_effects), 2) # Might, Slow

        # all_items = equipment + consumables + materials + weapons
        expected_all_items_count = len(self.data_manager.equipment) + \
                                   len(self.data_manager.consumables) + \
                                   len(self.data_manager.materials) + \
                                   len(self.data_manager.weapons)
        self.assertEqual(len(self.data_manager.all_items), expected_all_items_count, "All_items count mismatch.")
        self.assertTrue(len(self.data_manager.all_items) > 0, "All_items should be populated.")


    def test_getters_retrieve_data(self):
        """Tests that getter methods correctly retrieve loaded data."""
        self.data_manager.load_all_data(base_csv_path=self.temp_csv_base_path)

        # Enemy
        enemy = self.data_manager.get_enemy("TestGoblin")
        self.assertIsNotNone(enemy)
        self.assertIsInstance(enemy, Enemy)
        self.assertEqual(enemy.name, "TestGoblin")

        # Item (Equipment)
        equipment = self.data_manager.get_item("Leather Armor")
        self.assertIsNotNone(equipment)
        self.assertIsInstance(equipment, Equipment)
        self.assertEqual(equipment.name, "Leather Armor")

        # Item (Consumable)
        consumable = self.data_manager.get_item("Health Potion")
        self.assertIsNotNone(consumable)
        self.assertIsInstance(consumable, Consumable)
        self.assertEqual(consumable.name, "Health Potion")
        
        # Item (Material)
        material = self.data_manager.get_item("Gold Coin")
        self.assertIsNotNone(material)
        self.assertIsInstance(material, Material)
        self.assertEqual(material.name, "Gold Coin")

        # Item (Weapon)
        weapon = self.data_manager.get_item("Rusty Dagger")
        self.assertIsNotNone(weapon)
        self.assertIsInstance(weapon, Weapon)
        self.assertEqual(weapon.name, "Rusty Dagger")

        # Skill (Ability)
        skill_ability = self.data_manager.get_skill("Scratch")
        self.assertIsNotNone(skill_ability)
        self.assertIsInstance(skill_ability, Ability)
        self.assertEqual(skill_ability.name, "Scratch")

        # Skill (Passive)
        skill_passive = self.data_manager.get_skill("Tough Skin")
        self.assertIsNotNone(skill_passive)
        self.assertIsInstance(skill_passive, PassiveSkill)
        self.assertEqual(skill_passive.name, "Tough Skin")
        
        # Skill (Spell)
        skill_spell = self.data_manager.get_skill("Mini Heal")
        self.assertIsNotNone(skill_spell)
        self.assertIsInstance(skill_spell, Spell)
        self.assertEqual(skill_spell.name, "Mini Heal")

        # Status Effect
        status_effect = self.data_manager.get_status_effect("Might")
        self.assertIsNotNone(status_effect)
        self.assertIsInstance(status_effect, StatusEffect)
        self.assertEqual(status_effect.name, "Might")

    def test_enemy_data_is_linked(self):
        """Tests that enemy skills and loot are linked to actual Skill and Item objects."""
        self.data_manager.load_all_data(base_csv_path=self.temp_csv_base_path)
        
        enemy = self.data_manager.get_enemy("TestGoblin")
        self.assertIsNotNone(enemy)

        # Test linked abilities/spells
        self.assertTrue(len(enemy.abilities_spells) > 0, "TestGoblin should have abilities.")
        goblin_skill_scratch = enemy.abilities_spells[0] # Assuming "Scratch" is first
        self.assertIsInstance(goblin_skill_scratch, Skill) # Or more specifically, Ability
        self.assertEqual(goblin_skill_scratch.name, "Scratch")
        
        retrieved_skill_scratch = self.data_manager.get_skill("Scratch")
        self.assertIsNotNone(retrieved_skill_scratch)
        self.assertIs(goblin_skill_scratch, retrieved_skill_scratch, "Enemy skill object should be the same instance as in manager's skill list.")

        # Test linked loot
        self.assertTrue(len(enemy.loot) > 0, "TestGoblin should have loot.")
        goblin_loot_gold = enemy.loot[0] # Assuming "Gold Coin" is first
        self.assertIsInstance(goblin_loot_gold, Item) # Or more specifically, Material
        self.assertEqual(goblin_loot_gold.name, "Gold Coin")

        retrieved_item_gold = self.data_manager.get_item("Gold Coin")
        self.assertIsNotNone(retrieved_item_gold)
        self.assertIs(goblin_loot_gold, retrieved_item_gold, "Enemy loot object should be the same instance as in manager's item list.")

    def test_all_items_populated_correctly(self):
        """Tests that all_items dictionary contains items of various types."""
        self.data_manager.load_all_data(base_csv_path=self.temp_csv_base_path)

        # Check for specific items and their types via get_item (which uses all_items)
        equipment = self.data_manager.get_item("Leather Armor")
        self.assertIsNotNone(equipment)
        self.assertIsInstance(equipment, Equipment)

        weapon = self.data_manager.get_item("Rusty Dagger")
        self.assertIsNotNone(weapon)
        self.assertIsInstance(weapon, Weapon)

        consumable = self.data_manager.get_item("Health Potion")
        self.assertIsNotNone(consumable)
        self.assertIsInstance(consumable, Consumable)

        material = self.data_manager.get_item("Gold Coin")
        self.assertIsNotNone(material)
        self.assertIsInstance(material, Material)
        
        # Ensure items from different categories are present in all_items
        self.assertIn("Leather Armor", self.data_manager.all_items)
        self.assertIn("Rusty Dagger", self.data_manager.all_items)
        self.assertIn("Health Potion", self.data_manager.all_items)
        self.assertIn("Gold Coin", self.data_manager.all_items)


if __name__ == '__main__':
    unittest.main()
