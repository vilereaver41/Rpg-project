import random

class Enemy:
    """
    Represents an enemy character in the RPG.
    Handles stats, combat actions, and state.
    """
    def __init__(self, name: str, max_hp: int, attack_power: int, defense: int,
                 accuracy: float, evasion: float, critical_hit_chance: float, xp_reward: int):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_power = attack_power
        self.base_defense = defense  # Store base defense
        self.accuracy = accuracy  # Percentage (e.g., 70.0 for 70%)
        self.evasion = evasion  # Percentage (e.g., 10.0 for 10%)
        self.critical_hit_chance = critical_hit_chance  # Percentage (e.g., 5.0 for 5%)
        self.xp_reward = xp_reward
        self.is_defending = False  # Flag for defend action

    def get_name(self) -> str:
        return self.name

    def get_current_hp(self) -> int:
        return self.current_hp

    def get_max_hp(self) -> int:
        return self.max_hp

    def get_attack_power(self) -> int:
        """Returns the attack power of the enemy."""
        return self.attack_power

    def get_defense(self) -> int:
        """Returns the base defense of the enemy."""
        # The combat_attack function calculates damage against this base defense.
        # The take_damage method then applies the 50% reduction if defending.
        return self.base_defense

    def get_accuracy(self) -> float:
        """Returns the accuracy of the enemy."""
        return self.accuracy

    def get_evasion(self) -> float:
        """Returns the evasion of the enemy."""
        return self.evasion

    def get_critical_hit_chance(self) -> float:
        """Returns the critical hit chance of the enemy."""
        return self.critical_hit_chance

    def take_damage(self, damage: int):
        """
        Reduces enemy's HP by the damage amount.
        If the enemy is defending, damage is halved and defense state is reset.
        """
        actual_damage = damage
        if self.is_defending:
            print(f"{self.name} is defending and takes reduced damage!")
            actual_damage = damage // 2  # Takes 50% less damage
            self.reset_defense()  # Defend wears off after taking a hit

        actual_damage = max(1, actual_damage)  # Ensure at least 1 damage is dealt

        self.current_hp -= actual_damage
        if self.current_hp < 0:
            self.current_hp = 0
        
        print(f"{self.name} takes {actual_damage} damage. HP: {self.current_hp}/{self.max_hp}")
        if not self.is_alive():
            print(f"{self.name} has been defeated!")

    def is_alive(self) -> bool:
        """Checks if the enemy is still alive."""
        return self.current_hp > 0

    def start_defending(self):
        """Sets the enemy to defend for the next incoming attack."""
        if not self.is_defending:
            print(f"{self.name} takes a defensive stance!")
            self.is_defending = True

    def reset_defense(self):
        """Resets the enemy's defense state."""
        if self.is_defending:
            # print(f"{self.name} is no longer defending.") # Optional: can be a bit verbose
            self.is_defending = False
