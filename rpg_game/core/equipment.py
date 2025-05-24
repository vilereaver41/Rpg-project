from typing import Optional
# Assuming Item class is in rpg_game.core.item
# Adjust import path if necessary based on actual project structure
try:
    from rpg_game.core.item import Item
except ImportError:
    # Fallback for running script directly or if path is not set up
    import sys
    import os
    # Add the parent directory of 'core' to sys.path
    # This assumes equipment.py is in 'core' and item.py is also in 'core'
    # and 'rpg_game' is the top-level package.
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.item import Item


class Equipment(Item):
    """
    Represents a piece of equipment in the RPG game, inheriting from Item.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 tier: str,
                 equip_type: str,
                 attack_bonus: int = 0,
                 defense_bonus: int = 0,
                 magic_attack_bonus: int = 0,
                 magic_defense_bonus: int = 0,
                 agility_bonus: int = 0,
                 luck_bonus: int = 0,
                 max_hp_bonus: int = 0,
                 max_mp_bonus: int = 0,
                 extra_increases: str = "",
                 recipe: str = "",
                 source: str = ""):
        """
        Initializes a new piece of equipment.

        Args:
            name: The name of the equipment.
            description: A short description of the equipment.
            tier: The tier of the equipment (e.g., "Common", "Rare", "Epic").
            equip_type: The type of equipment (e.g., "Helmet", "Armor", "Weapon").
            attack_bonus: Bonus to physical attack.
            defense_bonus: Bonus to physical defense.
            magic_attack_bonus: Bonus to magic attack.
            magic_defense_bonus: Bonus to magic defense.
            agility_bonus: Bonus to agility.
            luck_bonus: Bonus to luck.
            max_hp_bonus: Bonus to maximum HP.
            max_mp_bonus: Bonus to maximum MP.
            extra_increases: Any other increases the equipment provides (e.g. "Fire Resistance +10%").
            recipe: Crafting recipe for the equipment, if any.
            source: How the equipment is obtained (e.g., "Monster Drop", "Quest Reward").
        """
        super().__init__(name, description)
        self.tier: str = tier
        self.equip_type: str = equip_type
        self.attack_bonus: int = attack_bonus
        self.defense_bonus: int = defense_bonus
        self.magic_attack_bonus: int = magic_attack_bonus
        self.magic_defense_bonus: int = magic_defense_bonus
        self.agility_bonus: int = agility_bonus
        self.luck_bonus: int = luck_bonus
        self.max_hp_bonus: int = max_hp_bonus
        self.max_mp_bonus: int = max_mp_bonus
        self.extra_increases: str = extra_increases
        self.recipe: str = recipe
        self.source: str = source

    def __str__(self) -> str:
        """
        Returns a string representation of the equipment, including its bonuses.
        """
        base_str = super().__str__()
        bonus_strs = []
        if self.attack_bonus: bonus_strs.append(f"ATK+{self.attack_bonus}")
        if self.defense_bonus: bonus_strs.append(f"DEF+{self.defense_bonus}")
        if self.magic_attack_bonus: bonus_strs.append(f"M.ATK+{self.magic_attack_bonus}")
        if self.magic_defense_bonus: bonus_strs.append(f"M.DEF+{self.magic_defense_bonus}")
        if self.agility_bonus: bonus_strs.append(f"AGI+{self.agility_bonus}")
        if self.luck_bonus: bonus_strs.append(f"LCK+{self.luck_bonus}")
        if self.max_hp_bonus: bonus_strs.append(f"MaxHP+{self.max_hp_bonus}")
        if self.max_mp_bonus: bonus_strs.append(f"MaxMP+{self.max_mp_bonus}")
        if self.extra_increases: bonus_strs.append(self.extra_increases)

        details = f"{base_str} ({self.tier} {self.equip_type})"
        if bonus_strs:
            details += " [" + ", ".join(bonus_strs) + "]"
        if self.source:
            details += f" (Source: {self.source})"
        return details

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    leather_cap = Equipment(
        name="Leather Cap",
        description="A simple cap made of sturdy leather.",
        tier="Common",
        equip_type="Helmet",
        defense_bonus=2,
        agility_bonus=1,
        source="Crafted"
    )

    iron_sword = Equipment(
        name="Iron Sword",
        description="A basic but reliable sword.",
        tier="Common",
        equip_type="Weapon",
        attack_bonus=5,
        recipe="3 Iron Ingots, 1 Leather Strip",
        source="Blacksmith"
    )
    
    wizard_robe = Equipment(
        name="Apprentice Robe",
        description="Robe worn by apprentice mages.",
        tier="Common",
        equip_type="Armor",
        magic_defense_bonus=3,
        max_mp_bonus=10,
        extra_increases="Mana Regen +1",
        source="Mage Guild Shop"
    )

    print("Created Equipment:")
    print(leather_cap)
    print(iron_sword)
    print(wizard_robe)

    print(f"\n--- {leather_cap.name} ---")
    print(f"  Description: {leather_cap.description}")
    print(f"  Tier: {leather_cap.tier}")
    print(f"  Type: {leather_cap.equip_type}")
    print(f"  Defense Bonus: {leather_cap.defense_bonus}")
    print(f"  Agility Bonus: {leather_cap.agility_bonus}")
    print(f"  Magic Attack Bonus: {leather_cap.magic_attack_bonus}") # Should be 0
    print(f"  Recipe: '{leather_cap.recipe}'") # Should be ""
    print(f"  Source: {leather_cap.source}")

    print(f"\n--- {iron_sword.name} ---")
    print(f"  Tier: {iron_sword.tier}, Type: {iron_sword.equip_type}")
    print(f"  Attack Bonus: {iron_sword.attack_bonus}")
    print(f"  Recipe: '{iron_sword.recipe}'")
    print(f"  Source: {iron_sword.source}")

    print(f"\n--- {wizard_robe.name} ---")
    print(f"  Tier: {wizard_robe.tier}, Type: {wizard_robe.equip_type}")
    print(f"  Magic Defense Bonus: {wizard_robe.magic_defense_bonus}")
    print(f"  Max MP Bonus: {wizard_robe.max_mp_bonus}")
    print(f"  Extra Increases: '{wizard_robe.extra_increases}'")
    print(f"  Source: {wizard_robe.source}")
