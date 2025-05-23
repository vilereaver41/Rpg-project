import unittest
from core.player import Player

class TestPlayerCreation(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHero")

    def test_initial_attributes(self):
        self.assertEqual(self.player.name, "TestHero")
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.xp, 0)
        self.assertEqual(self.player.xp_to_next_level, 100)
        
        # Initial stats
        self.assertEqual(self.player.stats['strength'], 10)
        self.assertEqual(self.player.stats['dexterity'], 10)
        self.assertEqual(self.player.stats['intelligence'], 10)
        self.assertEqual(self.player.stats['constitution'], 10)
        self.assertEqual(self.player.stats['luck'], 5)

    def test_initial_derived_stats_and_hp_mp(self):
        # Based on initial constitution of 10
        self.assertEqual(self.player.max_hp, 100)
        self.assertEqual(self.player.hp, 100)
        # Based on initial intelligence of 10
        self.assertEqual(self.player.max_mp, 50)
        self.assertEqual(self.player.mp, 50)

        # Check some derived stats (based on initial primary stats)
        self.assertEqual(self.player.derived_stats['attack_power'], 20) # strength * 2
        self.assertEqual(self.player.derived_stats['defense'], 15)      # constitution * 1.5
        self.assertEqual(self.player.derived_stats['magic_power'], 20)  # intelligence * 2
        self.assertAlmostEqual(self.player.derived_stats['critical_hit_chance'], 0.25) # luck * 0.05
        self.assertAlmostEqual(self.player.derived_stats['accuracy'], 1.0) # dexterity * 0.1
        self.assertAlmostEqual(self.player.derived_stats['evasion'], 0.2)  # dexterity * 0.02

