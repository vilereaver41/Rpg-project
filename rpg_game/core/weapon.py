from typing import Optional

# Adjust import path based on project structure
try:
    from rpg_game.core.equipment import Equipment
except ImportError:
    # Fallback for running script directly or if path is not set up
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Assuming this file is in 'core'
    from core.equipment import Equipment


class Weapon(Equipment):
    """
    Represents a weapon in the RPG game, inheriting from Equipment.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 tier: str,
                 equip_type: str,  # e.g., "Main Hand", "Offhand", "Two-Hand"
                 attack_type: str, # e.g., "Physical", "Fire", "Nil Element"
                 weapon_category: str, # e.g., "Sword", "Dagger", "Axe"
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
        Initializes a new weapon.

        Args:
            name: The name of the weapon.
            description: A short description of the weapon.
            tier: The tier of the weapon.
            equip_type: The type of equipment (e.g., "Main Hand", "Offhand").
            attack_type: The elemental or physical type of the weapon's attack.
            weapon_category: The category of the weapon (e.g., "Sword", "Axe").
            attack_bonus: Bonus to physical attack.
            defense_bonus: Bonus to physical defense.
            magic_attack_bonus: Bonus to magic attack.
            magic_defense_bonus: Bonus to magic defense.
            agility_bonus: Bonus to agility.
            luck_bonus: Bonus to luck.
            max_hp_bonus: Bonus to maximum HP.
            max_mp_bonus: Bonus to maximum MP.
            extra_increases: Any other increases the equipment provides.
            recipe: Crafting recipe for the equipment, if any.
            source: How the equipment is obtained.
        """
        super().__init__(name=name,
                         description=description,
                         tier=tier,
                         equip_type=equip_type,
                         attack_bonus=attack_bonus,
                         defense_bonus=defense_bonus,
                         magic_attack_bonus=magic_attack_bonus,
                         magic_defense_bonus=magic_defense_bonus,
                         agility_bonus=agility_bonus,
                         luck_bonus=luck_bonus,
                         max_hp_bonus=max_hp_bonus,
                         max_mp_bonus=max_mp_bonus,
                         extra_increases=extra_increases,
                         recipe=recipe,
                         source=source)
        
        self.attack_type: str = attack_type
        self.weapon_category: str = weapon_category

    def __str__(self) -> str:
        """
        Returns a string representation of the weapon.
        """
        base_str = super().__str__()
        # Example: "Iron Sword: A basic sword. (Common Main Hand) [ATK+5] (Source: Blacksmith) - Physical Sword"
        # Remove the closing parenthesis from base_str if it exists, add weapon details, then add it back or form new.
        
        # super().__str__() returns something like:
        # "Iron Sword: A basic but reliable sword. (Common Main Hand) [ATK+5] (Source: Blacksmith)"
        # We want to insert weapon specific details.
        
        # Find the position of the first opening parenthesis of the details part from Equipment's __str__
        details_start_index = base_str.find(" (") 
        if details_start_index != -1:
            main_part = base_str[:details_start_index]
            details_part = base_str[details_start_index:]
            return f"{main_part} ({self.attack_type} {self.weapon_category}){details_part}"
        else: # Should not happen if Equipment.__str__ is consistent
            return f"{base_str} ({self.attack_type} {self.weapon_category})"


if __name__ == '__main__':
    # Example Usage (for testing purposes)
    iron_sword = Weapon(
        name="Iron Sword",
        description="A trusty blade for novice adventurers.",
        tier="Common",
        equip_type="Main Hand", # Correctly passing equip_type
        attack_type="Physical",
        weapon_category="Sword",
        attack_bonus=5,
        luck_bonus=1,
        recipe="3 Iron Ingots, 1 Leather Strap",
        source="Crafted at Blacksmith"
    )

    fire_dagger = Weapon(
        name="Fire Dagger",
        description="A dagger that burns with magical fire.",
        tier="Uncommon",
        equip_type="Offhand",
        attack_type="Fire",
        weapon_category="Dagger",
        attack_bonus=3,
        magic_attack_bonus=4, # Dagger might have some magic scaling
        agility_bonus=2,
        extra_increases="Chance to inflict 'Burn' status",
        source="Dropped by Fire Lizards"
    )

    print("Created Weapons:")
    print(iron_sword)
    print(fire_dagger)

    print(f"\n--- {iron_sword.name} Details ---")
    print(f"  Name: {iron_sword.name}")
    print(f"  Description: {iron_sword.description}")
    print(f"  Tier: {iron_sword.tier}")
    print(f"  Equip Type: {iron_sword.equip_type}")
    print(f"  Attack Type: {iron_sword.attack_type}")
    print(f"  Weapon Category: {iron_sword.weapon_category}")
    print(f"  Attack Bonus: {iron_sword.attack_bonus}")
    print(f"  Defense Bonus: {iron_sword.defense_bonus}") # Should be 0
    print(f"  Magic Attack Bonus: {iron_sword.magic_attack_bonus}") # Should be 0
    print(f"  Magic Defense Bonus: {iron_sword.magic_defense_bonus}") # Should be 0
    print(f"  Agility Bonus: {iron_sword.agility_bonus}") # Should be 0
    print(f"  Luck Bonus: {iron_sword.luck_bonus}")
    print(f"  Max HP Bonus: {iron_sword.max_hp_bonus}") # Should be 0
    print(f"  Max MP Bonus: {iron_sword.max_mp_bonus}") # Should be 0
    print(f"  Extra Increases: '{iron_sword.extra_increases}'") # Should be ""
    print(f"  Recipe: '{iron_sword.recipe}'")
    print(f"  Source: '{iron_sword.source}'")

    print(f"\n--- {fire_dagger.name} Details ---")
    print(f"  Name: {fire_dagger.name}")
    print(f"  Description: {fire_dagger.description}")
    print(f"  Tier: {fire_dagger.tier}")
    print(f"  Equip Type: {fire_dagger.equip_type}")
    print(f"  Attack Type: {fire_dagger.attack_type}")
    print(f"  Weapon Category: {fire_dagger.weapon_category}")
    print(f"  Attack Bonus: {fire_dagger.attack_bonus}")
    print(f"  Magic Attack Bonus: {fire_dagger.magic_attack_bonus}")
    print(f"  Agility Bonus: {fire_dagger.agility_bonus}")
    print(f"  Extra Increases: '{fire_dagger.extra_increases}'")
    print(f"  Source: '{fire_dagger.source}'")
    print(f"  Recipe: '{fire_dagger.recipe}'") # Should be ""
