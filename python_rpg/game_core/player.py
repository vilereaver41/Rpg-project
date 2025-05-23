import sys
import os

# Ensure the package root (python_rpg) is in sys.path for absolute imports
_PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, _PACKAGE_ROOT)

from game_core.monster import Monster
from game_core.items import Item, Equipment, Weapon, Armor
from game_core.rarity import Rarity # For test block items

class Player:
    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.max_hp = 0 
        self.current_hp = 0 
        self.max_mp = 20 
        self.current_mp = 20
        
        self.inventory: list[Item] = []
        self.equipment: dict[str, Equipment | None] = {} 

        # Base Primary Stats
        self.base_strength = 5
        self.base_dexterity = 5
        self.base_agility = 5
        self.base_intelligence = 5
        self.base_vitality = 5
        self.base_luck = 5

        # Derived Stats - initialized to zero, will be set by _update_derived_stats
        self.attack = 0.0
        self.defense = 0.0
        self.magic_attack = 0.0
        self.magic_defense = 0.0
        self.crit_chance = 0.0
        self.dodge = 0.0
        self.discovery = 0.0
        
        self._initialize_equipment_slots() 
        self._update_derived_stats() 
        self.current_hp = self.max_hp 

    def _initialize_equipment_slots(self):
        slots = ["weapon", "helmet", "chest", "legs", "boots", "gloves", "shield", "amulet", "ring1", "ring2"]
        for slot in slots:
            self.equipment[slot] = None

    def _update_derived_stats(self):
        # Calculate Total Primary Stats from base + primary equipment bonuses
        total_strength = self.base_strength
        total_dexterity = self.base_dexterity
        total_agility = self.base_agility
        total_intelligence = self.base_intelligence
        total_vitality = self.base_vitality
        total_luck = self.base_luck

        for item in self.equipment.values():
            if item and hasattr(item, 'stat_bonuses') and isinstance(item.stat_bonuses, dict):
                # Primary stat bonuses
                if 'strength' in item.stat_bonuses: total_strength += item.stat_bonuses['strength']
                if 'dexterity' in item.stat_bonuses: total_dexterity += item.stat_bonuses['dexterity']
                if 'agility' in item.stat_bonuses: total_agility += item.stat_bonuses['agility']
                if 'intelligence' in item.stat_bonuses: total_intelligence += item.stat_bonuses['intelligence']
                if 'vitality' in item.stat_bonuses: total_vitality += item.stat_bonuses['vitality']
                if 'luck' in item.stat_bonuses: total_luck += item.stat_bonuses['luck']
        
        # Calculate derived stats from Total Primary Stats
        base_hp_from_level = 20 
        self.max_hp = base_hp_from_level + total_vitality * 5
        
        self.attack = total_strength * 1.5
        self.defense = total_strength * 0.5 + total_vitality * 0.25
        self.magic_attack = total_intelligence * 1.5
        self.magic_defense = total_intelligence * 1.0
        self.crit_chance = total_dexterity * 0.005 + total_agility * 0.001 + total_luck * 0.002
        self.dodge = total_dexterity * 0.002 + total_agility * 0.006 + total_luck * 0.002
        self.discovery = total_luck * 0.003

        # Apply direct bonuses from equipment to derived stats
        for item in self.equipment.values():
            if item and hasattr(item, 'stat_bonuses') and isinstance(item.stat_bonuses, dict):
                # Direct bonuses to derived stats
                if 'attack' in item.stat_bonuses: self.attack += item.stat_bonuses['attack']
                if 'defense' in item.stat_bonuses: self.defense += item.stat_bonuses['defense']
                if 'magic_attack' in item.stat_bonuses: self.magic_attack += item.stat_bonuses['magic_attack']
                if 'magic_defense' in item.stat_bonuses: self.magic_defense += item.stat_bonuses['magic_defense']
                if 'crit_chance' in item.stat_bonuses: self.crit_chance += item.stat_bonuses['crit_chance']
                if 'dodge' in item.stat_bonuses: self.dodge += item.stat_bonuses['dodge']
                if 'discovery' in item.stat_bonuses: self.discovery += item.stat_bonuses['discovery']
                if 'max_hp' in item.stat_bonuses: self.max_hp += item.stat_bonuses['max_hp']
        
        self.current_hp = min(self.current_hp, self.max_hp)

    def add_item_to_inventory(self, item: Item):
        self.inventory.append(item)
        print(f"'{item.name}' added to inventory.")

    def find_item_in_inventory(self, item_name: str) -> Item | None:
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def equip_item(self, item_name: str):
        item_to_equip = self.find_item_in_inventory(item_name)
        if not item_to_equip:
            print(f"Item '{item_name}' not found in inventory.")
            return
        if not isinstance(item_to_equip, Equipment):
            print(f"'{item_to_equip.name}' is not an equippable item.")
            return
        target_slot = item_to_equip.slot
        if target_slot not in self.equipment:
            print(f"Cannot equip to unknown slot: '{target_slot}'.")
            return
        if self.equipment[target_slot] is not None:
            self.unequip_item(target_slot)
        self.equipment[target_slot] = item_to_equip
        if item_to_equip in self.inventory:
            self.inventory.remove(item_to_equip)
        print(f"'{item_to_equip.name}' equipped to {target_slot} slot.")
        self._update_derived_stats() # Automatically update stats

    def unequip_item(self, slot_to_unequip: str):
        if slot_to_unequip not in self.equipment or self.equipment[slot_to_unequip] is None:
            print(f"Nothing equipped in the '{slot_to_unequip}' slot.")
            return
        item_to_unequip = self.equipment[slot_to_unequip]
        self.equipment[slot_to_unequip] = None
        self.inventory.append(item_to_unequip)
        print(f"'{item_to_unequip.name}' unequipped from {slot_to_unequip} slot.")
        self._update_derived_stats() # Automatically update stats

    def attack_target(self, target: Monster) -> bool:
        print(f"\n{self.name} attacks {target.name}!")
        damage = self.attack - target.defense 
        damage = max(1, float(damage)) # Ensure damage is float for consistency if attack/defense are float
        defeated = target.take_damage(int(round(damage))) # Monster take_damage expects int
        return defeated

    def take_damage(self, damage_amount: int) -> bool:
        actual_damage = max(0, damage_amount) 
        self.current_hp -= actual_damage
        print(f"{self.name} takes {actual_damage} damage.")
        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.name} has been defeated.")
            return True
        return False

    def add_xp(self, amount: int):
        if amount <= 0: return
        self.xp += amount
        print(f"{self.name} gains {amount} XP.")
        while self.xp >= self.xp_to_next_level:
            excess_xp = self.xp - self.xp_to_next_level
            self.level_up() 
            self.xp = excess_xp 

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def level_up(self):
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.xp = 0 

        self.base_strength += 1
        self.base_dexterity += 1
        self.base_agility += 1
        self.base_intelligence += 1
        self.base_vitality += 1
        self.base_luck += 1

        old_max_hp = self.max_hp
        self._update_derived_stats() 
        
        self.current_hp = self.max_hp 
        self.current_mp = self.max_mp 

        print(f"\nCongratulations, {self.name}! You've reached Level {self.level}!")
        print("Your base stats have increased:")
        print(f"  Strength: {self.base_strength}")
        print(f"  Dexterity: {self.base_dexterity}")
        print(f"  Agility: {self.base_agility}")
        print(f"  Intelligence: {self.base_intelligence}")
        print(f"  Vitality: {self.base_vitality}")
        print(f"  Luck: {self.base_luck}")
        print(f"Max HP increased from {old_max_hp} to {self.max_hp}.")
        print(f"HP and MP fully restored.")
        print(f"XP to next level: {self.xp_to_next_level}")

    def __str__(self):
        s = (
            f"--- {self.name} ---\n"
            f"Level: {self.level}\n"
            f"XP: {self.xp}/{self.xp_to_next_level}\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"MP: {self.current_mp}/{self.max_mp}\n"
            f"--- Stats ---\n"
            f"Strength: {self.base_strength}\n"
            f"Dexterity: {self.base_dexterity}\n"
            f"Agility: {self.base_agility}\n"
            f"Intelligence: {self.base_intelligence}\n"
            f"Vitality: {self.base_vitality}\n"
            f"Luck: {self.base_luck}\n"
            f"--- Derived Stats (calculated from base + equipment + direct bonuses) ---\n" # Updated header
            f"Attack: {self.attack:.2f}\n"
            f"Defense: {self.defense:.2f}\n"
            f"Magic Attack: {self.magic_attack:.2f}\n"
            f"Magic Defense: {self.magic_defense:.2f}\n"
            f"Crit Chance: {self.crit_chance*100:.2f}%\n"
            f"Dodge: {self.dodge*100:.2f}%\n"
            f"Discovery: {self.discovery*100:.2f}%\n"
            f"-------------\n"
            f"Inventory:\n"
        )
        if not self.inventory:
            s += "  Empty\n"
        else:
            for item_in_inv in self.inventory:
                s += f"  {item_in_inv}\n"
        s += "Equipped:\n"
        equipped_count = 0
        for slot, item_in_slot in self.equipment.items():
            if item_in_slot:
                s += f"  {slot.capitalize()}: {item_in_slot.name} ({item_in_slot.rarity.display_name})\n"
                equipped_count += 1
        if equipped_count == 0:
             s += "  Nothing equipped\n"
        s += "-------------"
        return s

