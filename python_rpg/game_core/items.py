import sys
import os

# Ensure the package root (python_rpg) is in sys.path for absolute imports
# This allows 'from game_core.rarity import Rarity' to work both when items.py
# is imported as a module and when it's run directly.
_PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, _PACKAGE_ROOT)

from game_core.rarity import Rarity

class Item:
    def __init__(self, name: str, description: str, rarity: Rarity, value: int):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.value = value

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity.display_name}) - Value: {self.value} G"

    def __repr__(self) -> str:
        return f"Item(name='{self.name}', rarity=Rarity.{self.rarity.name})"

class Equipment(Item):
    def __init__(self, name: str, description: str, rarity: Rarity, value: int, slot: str, stat_bonuses: dict):
        super().__init__(name, description, rarity, value)
        self.slot = slot
        if not isinstance(stat_bonuses, dict):
            raise TypeError("stat_bonuses must be a dictionary")
        self.stat_bonuses = stat_bonuses

    def __str__(self) -> str:
        # Example: "Rusty Sword (Common) - Slot: Weapon, Bonuses: {'attack_power': 3}, Value: 5 G"
        return (f"{self.name} ({self.rarity.display_name}) - Slot: {self.slot}, "
                f"Bonuses: {self.stat_bonuses}, Value: {self.value} G")

    def __repr__(self) -> str:
        return (f"Equipment(name='{self.name}', rarity=Rarity.{self.rarity.name}, "
                f"slot='{self.slot}')")

class Weapon(Equipment):
    def __init__(self, name: str, description: str, rarity: Rarity, value: int, stat_bonuses: dict):
        super().__init__(name, description, rarity, value, slot="weapon", stat_bonuses=stat_bonuses)
        # stat_bonuses typically include 'attack_power', 'strength', etc.

class Armor(Equipment):
    def __init__(self, name: str, description: str, rarity: Rarity, value: int, slot: str, stat_bonuses: dict):
        super().__init__(name, description, rarity, value, slot=slot, stat_bonuses=stat_bonuses)
        # slot can be "helmet", "chest", "legs", "boots", "gloves"
        # stat_bonuses typically include 'defense', 'constitution', 'max_hp', etc.

