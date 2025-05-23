import unittest
from unittest.mock import patch
import io # For capturing print output

from player import Player
from enemy import Enemy
from combat import combat_attack, start_battle, calculate_hit
from items import Weapon, ItemRarity

class TestCombat(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test Player")
        # Give player some base stats and a weapon for predictability
        self.player._base_strength = 10 # AP = 20
        self.player._base_dexterity = 10
        self.player._base_constitution = 10
        self.player._base_intelligence = 10
        self.player._base_luck = 10
        
        # Re-initialize HP/MP after setting base stats
        self.player.current_hp = self.player.get_max_hp()
        self.player.current_mp = self.player.get_max_mp()

        self.weapon = Weapon("Test Sword", "desc", ItemRarity.COMMON, attack_bonus=5) # Total AP = 20+5 = 25
        self.player.add_item_to_inventory(self.weapon)
        self.player.equip(self.weapon)
        
        self.enemy = Enemy(name="Test Enemy", max_hp=100, attack_power=10, defense=5,
                           accuracy=70.0, evasion=10.0, critical_hit_chance=0.0, xp_reward=10) # No crit for predictability

    def test_calculate_hit(self):
        self.assertTrue(calculate_hit(attacker_accuracy=100, defender_evasion=0)) # Guaranteed hit
        self.assertFalse(calculate_hit(attacker_accuracy=0, defender_evasion=100)) # Guaranteed miss
        
        # Test clamping: Accuracy - Evasion = 50. Roll <= 50 means hit.
        # Effective hit chance = max(5.0, min(Accuracy - Evasion, 95.0))
        self.assertTrue(calculate_hit(attacker_accuracy=70, defender_evasion=20)) # 50%
        
        # Test lower clamp
        with patch('random.uniform', return_value=4.9): # Roll 4.9, Hit chance 70-70=0, clamped to 5%. Hit.
            self.assertTrue(calculate_hit(attacker_accuracy=70, defender_evasion=70))
        with patch('random.uniform', return_value=5.1): # Roll 5.1, Hit chance 70-70=0, clamped to 5%. Miss.
            self.assertFalse(calculate_hit(attacker_accuracy=70, defender_evasion=70))
            
        # Test upper clamp
        with patch('random.uniform', return_value=94.9): # Roll 94.9, Hit chance 100-0=100, clamped to 95%. Hit.
            self.assertTrue(calculate_hit(attacker_accuracy=100, defender_evasion=0))
        with patch('random.uniform', return_value=95.1): # Roll 95.1, Hit chance 100-0=100, clamped to 95%. Miss.
            self.assertFalse(calculate_hit(attacker_accuracy=100, defender_evasion=0))


    @patch('combat.calculate_hit', return_value=True) # Ensure attack always hits for damage tests
    @patch('sys.stdout', new_callable=io.StringIO) # Capture print output
    def test_combat_attack_damage_calculation(self, mock_stdout, mock_calculate_hit):
        # Player (AP 25) attacks Enemy (DEF 5)
        # Expected damage = 25 - 5 = 20
        initial_enemy_hp = self.enemy.get_current_hp()
        combat_attack(self.player, self.enemy)
        self.assertEqual(self.enemy.get_current_hp(), initial_enemy_hp - 20)

        # Enemy (AP 10) attacks Player (DEF varies based on CON + DEX/2 + equip)
        # Player base DEF = 10 (CON) + 10/2 (DEX) = 15. No armor equipped in this setup for base player.
        # So, player get_defense() should be 15.
        initial_player_hp = self.player.get_current_hp()
        combat_attack(self.enemy, self.player)
        expected_player_damage = self.enemy.get_attack_power() - self.player.get_defense()
        expected_player_damage = max(1, expected_player_damage) # Min 1 damage
        self.assertEqual(self.player.get_current_hp(), initial_player_hp - expected_player_damage)
    
    @patch('combat.calculate_hit', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_combat_attack_critical_hit(self, mock_stdout, mock_calculate_hit):
        self.player.get_critical_hit_chance = lambda: 100.0 # Guaranteed crit for player
        
        initial_enemy_hp = self.enemy.get_current_hp()
        base_damage = self.player.get_attack_power() - self.enemy.get_defense()
        crit_damage = int(base_damage * 1.5)
        
        combat_attack(self.player, self.enemy)
        self.assertEqual(self.enemy.get_current_hp(), initial_enemy_hp - crit_damage)
        self.assertIn("CRITICAL HIT", mock_stdout.getvalue())

    @patch('combat.calculate_hit', return_value=False) # Ensure attack always misses
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_combat_attack_miss(self, mock_stdout, mock_calculate_hit):
        initial_enemy_hp = self.enemy.get_current_hp()
        combat_attack(self.player, self.enemy)
        self.assertEqual(self.enemy.get_current_hp(), initial_enemy_hp) # HP unchanged
        self.assertIn("MISSED", mock_stdout.getvalue())

    @patch('combat.calculate_hit', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_combat_attack_defender_defending(self, mock_stdout, mock_calculate_hit):
        initial_enemy_hp = self.enemy.get_current_hp()
        self.enemy.start_defending() # Enemy is defending
        
        base_damage = self.player.get_attack_power() - self.enemy.get_defense() # Enemy def is base
        damage_when_defending = base_damage // 2
        damage_when_defending = max(1, damage_when_defending)

        combat_attack(self.player, self.enemy)
        self.assertEqual(self.enemy.get_current_hp(), initial_enemy_hp - damage_when_defending)
        self.assertFalse(self.enemy.is_defending) # Defense wears off

    @patch('combat.calculate_hit', return_value=True)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_combat_attack_attacker_resets_defense(self, mock_stdout, mock_calculate_hit):
        self.player.start_defending()
        self.assertTrue(self.player.is_defending)
        combat_attack(self.player, self.enemy) # Player attacks
        self.assertFalse(self.player.is_defending) # Player should no longer be defending

    # Tests for start_battle are more complex due to input() and the game loop.
    # We'll test a simple win/loss scenario by manipulating HP.
    @patch('builtins.input', return_value="1") # Player always chooses action "1" (Attack)
    @patch('sys.stdout', new_callable=io.StringIO) # Capture print output
    def test_start_battle_player_wins(self, mock_stdout, mock_input):
        # Make enemy very weak so player wins in one hit
        self.enemy.current_hp = 1
        self.enemy.max_hp = 1 
        self.player.current_hp = self.player.get_max_hp() # Ensure player is full HP
        
        start_battle(self.player, self.enemy)
        
        self.assertTrue(self.player.is_alive())
        self.assertFalse(self.enemy.is_alive())
        self.assertGreater(self.player.get_xp(), 0) # Player should gain XP
        self.assertIn(f"{self.enemy.get_name()} was defeated!", mock_stdout.getvalue())
        self.assertIn("--- Battle End ---", mock_stdout.getvalue())

    @patch('builtins.input', return_value="1") 
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_start_battle_enemy_wins(self, mock_stdout, mock_input):
        # Make player very weak
        self.player.current_hp = 1
        # Make enemy strong enough to one-shot
        self.enemy.attack_power = 100 
        self.enemy.accuracy = 100 # Ensure enemy hits
        self.player.get_evasion = lambda: 0 # Ensure player doesn't evade

        start_battle(self.player, self.enemy)

        self.assertFalse(self.player.is_alive())
        self.assertTrue(self.enemy.is_alive())
        self.assertIn(f"{self.player.get_name()} was defeated!", mock_stdout.getvalue())
        self.assertIn("--- Battle End ---", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