class TestPlayerDamageAndHeal(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHero")
        # Initial HP = 100, Max HP = 100

    def test_take_damage_reduces_hp(self):
        damage_taken = self.player.take_damage(30)
        self.assertEqual(self.player.hp, 70)
        self.assertEqual(damage_taken, 30)

    def test_take_damage_does_not_go_below_zero(self):
        damage_taken = self.player.take_damage(150) # More than current HP
        self.assertEqual(self.player.hp, 0)
        self.assertEqual(damage_taken, 100) # Actual damage should be initial HP

    def test_take_damage_zero(self):
        damage_taken = self.player.take_damage(0)
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(damage_taken, 0)
    
    def test_take_damage_negative(self):
        # Current implementation: negative damage will heal if not capped by max_hp
        # Or rather, min(negative_amount, self.hp) will be negative_amount
        # self.hp -= negative_amount  => self.hp += abs(negative_amount)
        # This might be an area for future design decision (e.g. should it raise error or do nothing)
        # For now, test current behavior: it increases HP.
        damage_taken = self.player.take_damage(-10)
        self.assertEqual(self.player.hp, 110) # Heals beyond max_hp if not capped in take_damage itself
        # The Player class's take_damage doesn't prevent hp > max_hp if damage is negative.
        # Let's assume take_damage is for positive damage amounts.
        # Re-testing with a scenario where actual_damage is what's expected
        self.player.hp = 50 # Reset HP
        self.player.max_hp = 100
        damage_taken_neg = self.player.take_damage(-10)
        self.assertEqual(damage_taken_neg, -10) # actual_damage is -10
        self.assertEqual(self.player.hp, 60) # 50 - (-10) = 60. This behavior might be undesirable.
        # The problem description implies we should test current behavior.

    def test_heal_increases_hp(self):
        self.player.hp = 50 # Set HP to a lower value first
        amount_healed = self.player.heal(30)
        self.assertEqual(self.player.hp, 80)
        self.assertEqual(amount_healed, 30)

    def test_heal_does_not_exceed_max_hp(self):
        self.player.hp = 90
        amount_healed = self.player.heal(30) # Try to heal 30 when only 10 is needed for max
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(amount_healed, 10)

    def test_heal_zero(self):
        self.player.hp = 50
        amount_healed = self.player.heal(0)
        self.assertEqual(self.player.hp, 50)
        self.assertEqual(amount_healed, 0)

    def test_heal_negative(self):
        # Current implementation: negative healing will damage
        self.player.hp = 50
        amount_healed = self.player.heal(-10)
        self.assertEqual(self.player.hp, 40) # 50 + (-10) = 40
        self.assertEqual(amount_healed, -10) # Actual healed amount is -10

class TestPlayerXPAndLevelUp(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHero")
        # Initial: Level 1, XP 0, Next 100
        # Stats: Str 10, Dex 10, Int 10, Con 10, Luck 5
        # HP 100/100, MP 50/50

    def test_gain_xp_increases_xp(self):
        self.player.gain_xp(50)
        self.assertEqual(self.player.xp, 50)
        self.assertEqual(self.player.level, 1)

    def test_gain_xp_zero_or_negative(self):
        leveled_up_zero = self.player.gain_xp(0)
        self.assertEqual(self.player.xp, 0)
        self.assertFalse(leveled_up_zero)

        leveled_up_neg = self.player.gain_xp(-50)
        self.assertEqual(self.player.xp, 0) # XP should not go negative from gain_xp
        self.assertFalse(leveled_up_neg)


    def test_level_up_exact_xp(self):
        initial_stats = self.player.stats.copy()
        initial_max_hp = self.player.max_hp
        initial_max_mp = self.player.max_mp

        leveled_up = self.player.gain_xp(100)
        self.assertTrue(leveled_up)
        self.assertEqual(self.player.level, 2)
        self.assertEqual(self.player.xp, 0) # XP used for level up
        self.assertEqual(self.player.xp_to_next_level, 150) # 100 + 50

        # Check stat increases
        self.assertEqual(self.player.stats['strength'], initial_stats['strength'] + 2)
        self.assertEqual(self.player.stats['dexterity'], initial_stats['dexterity'] + 2)
        self.assertEqual(self.player.stats['intelligence'], initial_stats['intelligence'] + 2)
        self.assertEqual(self.player.stats['constitution'], initial_stats['constitution'] + 2)
        self.assertEqual(self.player.stats['luck'], initial_stats['luck'] + 1)

        # Check HP/MP are restored and max values updated
        self.assertEqual(self.player.max_hp, (initial_stats['constitution'] + 2) * 10)
        self.assertEqual(self.player.hp, self.player.max_hp)
        self.assertEqual(self.player.max_mp, (initial_stats['intelligence'] + 2) * 5)
        self.assertEqual(self.player.mp, self.player.max_mp)
        
        # Check derived stats are updated (e.g., attack_power)
        self.assertEqual(self.player.derived_stats['attack_power'], (initial_stats['strength'] + 2) * 2)

    def test_level_up_overflow_xp(self):
        self.player.gain_xp(120) # Needs 100 for level up
        self.assertEqual(self.player.level, 2)
        self.assertEqual(self.player.xp, 20) # 120 - 100 = 20 overflow
        self.assertEqual(self.player.xp_to_next_level, 150)

    def test_multiple_level_ups(self):
        # L1 (0/100) -> gain 250 XP
        # L1 -> L2: needs 100 XP. XP becomes 150. Next target: 150. Player is L2.
        # L2 -> L3: needs 150 XP. XP becomes 0. Next target: 200. Player is L3.
        initial_con = self.player.stats['constitution'] # 10
        initial_int = self.player.stats['intelligence'] # 10
        
        leveled_up = self.player.gain_xp(250) # Enough for 2 levels
        self.assertTrue(leveled_up)
        self.assertEqual(self.player.level, 3)
        self.assertEqual(self.player.xp, 0) # 250 - 100 (L1->L2) - 150 (L2->L3) = 0
        self.assertEqual(self.player.xp_to_next_level, 200) # 100 -> 150 -> 200

        # Stats after 2 level ups (each adds +2 Con, +2 Int)
        expected_con = initial_con + 2 + 2 # 14
        expected_int = initial_int + 2 + 2 # 14
        self.assertEqual(self.player.stats['constitution'], expected_con)
        self.assertEqual(self.player.stats['intelligence'], expected_int)
        self.assertEqual(self.player.max_hp, expected_con * 10) # 140
        self.assertEqual(self.player.hp, self.player.max_hp)
        self.assertEqual(self.player.max_mp, expected_int * 5)   # 70
        self.assertEqual(self.player.mp, self.player.max_mp)

    def test_level_up_method_direct_call(self):
        # Directly test the level_up method's effects
        self.player.xp = 100 # Set XP to exactly what's needed
        self.player.hp = 10 # Lower HP to check restoration
        self.player.mp = 5  # Lower MP to check restoration

        initial_stats = self.player.stats.copy()
        initial_level = self.player.level
        initial_xp_to_next = self.player.xp_to_next_level

        self.player.level_up() # Call directly

        self.assertEqual(self.player.level, initial_level + 1)
        self.assertEqual(self.player.xp, 0) # xp - initial_xp_to_next
        self.assertEqual(self.player.xp_to_next_level, initial_xp_to_next + 50)
        
        self.assertEqual(self.player.stats['strength'], initial_stats['strength'] + 2)
        self.assertEqual(self.player.stats['constitution'], initial_stats['constitution'] + 2)
        
        expected_max_hp = (initial_stats['constitution'] + 2) * 10
        expected_max_mp = (initial_stats['intelligence'] + 2) * 5
        self.assertEqual(self.player.max_hp, expected_max_hp)
        self.assertEqual(self.player.hp, expected_max_hp) # Fully restored
        self.assertEqual(self.player.max_mp, expected_max_mp)
        self.assertEqual(self.player.mp, expected_max_mp) # Fully restored

class TestPlayerDerivedStats(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHero")
        # Initial Con: 10, MaxHP: 100, HP: 100
        # Initial Int: 10, MaxMP: 50, MP: 50
        # Initial Defense: 15 (Con * 1.5)

    def test_derived_stats_update_on_stat_change(self):
        self.player.stats['constitution'] = 20
        self.player._calculate_derived_stats()

        self.assertEqual(self.player.max_hp, 200) # 20 * 10
        self.assertEqual(self.player.derived_stats['defense'], 30) # 20 * 1.5
        # HP should remain at its current value unless it exceeds new max_hp
        # In this case, max_hp increased, so hp (100) is fine.
        self.assertEqual(self.player.hp, 100) 

        self.player.stats['strength'] = 15
        self.player._calculate_derived_stats()
        self.assertEqual(self.player.derived_stats['attack_power'], 30) # 15 * 2

    def test_hp_mp_capping_on_stat_decrease(self):
        self.player.hp = self.player.max_hp # Ensure HP is full (100)
        
        self.player.stats['constitution'] = 5 # Decrease constitution
        self.player._calculate_derived_stats()

        self.assertEqual(self.player.max_hp, 50) # 5 * 10
        # HP should be capped at the new max_hp if it was higher
        self.assertEqual(self.player.hp, 50) 

        self.player.mp = self.player.max_mp # Ensure MP is full (50)
        self.player.stats['intelligence'] = 6 # Decrease intelligence
        self.player._calculate_derived_stats()
        self.assertEqual(self.player.max_mp, 30) # 6 * 5
        self.assertEqual(self.player.mp, 30)


if __name__ == '__main__':
    unittest.main()