if __name__ == '__main__':
    # Adjust sys.path for direct execution, if not already handled by the top-level code.
    # This specific block for __main__ ensures that game_core can be found if items.py is run directly.
    # The top-level sys.path modification should ideally handle this, but being explicit here
    # for the test environment can be safer.
    # (Re-evaluating, the top-level sys.path adjustment should be sufficient)

    print("--- Creating Items ---")
    rock = Item(name="Rock", description="A common rock. Not very useful.", rarity=Rarity.COMMON, value=0)
    health_potion = Item(name="Health Potion", description="Restores a small amount of HP.", rarity=Rarity.UNCOMMON, value=25)
    rare_sword = Item(name="Fine Steel Sword", description="A well-crafted sword.", rarity=Rarity.RARE, value=150)
    epic_amulet = Item(name="Amulet of Power", description="A potent magical amulet.", rarity=Rarity.EPIC, value=1000)

    print("\n--- Testing __str__ ---")
    print(rock)
    print(health_potion)
    print(rare_sword)
    print(epic_amulet)

    print("\n--- Testing __repr__ ---")
    print(repr(health_potion))
    print(repr(epic_amulet))

    print("\n--- Testing Rarity properties via Item ---")
    print(f"The {health_potion.name} has rarity color: {health_potion.rarity.color}")
    print(f"The {rare_sword.name} has drop rate: {rare_sword.rarity.drop_rate*100:.3f}%")

    print("\n\n--- Creating Equipment ---")
    rusty_sword = Equipment(
        name="Rusty Sword", 
        description="An old, rusty sword. Better than nothing.", 
        rarity=Rarity.COMMON, 
        value=5, 
        slot="Weapon", 
        stat_bonuses={'strength': 2} # Was {'attack_power': 3} -> 2 str = 3 attack
    )
    leather_vest = Equipment(
        name="Leather Vest",
        description="A simple vest made of tough leather.",
        rarity=Rarity.COMMON,
        value=10,
        slot="Chest",
        stat_bonuses={'vitality': 2, 'strength': 1} # Was {'defense': 5} -> 2 vit = 10HP, 0.5 def; 1 str = 0.5 def. Total +1 def
    )
    iron_helmet = Equipment(
        name="Iron Helmet",
        description="A sturdy iron helmet.",
        rarity=Rarity.UNCOMMON,
        value=30,
        slot="Head",
        stat_bonuses={'vitality': 1, 'strength': 1} # Was {'defense': 3, 'constitution': 1} -> 1 vit=5HP,0.25def; 1 str=0.5def. Total +0.75def
    )
    wizard_staff = Equipment(
        name="Apprentice Staff",
        description="A basic staff for aspiring mages.",
        rarity=Rarity.UNCOMMON,
        value=40,
        slot="Weapon",
        stat_bonuses={'intelligence': 3} # Was {'magic_power': 4, 'intelligence': 2} -> 3 int = 4.5 magic_attack
    )


    print("\n--- Testing Equipment __str__ ---")
    print(rusty_sword)
    print(leather_vest)
    print(iron_helmet)
    print(wizard_staff)

    print("\n--- Testing Equipment __repr__ ---")
    print(repr(rusty_sword))
    print(repr(iron_helmet))
    
    print("\n--- Testing Equipment Rarity Access ---")
    print(f"The {wizard_staff.name} ({wizard_staff.rarity.display_name}) has color code: {wizard_staff.rarity.color}")

    print("\n\n--- Creating Weapons ---")
    short_sword = Weapon(
        name="Short Sword", 
        description="A basic short sword.", 
        rarity=Rarity.COMMON, 
        value=10, 
        stat_bonuses={'strength': 2} # Was {'attack_power': 3}
    )
    battle_axe = Weapon(
        name="Battle Axe", 
        description="A sturdy battle axe.", 
        rarity=Rarity.RARE, 
        value=100, 
        stat_bonuses={'strength': 5} # Was {'attack_power': 10, 'strength': 2} -> 5 str = 7.5 attack
    )

    print("\n--- Testing Weapon Instances ---")
    print(short_sword)
    print(battle_axe)
    print(f"{short_sword.name} slot: {short_sword.slot}")
    print(f"{battle_axe.name} slot: {battle_axe.slot}")


    print("\n\n--- Creating Armor ---")
    leather_helmet = Armor(
        name="Leather Helmet", 
        description="A simple leather helmet.", 
        rarity=Rarity.COMMON, 
        value=8, 
        slot="helmet", 
        stat_bonuses={'vitality': 1} # Was {'defense': 2} -> 1 vit = 5HP, 0.25 def
    )
    iron_chestplate = Armor(
        name="Iron Chestplate", 
        description="A solid iron chestplate.", 
        rarity=Rarity.UNCOMMON, 
        value=50, 
        slot="chest", 
        stat_bonuses={'vitality': 2, 'strength': 2} # Was {'defense': 8, 'constitution': 1} -> 2vit=10HP,0.5def; 2str=1def. Total +1.5def
    )
    mage_robes = Armor(
        name="Mage Robes",
        description="Enchanted robes offering magical protection.",
        rarity=Rarity.RARE,
        value=120,
        slot="chest", # Example, could also be a full set
        stat_bonuses={'intelligence': 2, 'vitality': 1} # Was {'magic_power': 5, 'intelligence': 3, 'defense': 3} -> 2int=3MA,1MD; 1vit=5HP,0.25def
    )

    print("\n--- Testing Armor Instances ---")
    print(leather_helmet)
    print(iron_chestplate)
    print(mage_robes)
    print(f"{leather_helmet.name} slot: {leather_helmet.slot}")
    print(f"{iron_chestplate.name} slot: {iron_chestplate.slot}")
    print(f"{mage_robes.name} slot: {mage_robes.slot}")