if __name__ == '__main__':
    player1 = Player("HeroDirectBonusTest") 

    print("--- Initial Player State (Base Stats Only) ---")
    # Base: str=5, dex=5, agi=5, int=5, vit=5, luck=5
    # Derived from base:
    # max_hp = 20 + 5*5 = 45
    # attack = 5 * 1.5 = 7.5
    # defense = 5*0.5 + 5*0.25 = 3.75
    # magic_attack = 5*1.5 = 7.5
    # magic_defense = 5*1.0 = 5.0
    # crit_chance = 5*0.005 + 5*0.001 + 5*0.002 = 0.040 (4.0%)
    # dodge = 5*0.002 + 5*0.006 + 5*0.002 = 0.050 (5.0%)
    # discovery = 5*0.003 = 0.015 (1.5%)
    print(player1)

    print("\n--- Equipping Items with Primary and Direct Derived Bonuses ---")
    # Sword: +2 strength (primary), +5 attack (direct derived)
    mighty_sword = Weapon(name="Mighty Sword", description="Boosts strength and attack.", 
                           rarity=Rarity.RARE, value=150, 
                           stat_bonuses={'strength': 2, 'attack': 5}) # Direct 'attack' bonus
    
    # Shield: +2 vitality (primary), +10 defense (direct derived), +20 max_hp (direct derived)
    sturdy_shield = Armor(name="Sturdy Shield", description="Boosts vitality and defense.", 
                            rarity=Rarity.RARE, value=120, slot="shield", 
                            stat_bonuses={'vitality': 2, 'defense': 10, 'max_hp': 20}) # Direct 'defense' and 'max_hp'

    player1.add_item_to_inventory(mighty_sword)
    player1.add_item_to_inventory(sturdy_shield)

    player1.equip_item("Mighty Sword") # Should now auto-update stats
    player1.equip_item("Sturdy Shield") # Should now auto-update stats
    
    # player1._update_derived_stats() # No longer needed manually
    
    print("\n--- Player State After Equipping (Stats Automatically Updated) ---")
    # Base stats: str=5, dex=5, agi=5, int=5, vit=5, luck=5
    # Equipment primary bonuses: strength+2, vitality+2
    # Total primary stats for calculation:
    #   total_strength = 5 + 2 = 7
    #   total_vitality = 5 + 2 = 7
    # Derived stats before direct bonuses:
    #   max_hp_from_primary = 20 + 7*5 = 55
    #   attack_from_primary = 7 * 1.5 = 10.5
    #   defense_from_primary = 7*0.5 + 7*0.25 = 3.5 + 1.75 = 5.25
    # Direct derived bonuses from equipment:
    #   Mighty Sword: 'attack': +5
    #   Sturdy Shield: 'defense': +10, 'max_hp': +20
    # Final Expected Derived Stats:
    #   max_hp = 55 (from primary) + 20 (direct shield) = 75
    #   attack = 10.5 (from primary) + 5 (direct sword) = 15.5
    #   defense = 5.25 (from primary) + 10 (direct shield) = 15.25
    print(player1)

    print("\n--- Testing Level Up (With Mixed Bonus Equipment) ---")
    player1.add_xp(100) # Level up to L2
    # Base stats become: str=6, dex=6, agi=6, int=6, vit=6, luck=6
    # Equipment primary bonuses: strength+2, vitality+2
    # Total primary for L2: str=8, dex=6, agi=6, int=6, vit=8, luck=6
    # Derived from L2 total primary:
    #   max_hp_from_primary = 20 + 8*5 = 60
    #   attack_from_primary = 8 * 1.5 = 12.0
    #   defense_from_primary = 8*0.5 + 8*0.25 = 4.0 + 2.0 = 6.0
    # Direct derived bonuses remain: attack+5, defense+10, max_hp+20
    # Final L2 Expected:
    #   max_hp = 60 + 20 = 80
    #   attack = 12.0 + 5 = 17.0
    #   defense = 6.0 + 10 = 16.0
    print(player1)

    print("\n--- Unequipping an Item (Stats Automatically Updated) ---")
    player1.unequip_item("weapon") # Unequip Mighty Sword, should auto-update stats
    # player1._update_derived_stats() # No longer needed manually
    print("\n--- Player State After Unequipping Sword ---")
    # Base stats (L2): str=6, dex=6, agi=6, int=6, vit=6, luck=6
    # Equipment (Shield only): primary vit+2; direct defense+10, max_hp+20
    # Total primary: str=6, dex=6, agi=6, int=6, vit=8, luck=6
    # Derived from total primary:
    #   max_hp_from_primary = 20 + 8*5 = 60
    #   attack_from_primary = 6 * 1.5 = 9.0
    #   defense_from_primary = 6*0.5 + 8*0.25 = 3.0 + 2.0 = 5.0
    # Direct derived bonuses from Shield: defense+10, max_hp+20
    # Final Expected:
    #   max_hp = 60 + 20 = 80
    #   attack = 9.0 (no direct bonus)
    #   defense = 5.0 + 10 = 15.0
    print(player1)
