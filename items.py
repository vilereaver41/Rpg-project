from enum import Enum

class ItemRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

class Item:
    """
    Base class for all items in the game.
    """
    def __init__(self, name: str, description: str, rarity: ItemRarity):
        self.name = name
        self.description = description
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} ({self.rarity.value})"

class Equipment(Item):
    """
    Represents an item that can be equipped by the player.
    """
    VALID_EQUIP_SLOTS = ["weapon", "shield", "head", "chest", "legs", "feet", "ring", "amulet"]

    def __init__(self, name: str, description: str, rarity: ItemRarity, 
                 equip_slot: str, stat_bonuses: dict):
        super().__init__(name, description, rarity)
        
        if equip_slot not in self.VALID_EQUIP_SLOTS:
            raise ValueError(f"Invalid equip_slot: {equip_slot}. Must be one of {self.VALID_EQUIP_SLOTS}")
        self.equip_slot = equip_slot
        self.stat_bonuses = stat_bonuses # e.g., {'strength': 5, 'max_hp': 10}

    def __str__(self):
        return f"{self.name} ({self.rarity.value}) - Slot: {self.equip_slot}, Bonuses: {self.stat_bonuses}"

class Weapon(Equipment):
    """
    Represents a weapon that can be equipped.
    Bonuses are typically to 'attack_power' or primary stats like 'strength'.
    """
    def __init__(self, name: str, description: str, rarity: ItemRarity, 
                 attack_bonus: int = 0, strength_bonus: int = 0, dexterity_bonus: int = 0):
        stat_bonuses = {}
        if attack_bonus > 0:
            stat_bonuses['attack_power'] = attack_bonus # Direct bonus to attack_power
        if strength_bonus > 0:
            stat_bonuses['strength'] = strength_bonus
        if dexterity_bonus > 0:
            stat_bonuses['dexterity'] = dexterity_bonus
            
        super().__init__(name, description, rarity, "weapon", stat_bonuses)

class Armor(Equipment):
    """
    Represents a piece of armor that can be equipped.
    Bonuses are typically to 'defense' or primary stats like 'constitution', 'max_hp'.
    """
    def __init__(self, name: str, description: str, rarity: ItemRarity, equip_slot: str,
                 defense_bonus: int = 0, constitution_bonus: int = 0, max_hp_bonus: int = 0):
        
        if equip_slot not in ["head", "chest", "legs", "feet", "shield"]:
             raise ValueError(f"Invalid equip_slot for Armor: {equip_slot}. Must be armor slot.")

        stat_bonuses = {}
        if defense_bonus > 0:
            stat_bonuses['defense'] = defense_bonus # Direct bonus to defense
        if constitution_bonus > 0:
            stat_bonuses['constitution'] = constitution_bonus
        if max_hp_bonus > 0:
            stat_bonuses['max_hp'] = max_hp_bonus

        super().__init__(name, description, rarity, equip_slot, stat_bonuses)
