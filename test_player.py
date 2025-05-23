import unittest
from player import Player
from items import Weapon, Armor, Item, ItemRarity

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """Set up for test methods."""
        self.player = Player("Test Hero")
        # Create some items for testing equipment and inventory
        self.sword = Weapon(name="Test Sword", description="A sword for testing.", 
                            rarity=ItemRarity.COMMON, attack_bonus=5, strength_bonus=2)
        self.helmet = Armor(name="Test Helmet", description="A helmet for testing.", 
                            rarity=ItemRarity.UNCOMMON, equip_slot="head", 
                            defense_bonus=3, max_hp_bonus=10)
        self.potion = Item(name="Health Potion", description="A test potion.", rarity=ItemRarity.COMMON)

    def test_player_creation(self):
        self.assertEqual(self.player.get_name(), "Test Hero")
        self.assertEqual(self.player.get_level(), 1)
        self.assertEqual(self.player.get_xp(), 0)
        self.assertEqual(self.player.xp_to_next_level, 100)
        # Base stats
        self.assertEqual(self.player.get_base_strength(), 10)
        self.assertEqual(self.player.get_base_dexterity(), 10)
        self.assertEqual(self.player.get_base_intelligence(), 10)
        self.assertEqual(self.player.get_base_constitution(), 10)
        self.assertEqual(self.player.get_base_luck(), 10)
        # Effective stats should equal base stats initially
        self.assertEqual(self.player.get_strength(), 10)
        # Initial HP/MP
        expected_hp = 10 * 10 + 1 * 5 # CON * 10 + Lvl * 5
        expected_mp = 10 * 10 + 1 * 3 # INT * 10 + Lvl * 3
        self.assertEqual(self.player.get_max_hp(), expected_hp)
        self.assertEqual(self.player.get_current_hp(), expected_hp)
        self.assertEqual(self.player.get_max_mp(), expected_mp)
        self.assertEqual(self.player.get_current_mp(), expected_mp)
        self.assertTrue(self.player.is_alive())
        self.assertFalse(self.player.is_defending)

    def test_xp_gain_and_level_up(self):
        initial_str = self.player.get_base_strength()
        initial_con = self.player.get_base_constitution()
        
        self.player.gain_xp(100) # Should level up to 2
        self.assertEqual(self.player.get_level(), 2)
        self.assertEqual(self.player.get_xp(), 0) # XP reset after level up
        self.assertGreater(self.player.xp_to_next_level, 100) # XP needed should increase
        
        self.assertGreaterEqual(self.player.get_base_strength(), initial_str)
        self.assertGreaterEqual(self.player.get_base_constitution(), initial_con + 1) # CON should gain at least 1

        expected_hp_lvl2 = self.player.get_base_constitution() * 10 + self.player.get_level() * 5
        self.assertEqual(self.player.get_max_hp(), expected_hp_lvl2)
        self.assertEqual(self.player.get_current_hp(), expected_hp_lvl2) # HP restored on level up

        # Test level cap (assuming 50)
        self.player.level = 49
        self.player.xp_to_next_level = 100
        self.player.gain_xp(100) # Level to 50
        self.assertEqual(self.player.get_level(), 50)
        
        xp_before_cap_gain = self.player.get_xp()
        self.player.gain_xp(1000) # Try to gain XP at max level
        self.assertEqual(self.player.get_level(), 50) # Still level 50
        self.assertEqual(self.player.get_xp(), 0) # XP should be reset or capped at 0 for max level

    def test_derived_stats_change_with_base_stats(self):
        initial_attack = self.player.get_attack_power()
        self.player._base_strength += 5
        self.assertGreater(self.player.get_attack_power(), initial_attack)

        initial_defense = self.player.get_defense()
        self.player._base_constitution += 5
        self.assertGreater(self.player.get_defense(), initial_defense)
        
        initial_magic_power = self.player.get_magic_power()
        self.player._base_intelligence += 5
        self.assertGreater(self.player.get_magic_power(), initial_magic_power)

    def test_take_damage_and_is_alive(self):
        initial_hp = self.player.get_current_hp()
        self.player.take_damage(10)
        self.assertEqual(self.player.get_current_hp(), initial_hp - 10)
        self.assertTrue(self.player.is_alive())

        self.player.take_damage(self.player.get_current_hp()) # Take exact lethal damage
        self.assertEqual(self.player.get_current_hp(), 0)
        self.assertFalse(self.player.is_alive())

        self.player.current_hp = 10 # Revive for next test
        self.player.start_defending()
        self.assertTrue(self.player.is_defending)
        self.player.take_damage(10) # Damage should be halved
        self.assertEqual(self.player.get_current_hp(), 10 - (10//2) ) # 10 - 5 = 5
        self.assertFalse(self.player.is_defending) # Defend wears off

    def test_use_mp(self):
        initial_mp = self.player.get_current_mp()
        can_use = self.player.use_mp(10)
        self.assertTrue(can_use)
        self.assertEqual(self.player.get_current_mp(), initial_mp - 10)

        cannot_use = self.player.use_mp(self.player.get_current_mp() + 1)
        self.assertFalse(cannot_use)
        self.assertEqual(self.player.get_current_mp(), initial_mp - 10) # MP unchanged

    def test_inventory_management(self):
        self.assertEqual(len(self.player.inventory), 0)
        self.player.add_item_to_inventory(self.potion)
        self.assertEqual(len(self.player.inventory), 1)
        self.assertIn(self.potion, self.player.inventory)

        removed = self.player.remove_item_from_inventory(self.potion)
        self.assertTrue(removed)
        self.assertEqual(len(self.player.inventory), 0)

        not_present_item = Item("Ghost Potion", "boo", ItemRarity.EPIC)
        removed_false = self.player.remove_item_from_inventory(not_present_item)
        self.assertFalse(removed_false)

    def test_equipment_equip_unequip(self):
        self.player.add_item_to_inventory(self.sword)
        self.player.add_item_to_inventory(self.helmet)

        # Equip sword
        base_str = self.player.get_base_strength()
        base_atk = self.player.get_attack_power() # Calculated from base_str only at this point
        
        self.player.equip(self.sword)
        self.assertIn(self.sword, self.player.equipment.values())
        self.assertNotIn(self.sword, self.player.inventory)
        self.assertEqual(self.player.get_strength(), base_str + self.sword.stat_bonuses['strength'])
        # Attack power = (base_str + sword_str_bonus)*2 + sword_attack_bonus
        expected_atk = (base_str + self.sword.stat_bonuses['strength']) * 2 + self.sword.stat_bonuses['attack_power']
        self.assertEqual(self.player.get_attack_power(), expected_atk)

        # Equip helmet
        base_con = self.player.get_base_constitution()
        initial_max_hp = self.player.get_max_hp() # Before helmet
        base_def = self.player.get_defense() # Before helmet

        self.player.equip(self.helmet)
        self.assertIn(self.helmet, self.player.equipment.values())
        self.assertEqual(self.player.get_constitution(), base_con) # Helmet has no CON bonus in this setup
        expected_max_hp = (base_con * 10 + self.player.level * 5) + self.helmet.stat_bonuses['max_hp']
        self.assertEqual(self.player.get_max_hp(), expected_max_hp)
        
        expected_def = (base_con + self.player.get_dexterity() // 2) + \
                       self.helmet.stat_bonuses['defense'] + \
                       self.player._get_equipment_bonus('defense') # Sword has no def bonus
        self.assertEqual(self.player.get_defense(), expected_def)


        # Unequip sword
        hp_before_unequip_sword = self.player.get_current_hp()
        max_hp_before_unequip_sword = self.player.get_max_hp()

        self.player.unequip("weapon")
        self.assertIsNone(self.player.equipment["weapon"])
        self.assertIn(self.sword, self.player.inventory)
        self.assertEqual(self.player.get_strength(), base_str) # Back to base
        self.assertEqual(self.player.get_attack_power(), base_str * 2) # Back to base_str derived
        self.assertEqual(self.player.get_max_hp(), max_hp_before_unequip_sword) # Sword had no HP bonus
        self.assertEqual(self.player.get_current_hp(), hp_before_unequip_sword)


        # Unequip helmet - test HP adjustment
        self.player.current_hp = self.player.get_max_hp() // 2 # Set HP to 50%
        hp_before_unequip = self.player.get_current_hp()
        max_hp_before_unequip = self.player.get_max_hp()
        
        self.player.unequip("head")
        self.assertIsNone(self.player.equipment["head"])
        self.assertIn(self.helmet, self.player.inventory)
        self.assertEqual(self.player.get_max_hp(), max_hp_before_unequip - self.helmet.stat_bonuses['max_hp'])
        
        # Proportional HP check
        expected_hp_after_unequip = int((max_hp_before_unequip - self.helmet.stat_bonuses['max_hp']) * \
                                     (hp_before_unequip / max_hp_before_unequip))
        self.assertEqual(self.player.get_current_hp(), expected_hp_after_unequip)
        self.assertEqual(self.player.get_defense(), base_con + self.player.get_dexterity() // 2) # Back to base

    def test_equip_replace(self):
        self.player.add_item_to_inventory(self.sword)
        self.player.equip(self.sword) # Equip initial sword

        better_sword = Weapon(name="Better Sword", description="A shiny new sword.", 
                              rarity=ItemRarity.RARE, attack_bonus=10, strength_bonus=5)
        self.player.add_item_to_inventory(better_sword)
        
        self.player.equip(better_sword) # Equip better_sword, should replace self.sword
        self.assertEqual(self.player.equipment["weapon"], better_sword)
        self.assertIn(self.sword, self.player.inventory) # Old sword should be back in inventory
        self.assertNotIn(better_sword, self.player.inventory)

if __name__ == '__main__':
    unittest.main()
