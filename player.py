import random
from items import Item, Equipment # Import Item and Equipment

class Player:
    """
    Represents a player character in the RPG.
    Handles stats, leveling, inventory, equipment, and character progression.
    """
    def __init__(self, name: str):
        """
        Initializes a new player character.

        Args:
            name (str): The name of the player character.
        """
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100  # XP needed for level 2

        # Base Primary Stats (without equipment modifiers)
        self._base_strength = 10
        self._base_dexterity = 10
        self._base_intelligence = 10
        self._base_constitution = 10
        self._base_luck = 10
        
        # Equipment & Inventory
        self.inventory = [] # List to store Item objects
        self.equipment = {
            "weapon": None, "shield": None, "head": None, 
            "chest": None, "legs": None, "feet": None, 
            "ring": None, "amulet": None
        } # Dict to store equipped Equipment objects

        # HP and MP are calculated based on stats
        # Current HP/MP should be initialized after max values are known
        self.current_hp = self.get_max_hp() 
        self.current_mp = self.get_max_mp()
        self.is_defending = False # For combat defense action

    def _get_equipment_bonus(self, stat_name: str) -> int:
        """Helper to sum stat bonuses from all equipped items for a given stat."""
        total_bonus = 0
        for slot, item in self.equipment.items():
            if item and isinstance(item, Equipment) and stat_name in item.stat_bonuses:
                total_bonus += item.stat_bonuses[stat_name]
        return total_bonus
    
    def _update_hp_mp_after_stat_change(self, old_max_hp: int, old_max_mp: int):
        """Adjusts current HP/MP proportionally after max HP/MP changes."""
        new_max_hp = self.get_max_hp()
        if new_max_hp != old_max_hp:
            hp_ratio = self.current_hp / old_max_hp if old_max_hp > 0 else 1.0
            self.current_hp = int(new_max_hp * hp_ratio)
            self.current_hp = max(0, min(self.current_hp, new_max_hp)) # Clamp HP

        new_max_mp = self.get_max_mp()
        if new_max_mp != old_max_mp:
            mp_ratio = self.current_mp / old_max_mp if old_max_mp > 0 else 1.0
            self.current_mp = int(new_max_mp * mp_ratio)
            self.current_mp = max(0, min(self.current_mp, new_max_mp)) # Clamp MP

    # --- Effective Stats (Base + Equipment) ---
    def get_strength(self) -> int:
        return self._base_strength + self._get_equipment_bonus('strength')

    def get_dexterity(self) -> int:
        return self._base_dexterity + self._get_equipment_bonus('dexterity')

    def get_intelligence(self) -> int:
        return self._base_intelligence + self._get_equipment_bonus('intelligence')

    def get_constitution(self) -> int:
        return self._base_constitution + self._get_equipment_bonus('constitution')

    def get_luck(self) -> int:
        return self._base_luck + self._get_equipment_bonus('luck')

    def get_max_hp(self) -> int:
        """Calculates maximum HP based on effective Constitution and bonuses."""
        base_hp_from_con = self.get_constitution() * 10
        level_bonus = self.level * 5
        equipment_max_hp_bonus = self._get_equipment_bonus('max_hp')
        return base_hp_from_con + level_bonus + equipment_max_hp_bonus

    def get_max_mp(self) -> int:
        """Calculates maximum MP based on effective Intelligence and bonuses."""
        base_mp_from_int = self.get_intelligence() * 10
        level_bonus = self.level * 3
        equipment_max_mp_bonus = self._get_equipment_bonus('max_mp')
        return base_mp_from_int + level_bonus + equipment_max_mp_bonus
    
    # --- Inventory Management ---
    def add_item_to_inventory(self, item: Item):
        """Adds an item to the player's inventory."""
        if not isinstance(item, Item):
            print(f"Error: {item} is not a valid Item.")
            return
        self.inventory.append(item)
        print(f"{item.name} added to inventory.")

    def remove_item_from_inventory(self, item: Item):
        """Removes an item from the player's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item.name} removed from inventory.")
            return True
        print(f"Error: {item.name} not found in inventory.")
        return False

    # --- Equipment Management ---
    def equip(self, item_to_equip: Equipment):
        """Equips an item from the inventory."""
        if not isinstance(item_to_equip, Equipment):
            print(f"Cannot equip {item_to_equip.name}: Not an equippable item.")
            return

        if item_to_equip not in self.inventory:
            print(f"Cannot equip {item_to_equip.name}: Not found in inventory.")
            return

        slot = item_to_equip.equip_slot
        if slot not in self.equipment:
            print(f"Cannot equip {item_to_equip.name}: Invalid slot '{slot}'.")
            return

        old_max_hp = self.get_max_hp()
        old_max_mp = self.get_max_mp()

        # Unequip current item in the slot, if any
        if self.equipment[slot] is not None:
            self.unequip(slot, move_to_inventory=True) # Force move to inventory, not just remove

        # Remove from inventory and equip
        self.remove_item_from_inventory(item_to_equip)
        self.equipment[slot] = item_to_equip
        print(f"{item_to_equip.name} equipped to {slot}.")
        
        self._update_hp_mp_after_stat_change(old_max_hp, old_max_mp)


    def unequip(self, slot_to_unequip: str, move_to_inventory: bool = True):
        """Unequips an item from a given slot."""
        if slot_to_unequip not in self.equipment:
            print(f"Cannot unequip: Invalid slot '{slot_to_unequip}'.")
            return

        item = self.equipment[slot_to_unequip]
        if item is None:
            print(f"Nothing equipped in {slot_to_unequip}.")
            return

        old_max_hp = self.get_max_hp()
        old_max_mp = self.get_max_mp()

        self.equipment[slot_to_unequip] = None
        print(f"{item.name} unequipped from {slot_to_unequip}.")

        if move_to_inventory:
            self.add_item_to_inventory(item) # Add it back to inventory
        
        self._update_hp_mp_after_stat_change(old_max_hp, old_max_mp)


    # --- Leveling and XP ---
    def gain_xp(self, amount: int):
        """Grants XP to the player and handles level ups."""
        if self.level >= 50: # Max level cap
            self.xp = 0 
            return

        self.xp += amount
        print(f"{self.name} gained {amount} XP.")
        while self.xp >= self.xp_to_next_level and self.level < 50:
            self.level_up()

    def level_up(self):
        """Handles the player leveling up."""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(100 * (self.level ** 1.8)) 

        str_gain = random.randint(1, 3)
        dex_gain = random.randint(1, 3)
        int_gain = random.randint(1, 3)
        con_gain = random.randint(1, 3)
        luc_gain = random.randint(0, 2) 
        con_gain = max(1, con_gain) 

        # Store old max HP/MP to calculate percentage for current HP/MP restoration
        old_max_hp = self.get_max_hp()
        old_max_mp = self.get_max_mp()

        self._base_strength += str_gain
        self._base_dexterity += dex_gain
        self._base_intelligence += int_gain
        self._base_constitution += con_gain
        self._base_luck += luc_gain
        
        # HP/MP are fully restored and increased to new max on level up
        self.current_hp = self.get_max_hp()
        self.current_mp = self.get_max_mp()

        print(f"\n{self.name} leveled up to level {self.level}!")
        # Displaying base stats and gains
        print(f"Base STR: {self._base_strength - str_gain} -> {self._base_strength} (+{str_gain})")
        print(f"Base DEX: {self._base_dexterity - dex_gain} -> {self._base_dexterity} (+{dex_gain})")
        print(f"Base INT: {self._base_intelligence - int_gain} -> {self._base_intelligence} (+{int_gain})")
        print(f"Base CON: {self._base_constitution - con_gain} -> {self._base_constitution} (+{con_gain})")
        print(f"Base LUK: {self._base_luck - luc_gain} -> {self._base_luck} (+{luc_gain})")
        print(f"Max HP now: {self.get_max_hp()}")
        print(f"Max MP now: {self.get_max_mp()}")

    # --- Getters for basic attributes ---
    def get_name(self) -> str:
        return self.name

    def get_level(self) -> int:
        return self.level

    def get_xp(self) -> int:
        return self.xp

    def get_xp_to_next_level(self) -> int:
        return self.xp_to_next_level

    def get_current_hp(self) -> int:
        return self.current_hp

    def get_current_mp(self) -> int:
        return self.current_mp

    # --- Getters for BASE primary stats (mostly for internal use or display) ---
    def get_base_strength(self) -> int:
        return self._base_strength

    def get_base_dexterity(self) -> int:
        return self._base_dexterity

    def get_base_intelligence(self) -> int:
        return self._base_intelligence

    def get_base_constitution(self) -> int:
        return self._base_constitution

    def get_base_luck(self) -> int:
        return self._base_luck

    # --- Methods for derived stats (using effective primary stats) ---
    def get_attack_power(self) -> int:
        """Calculates attack power, based on effective Strength and equipment bonuses."""
        ap_from_strength = self.get_strength() * 2 
        ap_bonus_from_equipment = self._get_equipment_bonus('attack_power')
        return ap_from_strength + ap_bonus_from_equipment

    def get_defense(self) -> int:
        """Calculates defense, based on effective Constitution/Dexterity and equipment bonuses."""
        defense_from_stats = self.get_constitution() + self.get_dexterity() // 2
        defense_bonus_from_equipment = self._get_equipment_bonus('defense')
        base_total_defense = defense_from_stats + defense_bonus_from_equipment
        return base_total_defense * 2 if self.is_defending else base_total_defense

    def get_magic_power(self) -> int:
        """Calculates magic power, primarily based on effective Intelligence and equipment bonuses."""
        mp_from_intelligence = self.get_intelligence() * 2
        mp_bonus_from_equipment = self._get_equipment_bonus('magic_power')
        return mp_from_intelligence + mp_bonus_from_equipment

    def get_critical_hit_chance(self) -> float:
        """Calculates critical hit chance in percent using effective Luck."""
        return max(0.0, self.get_luck() / 2.0) 

    def get_accuracy(self) -> float:
        """Calculates accuracy, influencing hit chance, using effective Dexterity."""
        base_accuracy = 75.0
        accuracy = base_accuracy + (self.get_dexterity() - 10) * 1.5
        return max(5.0, min(accuracy, 100.0)) 

    def get_evasion(self) -> float:
        """Calculates evasion, influencing dodge chance, using effective Dexterity and Luck."""
        base_evasion = 5.0
        evasion = base_evasion + (self.get_dexterity() - 10) * 1.0 + (self.get_luck() - 10) * 0.5
        return max(0.0, min(evasion, 75.0)) 

    # --- Methods for combat ---
    def take_damage(self, damage: int):
        """Reduces player's HP by the damage amount. Considers defense stance."""
        actual_damage = damage
        if self.is_defending:
            print(f"{self.name} is defending and takes reduced damage!")
            actual_damage = damage // 2 
            self.is_defending = False 
        
        actual_damage = max(1, actual_damage) 

        self.current_hp -= actual_damage
        if self.current_hp < 0:
            self.current_hp = 0
        print(f"{self.name} takes {actual_damage} damage. HP: {self.current_hp}/{self.get_max_hp()}")
        if self.current_hp == 0:
            print(f"{self.name} has been defeated!")

    def start_defending(self):
        print(f"{self.name} is defending!")
        self.is_defending = True

    def reset_defense(self):
        if self.is_defending:
            # print(f"{self.name} stops defending.") # Can be noisy
            self.is_defending = False

    def use_mp(self, cost: int) -> bool:
        if self.current_mp >= cost:
            self.current_mp -= cost
            print(f"{self.name} uses {cost} MP. MP: {self.current_mp}/{self.get_max_mp()}")
            return True
        else:
            print(f"{self.name} does not have enough MP!")
            return False

    def is_alive(self) -> bool:
        """Checks if the player is still alive."""
        return self.current_hp > 0

    def display_stats(self):
        """Displays a summary of the player's current stats and equipment."""
        print(f"\n--- {self.get_name()} - Level {self.get_level()} ---")
        print(f"HP: {self.get_current_hp()}/{self.get_max_hp()} | MP: {self.get_current_mp()}/{self.get_max_mp()}")
        print(f"XP: {self.get_xp()}/{self.get_xp_to_next_level()}")
        print("--- Attributes ---")
        print(f"  STR: {self.get_strength()} (Base: {self.get_base_strength()})")
        print(f"  DEX: {self.get_dexterity()} (Base: {self.get_base_dexterity()})")
        print(f"  INT: {self.get_intelligence()} (Base: {self.get_base_intelligence()})")
        print(f"  CON: {self.get_constitution()} (Base: {self.get_base_constitution()})")
        print(f"  LUK: {self.get_luck()} (Base: {self.get_base_luck()})")
        print("--- Combat Stats ---")
        print(f"  Attack Power: {self.get_attack_power()}")
        
        # Calculate base defense value (stats + equipment direct bonus)
        base_defense_val = (self.get_constitution() + self.get_dexterity() // 2) + \
                           self._get_equipment_bonus('defense')
        # get_defense() returns defense possibly doubled if self.is_defending is true
        current_total_defense = self.get_defense() 
        
        if self.is_defending:
            # If defending, current_total_defense is already doubled.
            # The base_defense_val here is the non-doubled value.
            print(f"  Defense: {current_total_defense} (Base: {base_defense_val}, Defending!)")
        else:
            print(f"  Defense: {current_total_defense} (Base: {base_defense_val})")
            
        print(f"  Magic Power: {self.get_magic_power()}")
        print(f"  Crit Chance: {self.get_critical_hit_chance()}%")
        print(f"  Accuracy: {self.get_accuracy()}%")
        print(f"  Evasion: {self.get_evasion()}%")
        print("--- Equipment ---")
        for slot, item in self.equipment.items():
            if item:
                print(f"  {slot.capitalize()}: {item.name} ({item.rarity.value})")
            else:
                print(f"  {slot.capitalize()}: None")
        print("--------------------")
