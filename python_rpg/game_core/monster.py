class Monster:
    def __init__(self, name: str, hp: int, attack_power: int, defense: int, xp_reward: int, gold_reward: int):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

    def take_damage(self, damage_amount: int) -> bool:
        """
        Reduces the monster's HP by the given damage amount.
        Prints damage taken and defeat messages.
        Returns True if the monster is defeated, False otherwise.
        """
        actual_damage = max(0, damage_amount) # Ensure damage is not negative
        self.hp -= actual_damage
        print(f"{self.name} takes {actual_damage} damage.")

        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name} has been defeated.")
            return True
        return False

    def is_alive(self) -> bool:
        """Checks if the monster is still alive."""
        return self.hp > 0

    def __str__(self) -> str:
        """Returns a string representation of the monster."""
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    goblin = Monster(name="Goblin Grunt", hp=30, attack_power=8, defense=4, xp_reward=10, gold_reward=5)
    print(goblin)

    print("\n--- Simulating Combat ---")
    goblin.take_damage(10)
    print(goblin)

    if goblin.is_alive():
        print(f"{goblin.name} is still alive.")
    else:
        print(f"{goblin.name} is no longer alive.")

    goblin.take_damage(15)
    print(goblin)

    goblin.take_damage(10) # Should be enough to defeat
    print(goblin)

    if goblin.is_alive():
        print(f"{goblin.name} is still alive.")
    else:
        print(f"{goblin.name} is no longer alive.")

    # Test taking damage when already defeated
    goblin.take_damage(5)
    print(goblin)
