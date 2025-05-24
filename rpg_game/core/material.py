# Adjust import path based on project structure
try:
    from rpg_game.core.item import Item
except ImportError:
    # Fallback for running script directly or if path is not set up
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Assuming this file is in 'core'
    from core.item import Item


class Material(Item):
    """
    Represents a crafting material in the RPG game, inheriting from Item.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 rarity: str = "Common"):
        """
        Initializes a new material item.

        Args:
            name: The name of the material.
            description: A short description of the material.
            rarity: The rarity of the material (e.g., "Common", "Uncommon", "Rare").
        """
        super().__init__(name, description)
        self.rarity: str = rarity

    def __str__(self) -> str:
        """
        Returns a string representation of the material.
        """
        base_str = super().__str__()
        return f"{base_str} [{self.rarity}]"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    chomper_filet = Material(
        name="Chomper Filet",
        description="A raw, surprisingly tender piece of meat from a Chomper. Used in cooking.",
        rarity="Common"
    )

    iron_ingot = Material(
        name="Iron Ingot",
        description="A bar of refined iron, ready for smithing.",
        rarity="Common"
    )

    spirit_essence = Material(
        name="Spirit Essence",
        description="A shimmering mote of captured spirit energy. Used in enchanting.",
        rarity="Uncommon"
    )
    
    dragon_scale = Material(
        name="Dragon Scale",
        description="A large, incredibly durable scale from a dragon.",
        rarity="Epic"
    )

    print("Created Materials:")
    print(chomper_filet)
    print(iron_ingot)
    print(spirit_essence)
    print(dragon_scale)

    print(f"\n--- {chomper_filet.name} ---")
    print(f"  Description: {chomper_filet.description}")
    print(f"  Rarity: {chomper_filet.rarity}")

    print(f"\n--- {iron_ingot.name} ---")
    print(f"  Description: {iron_ingot.description}")
    print(f"  Rarity: {iron_ingot.rarity}")

    print(f"\n--- {spirit_essence.name} ---")
    print(f"  Description: {spirit_essence.description}")
    print(f"  Rarity: {spirit_essence.rarity}")
    
    print(f"\n--- {dragon_scale.name} ---")
    print(f"  Description: {dragon_scale.description}")
    print(f"  Rarity: {dragon_scale.rarity}")
