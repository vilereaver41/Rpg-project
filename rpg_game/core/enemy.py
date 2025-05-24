from typing import List, Optional
# Import Skill and Item for type hinting
try:
    from rpg_game.core.skill import Skill
    from rpg_game.core.item import Item
except ImportError:
    # Fallback for cases where the script might be run directly or path issues
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '.')) # Assuming skill.py and item.py are in the same directory (core)
    from skill import Skill
    from item import Item

class Enemy:
    """
    Represents an enemy in the RPG game.
    """
    def __init__(self, name: str, max_hp: int, attack_power: int, defense: int,
                 level_range: str, spawn_chance: str, enemy_type: str,
                 max_mp: int, magic_attack: int, magic_defense: int,
                 agility: int, luck: int, has_sprite: bool,
                 abilities_spells: List[Skill], loot: List[Item],
                 zone_name: Optional[str] = None):
        """
        Initializes a new enemy.

        Args:
            name: The name of the enemy.
            max_hp: The maximum health points of the enemy.
            attack_power: The attack power of the enemy.
            defense: The defense value of the enemy.
            level_range: The level range of the enemy (e.g., "1-5").
            spawn_chance: The chance of spawning the enemy (e.g., "Common").
            enemy_type: The type of the enemy (e.g., "Goblin", "Undead").
            max_mp: The maximum magic points of the enemy.
            magic_attack: The magic attack power of the enemy.
            magic_defense: The magic defense value of the enemy.
            agility: The agility of the enemy.
            luck: The luck of the enemy.
            has_sprite: Whether the enemy has a sprite.
            abilities_spells: A list of Skill objects the enemy has.
            loot: A list of Item objects the enemy can drop.
            zone_name: The name of the zone this enemy instance might be associated with.
        """
        self.name: str = name
        self.max_hp: int = max_hp
        self.hp: int = self.max_hp  # Current HP initialized to max_hp
        self.attack_power: int = attack_power
        self.defense: int = defense
        self.level_range: str = level_range
        self.spawn_chance: str = spawn_chance
        self.enemy_type: str = enemy_type
        self.max_mp: int = max_mp
        self.magic_attack: int = magic_attack
        self.magic_defense: int = magic_defense
        self.agility: int = agility
        self.luck: int = luck
        self.has_sprite: bool = has_sprite
        self.abilities_spells: List[Skill] = abilities_spells
        self.loot: List[Item] = loot
        self.zone_name: Optional[str] = zone_name

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

    def get_loot(self) -> List[Item]:
        """
        Returns the loot the enemy can drop.
        """
        return self.loot

    def use_ability(self, ability_name: str) -> None:
        """
        Uses an ability or spell.
        (Placeholder implementation)
        """
        pass

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    # This example needs to be updated to use actual Skill and Item objects
    # For now, we'll use mock objects or skip detailed instantiation here
    # as the main test for this will be in the loader and game data manager.

    # Mock Skill and Item classes for standalone testing if real ones are complex to init here
    class MockSkill:
        def __init__(self, name): self.name = name
        def __repr__(self): return f"MockSkill(name='{self.name}')"

    class MockItem:
        def __init__(self, name): self.name = name
        def __repr__(self): return f"MockItem(name='{self.name}')"

    goblin_loot_objects = [MockItem(name="Gold Coin"), MockItem(name="Rusty Dagger")]
    goblin_ability_objects = [MockSkill(name="Scratch"), MockSkill(name=" पत्थर फेंकना")]
    
    enemy = Enemy(
        name="Goblin",
        max_hp=50,
        attack_power=8,
        defense=4,
        level_range="1-3",
        spawn_chance="Common",
        enemy_type="Goblinoid",
        max_mp=10,
        magic_attack=2,
        magic_defense=1,
        agility=5,
        luck=2,
        has_sprite=True,
        abilities_spells=goblin_ability_objects,
        loot=goblin_loot_objects,
        zone_name="Goblin Test Zone"
    )
    print(f"Enemy: {enemy.name}, Type: {enemy.enemy_type}, HP: {enemy.hp}/{enemy.max_hp}, MP: {enemy.max_mp}, Zone: {enemy.zone_name}")
    print(f"Attack: {enemy.attack_power}, Magic Attack: {enemy.magic_attack}, Agility: {enemy.agility}")
    
    # Printing object lists will show their repr
    print(f"Abilities: {enemy.abilities_spells}")
    # Example of accessing names from the objects
    goblin_loot_names = [item.name for item in enemy.get_loot()]
    print(f"Potential Loot: {goblin_loot_names}")


    damage_taken = enemy.take_damage(10)
    print(f"{enemy.name} took {damage_taken} damage. Current HP: {enemy.hp}")

    damage_taken = enemy.take_damage(100) # More than current HP
    print(f"{enemy.name} took {damage_taken} damage. Current HP: {enemy.hp}")
    print(f"Is {enemy.name} alive? {enemy.is_alive()}")

    orc_ability_objects = [MockSkill(name="Heavy Swing"), MockSkill(name="Warcry")]
    orc_loot_objects = [MockItem(name="Iron Axe"), MockItem(name="Orcish Helm")]
    enemy2 = Enemy(
        name="Orc",
        max_hp=100,
        attack_power=15,
        defense=10,
        level_range="5-8",
        spawn_chance="Uncommon",
        enemy_type="Orcish",
        max_mp=5,
        magic_attack=1,
        magic_defense=5,
        agility=3,
        luck=1,
        has_sprite=True,
        abilities_spells=orc_ability_objects,
        loot=orc_loot_objects,
        zone_name=None # Example with no zone
    )
    print(f"\nEnemy: {enemy2.name}, Type: {enemy2.enemy_type}, HP: {enemy2.hp}/{enemy2.max_hp}, MP: {enemy2.max_mp}, Zone: {enemy2.zone_name}")
    print(f"Is {enemy2.name} alive? {enemy2.is_alive()}")
    # Example of accessing names from the objects
    orc_loot_names = [item.name for item in enemy2.get_loot()]
    print(f"{enemy2.name} (Type: {enemy2.enemy_type}) drops: {orc_loot_names}")
