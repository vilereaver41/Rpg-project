class Enemy:
    """
    Represents an enemy in the RPG game.
    """
    def __init__(self, name: str, hp: int, attack_power: int, defense: int):
        """
        Initializes a new enemy.

        Args:
            name: The name of the enemy.
            hp: The current and maximum health points of the enemy.
            attack_power: The attack power of the enemy.
            defense: The defense value of the enemy.
        """
        self.name: str = name
        self.hp: int = hp
        self.max_hp: int = hp # Assuming initial HP is max HP
        self.attack_power: int = attack_power
        self.defense: int = defense

    def take_damage(self, amount: int) -> int:
        """
        Reduces enemy's HP by the given amount.

        Args:
            amount: The amount of damage to take.

        Returns:
            The actual amount of damage taken.
        """
        actual_damage = min(self.hp, amount)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        """
        Checks if the enemy is still alive.

        Returns:
            True if hp > 0, False otherwise.
        """
        return self.hp > 0

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    enemy = Enemy("Goblin", 50, 8, 4)
    print(f"Enemy: {enemy.name}, HP: {enemy.hp}/{enemy.max_hp}, Attack: {enemy.attack_power}, Defense: {enemy.defense}")

    damage_taken = enemy.take_damage(10)
    print(f"{enemy.name} took {damage_taken} damage. Current HP: {enemy.hp}")

    damage_taken = enemy.take_damage(100) # More than current HP
    print(f"{enemy.name} took {damage_taken} damage. Current HP: {enemy.hp}")
    print(f"Is {enemy.name} alive? {enemy.is_alive()}")

    enemy2 = Enemy("Orc", 100, 15, 10)
    print(f"Is {enemy2.name} alive? {enemy2.is_alive()}")
