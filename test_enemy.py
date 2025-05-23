import unittest
from enemy import Enemy

class TestEnemy(unittest.TestCase):
    def setUp(self):
        """Set up for test methods."""
        self.enemy = Enemy(
            name="Test Goblin",
            max_hp=50,
            attack_power=10,
            defense=5,
            accuracy=70.0,
            evasion=10.0,
            critical_hit_chance=5.0,
            xp_reward=20
        )

    def test_enemy_creation(self):
        self.assertEqual(self.enemy.get_name(), "Test Goblin")
        self.assertEqual(self.enemy.get_max_hp(), 50)
        self.assertEqual(self.enemy.get_current_hp(), 50)
        self.assertEqual(self.enemy.get_attack_power(), 10)
        self.assertEqual(self.enemy.get_defense(), 5) # Base defense
        self.assertEqual(self.enemy.get_accuracy(), 70.0)
        self.assertEqual(self.enemy.get_evasion(), 10.0)
        self.assertEqual(self.enemy.get_critical_hit_chance(), 5.0)
        self.assertEqual(self.enemy.xp_reward, 20)
        self.assertTrue(self.enemy.is_alive())
        self.assertFalse(self.enemy.is_defending)

    def test_take_damage(self):
        initial_hp = self.enemy.get_current_hp()
        self.enemy.take_damage(10)
        self.assertEqual(self.enemy.get_current_hp(), initial_hp - 10)
        self.assertTrue(self.enemy.is_alive())

        # Test minimum 1 damage
        self.enemy.current_hp = 10
        self.enemy.take_damage(0) # Damage is 0
        self.assertEqual(self.enemy.get_current_hp(), 10 - 1) # Should take 1 damage

        self.enemy.current_hp = 5
        self.enemy.take_damage(10) # More damage than current HP
        self.assertEqual(self.enemy.get_current_hp(), 0)
        self.assertFalse(self.enemy.is_alive())

    def test_take_damage_while_defending(self):
        initial_hp = self.enemy.get_current_hp()
        self.enemy.start_defending()
        self.assertTrue(self.enemy.is_defending)

        self.enemy.take_damage(20) # Damage should be halved (20 / 2 = 10)
        self.assertEqual(self.enemy.get_current_hp(), initial_hp - 10)
        self.assertFalse(self.enemy.is_defending) # Defense should wear off
        self.assertTrue(self.enemy.is_alive())

        # Test minimum 1 damage while defending
        self.enemy.current_hp = 10
        self.enemy.start_defending()
        self.enemy.take_damage(1) # Damage is 1, halved is 0, but should be 1
        self.assertEqual(self.enemy.get_current_hp(), 10 - 1)

    def test_is_alive(self):
        self.assertTrue(self.enemy.is_alive())
        self.enemy.current_hp = 0
        self.assertFalse(self.enemy.is_alive())
        self.enemy.current_hp = -10 # Should still be not alive
        self.assertFalse(self.enemy.is_alive())

    def test_start_and_reset_defense(self):
        self.assertFalse(self.enemy.is_defending)
        self.enemy.start_defending()
        self.assertTrue(self.enemy.is_defending)
        
        # Calling start_defending again should not change anything if already defending
        self.enemy.start_defending()
        self.assertTrue(self.enemy.is_defending)

        self.enemy.reset_defense()
        self.assertFalse(self.enemy.is_defending)
        
        # Calling reset_defense again should not change anything if not defending
        self.enemy.reset_defense()
        self.assertFalse(self.enemy.is_defending)

if __name__ == '__main__':
    unittest.main()
