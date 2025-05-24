from typing import Dict, Any

# Adjust import path based on project structure
try:
    from rpg_game.core.item import Item
except ImportError:
    # Fallback for running script directly or if path is not set up
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Assuming this file is in 'core'
    from core.item import Item


class Consumable(Item):
    """
    Represents a consumable item in the RPG game, inheriting from Item.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 category: str,  # "Potion", "Special Consumable", "Food"
                 effect_description: str,
                 rarity: str = "Common",
                 recipe: str = ""):
        """
        Initializes a new consumable item.

        Args:
            name: The name of the consumable.
            description: A short description of the consumable.
            category: The category of the consumable (e.g., "Potion", "Food").
            effect_description: A description of the item's effect when used.
            rarity: The rarity of the consumable (e.g., "Common", "Rare").
            recipe: Crafting recipe for the consumable, if any.
        """
        super().__init__(name, description)
        self.category: str = category
        self.effect_description: str = effect_description
        self.rarity: str = rarity
        self.recipe: str = recipe

    def __str__(self) -> str:
        """
        Returns a string representation of the consumable.
        """
        base_str = super().__str__()
        return f"{base_str} [{self.rarity} {self.category}] (Effect: {self.effect_description})"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    crude_health_potion = Consumable(
        name="Crude Health Potion",
        description="A murky potion that restores a small amount of health.",
        category="Potion",
        effect_description="Restores 25 HP.",
        rarity="Common",
        recipe="1x Empty Vial, 2x Minor Healing Herb"
    )

    mystery_meat = Consumable(
        name="Mystery Meat Skewer",
        description="Cooked meat from an unknown creature. Surprisingly tasty.",
        category="Food",
        effect_description="Restores 10 HP and grants 'Well Fed' for 5 minutes.",
        rarity="Uncommon"
    )
    
    elixir_of_strength = Consumable(
        name="Elixir of Fleeting Strength",
        description="A sparkling liquid that temporarily boosts power.",
        category="Special Consumable",
        effect_description="Increases Attack by +5 for 1 minute.",
        rarity="Rare",
        recipe="1x Crystal Vial, 3x Tiger Lily, 1x Ogre's Tooth"
    )

    print("Created Consumables:")
    print(crude_health_potion)
    print(mystery_meat)
    print(elixir_of_strength)

    print(f"\n--- {crude_health_potion.name} ---")
    print(f"  Description: {crude_health_potion.description}")
    print(f"  Category: {crude_health_potion.category}")
    print(f"  Effect: {crude_health_potion.effect_description}")
    print(f"  Rarity: {crude_health_potion.rarity}")
    print(f"  Recipe: '{crude_health_potion.recipe}'")

    print(f"\n--- {mystery_meat.name} ---")
    print(f"  Description: {mystery_meat.description}")
    print(f"  Category: {mystery_meat.category}")
    print(f"  Effect: {mystery_meat.effect_description}")
    print(f"  Rarity: {mystery_meat.rarity}")
    print(f"  Recipe: '{mystery_meat.recipe}'") # Should be empty as not provided
    
    print(f"\n--- {elixir_of_strength.name} ---")
    print(f"  Description: {elixir_of_strength.description}")
    print(f"  Category: {elixir_of_strength.category}")
    print(f"  Effect: {elixir_of_strength.effect_description}")
    print(f"  Rarity: {elixir_of_strength.rarity}")
    print(f"  Recipe: '{elixir_of_strength.recipe}'")
