import csv
from typing import Dict, Union

# Adjust import path based on project structure
try:
    from rpg_game.core.equipment import Equipment
    from rpg_game.core.consumable import Consumable
    from rpg_game.core.material import Material
    from rpg_game.core.item import Item # For type hinting
    from rpg_game.core.weapon import Weapon
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.equipment import Equipment
    from core.consumable import Consumable
    from core.material import Material
    from core.item import Item # For type hinting
    from core.weapon import Weapon


def _to_int(value: str, default: int = 0) -> int:
    """Converts a string to an integer, returning a default if empty or invalid."""
    if not value:
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default

def load_equipment_from_csv(file_path: str) -> Dict[str, 'Equipment']:
    """
    Loads equipment data from a CSV file and returns a dictionary of Equipment objects.
    """
    equipment_dict: Dict[str, Equipment] = {}
    
    # Known section headers or titles to skip. Case-insensitive matching might be good.
    section_titles = {"shields", "cloaks", "accesories", "armor sets", "leather set", "iron set", "steel set", 
                      "mythril set", "adamantite set", "dragon scale set", "crystal set", "bone set",
                      "elemental robes", "special armor"} # Add more as identified

    # Expected main header for reference, though we primarily skip by position
    # "Armor,(empty),Tier,Recipe,Equip Type,Attack,Defense,M.Attack,M.Defense,Agility,Luck,Max Hp,Max Mp,Extra Increases,Additional Changes, (empty or Source)"
    
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        try:
            _ = next(reader) # Skip the main header row
        except StopIteration:
            # Empty file
            return equipment_dict

        for row_number, row in enumerate(reader, start=2): # Start from 2 as 1 was header
            if not row or not any(row): # Skip completely empty rows
                continue

            name = row[0].strip()

            # Skip row if name is empty or it looks like a section header/separator
            if not name:
                continue
            
            # Check if it's a known section title (e.g., "Shields", "Cloaks")
            # Also check for common patterns of section headers (e.g., "Leather set,,,,,,,")
            # A row is a section header if name is in section_titles or (col2 is empty and col3 is empty and col4 is empty)
            # Tier is in column index 2 (row[2])
            is_section_header = False
            if name.lower() in section_titles:
                is_section_header = True
            elif len(row) > 4 and not row[1].strip() and not row[2].strip() and not row[3].strip() and not row[4].strip():
                # This pattern often indicates a set name like "Leather set,,,,,,,,"
                is_section_header = True
            
            if is_section_header:
                # print(f"Skipping section header: {name}")
                continue

            # Ensure row has enough columns, otherwise it might be a malformed entry or separator
            if len(row) < 16: # Expecting up to at least column index 15 for Source
                # print(f"Skipping row {row_number} due to insufficient columns: {row}")
                continue

            try:
                tier = row[2].strip()
                recipe = row[3].strip()
                equip_type = row[4].strip()

                attack_bonus = _to_int(row[5])
                defense_bonus = _to_int(row[6])
                magic_attack_bonus = _to_int(row[7])
                magic_defense_bonus = _to_int(row[8])
                agility_bonus = _to_int(row[9])
                luck_bonus = _to_int(row[10])
                max_hp_bonus = _to_int(row[11])
                max_mp_bonus = _to_int(row[12])
                
                extra_increases = row[13].strip()
                # Column 14 is "Additional Changes" - not directly used in Equipment constructor per previous subtask
                # Column 15 is "Source"
                source = row[15].strip()

                description = f"A piece of {tier} {equip_type}." if tier and equip_type else "A piece of equipment."

                equipment_obj = Equipment(
                    name=name,
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
                    source=source
                )
                equipment_dict[name] = equipment_obj
            
            except IndexError:
                # This can happen if a row is shorter than expected, even after the initial length check
                # print(f"Warning: Skipping row {row_number} for item '{name}' due to IndexError (likely missing columns). Row data: {row}")
                continue
            except Exception as e:
                # print(f"Warning: An unexpected error occurred while processing row {row_number} for item '{name}': {e}. Row data: {row}")
                continue
                
    return equipment_dict


def load_consumables_and_materials_from_csv(file_path: str) -> Dict[str, 'Item']:
    """
    Loads consumables and materials data from a CSV file.
    The CSV is section-based: "Potions", "Special Consumable", "Food", "Raw Ingriedient".
    """
    items: Dict[str, Item] = {}
    current_section: Union[str, None] = None
    
    # Define section names (case-sensitive as per current implementation plan)
    section_map = {
        "Potions": "Potion",
        "Special Consumable": "Special Consumable",
        "Food": "Food",
        "Raw Ingriedient": "Material" # "Raw Ingriedient" in CSV maps to Material type
    }
    section_titles = list(section_map.keys())

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row_number, row in enumerate(reader, start=1):
            if not row or not any(row): # Skip empty rows
                continue

            first_cell_value = row[0].strip()

            # Check if this row defines a new section
            if first_cell_value in section_titles:
                current_section = section_map[first_cell_value]
                # print(f"Switched to section: {current_section} (from '{first_cell_value}')")
                continue

            if not current_section:
                # print(f"Skipping row {row_number} as no section is currently active: {row}")
                continue
            
            # Skip rows where the name is empty or matches the section title (often sub-headers)
            if not first_cell_value or \
               (first_cell_value == "Potions" and current_section == "Potion") or \
               (first_cell_value == "Special Consumable" and current_section == "Special Consumable") or \
               (first_cell_value == "Food" and current_section == "Food") or \
               (first_cell_value == "Raw Ingriedient" and current_section == "Material"):
                continue

            name = first_cell_value
            item_obj: Union[Consumable, Material, None] = None

            try:
                if current_section == "Potion":
                    # Potions: name (col 0), (empty col 1), effect_notes (col 2)
                    if len(row) < 3: continue # Ensure enough columns
                    effect_notes = row[2].strip()
                    item_obj = Consumable(
                        name=name,
                        description=effect_notes if effect_notes else f"A standard {name}.", # Default desc if notes empty
                        category="Potion",
                        effect_description=effect_notes,
                        rarity="Common" # Default rarity for potions as per spec
                    )
                elif current_section == "Special Consumable":
                    # Special Consumable: name (col 0), rarity (col 1), (empty col 2), effect_notes (col 3)
                    if len(row) < 4: continue
                    rarity = row[1].strip() if row[1].strip() else "Common" # Default if rarity empty
                    effect_notes = row[3].strip()
                    item_obj = Consumable(
                        name=name,
                        description=effect_notes if effect_notes else f"A special consumable: {name}.",
                        category="Special Consumable",
                        effect_description=effect_notes,
                        rarity=rarity
                    )
                elif current_section == "Food":
                    # Food: name (col 0), rarity (col 1), effect (col 2), recipe (col 3)
                    if len(row) < 4: continue
                    rarity = row[1].strip() if row[1].strip() else "Common"
                    effect = row[2].strip()
                    recipe = row[3].strip() # Can be empty
                    item_obj = Consumable(
                        name=name,
                        description=effect if effect else f"A type of food: {name}.",
                        category="Food",
                        effect_description=effect,
                        rarity=rarity,
                        recipe=recipe
                    )
                elif current_section == "Material":
                    # Raw Ingriedient (Material): name (col 0), rarity (col 1)
                    if len(row) < 2: continue
                    rarity = row[1].strip() if row[1].strip() else "Common"
                    item_obj = Material(
                        name=name,
                        description=f"{rarity} crafting material: {name}.", # Generic description
                        rarity=rarity
                    )
                
                if item_obj:
                    items[name] = item_obj

            except IndexError:
                # print(f"Warning: Skipping row {row_number} for item '{name}' in section '{current_section}' due to IndexError. Row data: {row}")
                continue
            except Exception as e:
                # print(f"Warning: An unexpected error occurred while processing row {row_number} for item '{name}' in section '{current_section}': {e}. Row data: {row}")
                continue
                
    return items


if __name__ == '__main__':
    # --- Load Equipment ---
    equipment_csv_path = "Game Csv Data/Armor, Accesories, Shields.csv"
    
    if not os.path.exists(equipment_csv_path):
        print(f"Test CSV file for equipment not found at {equipment_csv_path}. Creating a dummy file for basic testing.")
        dummy_dir = os.path.dirname(equipment_csv_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        with open(equipment_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Armor","","Tier","Recipe","Equip Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max Hp","Max Mp","Extra Increases","Additional Changes","Source"])
            writer.writerow(["Leather Cap","","Common","2 Leather","Helmet","","2","","","1","","","","","","Crafted"])
    
    print(f"Attempting to load equipment from: {os.path.abspath(equipment_csv_path)}")
    try:
        loaded_equipment = load_equipment_from_csv(equipment_csv_path)
        print(f"\nTotal equipment pieces loaded: {len(loaded_equipment)}")
        if "Leather Cap" in loaded_equipment:
            print(f"  Example Equipment: {loaded_equipment['Leather Cap']}")
    except FileNotFoundError:
        print(f"Error: Equipment CSV file was not found at '{equipment_csv_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during equipment loading: {e}")
    print("\nEquipment loading test finished.")

    # --- Load Consumables and Materials ---
    consumables_csv_path = "Game Csv Data/Potions, Consumables, Materials.csv"

    if not os.path.exists(consumables_csv_path):
        print(f"Test CSV file for consumables/materials not found at {consumables_csv_path}. Creating a dummy file for basic testing.")
        dummy_dir = os.path.dirname(consumables_csv_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        with open(consumables_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Potions,,Effect Notes,,
            writer.writerow(["Potions", "", "Effect Notes", "", ""])
            writer.writerow(["Crude Health Potion", "", "Restores 25 HP", "", ""])
            writer.writerow(["Minor Mana Potion", "", "Restores 10 MP", "", ""])
            # Special Consumable,Rarity,,Effect Notes,
            writer.writerow(["Special Consumable", "Rarity", "", "Effect Notes", ""])
            writer.writerow(["Crystal Glow Berry", "Uncommon", "", "Grants Night Vision for 5 minutes", ""])
            writer.writerow(["Elixir of Speed", "Rare", "", "Increases Agility by +10 for 1 minute", ""])
            # Food,Rarity,Effect,Recipe
            writer.writerow(["Food", "Rarity", "Effect", "Recipe", ""])
            writer.writerow(["Dried Meat", "Common", "Restores 5 HP over 10 seconds", "1x Raw Meat, 1x Salt", ""])
            writer.writerow(["Traveler's Stew", "Uncommon", "Restores 20 HP & 5 MP, grants 'Well Fed'", "2x Carrot, 1x Potato, 1x Mystery Meat", ""])
            # Raw Ingriedient,Rarity,,,
            writer.writerow(["Raw Ingriedient", "Rarity", "", "", ""]) # Note: CSV has "Ingriedient"
            writer.writerow(["Chomper Filet", "Common", "", "", ""])
            writer.writerow(["Iron Ore", "Common", "", "", ""])
            writer.writerow(["Spirit Bloom Petal", "Uncommon", "", "", ""])

    print(f"\nAttempting to load consumables and materials from: {os.path.abspath(consumables_csv_path)}")
    try:
        loaded_items = load_consumables_and_materials_from_csv(consumables_csv_path)
        print(f"\nTotal consumables and materials loaded: {len(loaded_items)}")

        sample_items_to_check = {
            "Crude Health Potion": Consumable,
            "Crystal Glow Berry": Consumable,
            "Dried Meat": Consumable,
            "Chomper Filet": Material
        }
        for item_name, item_type in sample_items_to_check.items():
            if item_name in loaded_items:
                item = loaded_items[item_name]
                print(f"\n--- Details for {item_name} ({type(item).__name__}) ---")
                print(f"  Name: {item.name}")
                print(f"  Description: {item.description}")
                if isinstance(item, Consumable):
                    print(f"  Category: {item.category}")
                    print(f"  Effect: {item.effect_description}")
                    print(f"  Recipe: '{item.recipe}'")
                print(f"  Rarity: {item.rarity}")
                print(f"  Full __str__: {item}")
            else:
                print(f"\nItem '{item_name}' not found in loaded items.")

    except FileNotFoundError:
        print(f"Error: Consumables/Materials CSV file was not found at '{consumables_csv_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during consumables/materials loading: {e}")
    
    print("\nConsumables and materials loading test finished.")


def load_weapons_from_csv(file_path: str) -> Dict[str, 'Weapon']:
    """
    Loads weapon data from a CSV file.
    The CSV has sections like "Swords Level 1-50", each with its own header row.
    """
    weapons: Dict[str, Weapon] = {}
    current_weapon_category: Union[str, None] = None
    skip_next_row_as_header: bool = False

    weapon_category_keywords = {
        "Swords": "Sword", "Daggers": "Dagger", "Axes": "Axe",
        "Polearm": "Polearm", "Staff": "Staff", "Mace": "Mace",
        "Hammers": "Hammer", "Bows": "Bow", "Crossbow": "Crossbow",
        "Gun": "Gun" 
        # Add more if the CSV contains other primary keywords like "Wands", "Spears", etc.
    }

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row_number, row in enumerate(reader, start=1):
            if not row or not any(field.strip() for field in row): # Skip fully empty or whitespace-only rows
                continue
            
            # Check for separator rows like ",,,,,,,,,,,"
            if all(not field.strip() for field in row):
                # print(f"Skipping separator row {row_number}")
                continue

            first_cell_value = row[0].strip()

            # Identify weapon category section headers
            identified_category = False
            for keyword, category_name in weapon_category_keywords.items():
                if first_cell_value.startswith(keyword):
                    current_weapon_category = category_name
                    skip_next_row_as_header = True # The row after this is the actual column header
                    # print(f"Switched to weapon category: {current_weapon_category} (from '{first_cell_value}') at row {row_number}")
                    identified_category = True
                    break
            
            if identified_category:
                continue # Skip the category defining row itself

            if skip_next_row_as_header:
                skip_next_row_as_header = False # This row is the column header, skip it
                # print(f"Skipping column header row {row_number} for category {current_weapon_category}")
                continue

            if not current_weapon_category:
                # print(f"Skipping row {row_number} as no weapon category is active: {row}")
                continue

            # At this point, we should be processing actual weapon data rows
            name = first_cell_value
            if not name: # Skip if name is empty
                # print(f"Skipping row {row_number} due to empty weapon name in category {current_weapon_category}.")
                continue

            # Defensive check for row length
            if len(row) < 15: # Expecting up to at least column index 14 (Extra Increases)
                # print(f"Skipping row {row_number} for '{name}' due to insufficient columns ({len(row)}). Data: {row}")
                continue

            try:
                level_range = row[1].strip()
                source = row[2].strip()
                tier = row[3].strip()
                attack_type = row[4].strip()

                attack_bonus = _to_int(row[5])
                defense_bonus = _to_int(row[6])
                magic_attack_bonus = _to_int(row[7])
                magic_defense_bonus = _to_int(row[8])
                agility_bonus = _to_int(row[9])
                luck_bonus = _to_int(row[10])
                max_hp_bonus = _to_int(row[11])
                max_mp_bonus = _to_int(row[12])
                
                recipe = row[13].strip()
                extra_increases = row[14].strip()

                description = f"{tier} {current_weapon_category} (Lvl: {level_range})." if tier and level_range else f"{tier} {current_weapon_category}."
                equip_type = "Main Hand" # Default as per subtask

                weapon_obj = Weapon(
                    name=name,
                    description=description,
                    tier=tier,
                    equip_type=equip_type,
                    attack_type=attack_type,
                    weapon_category=current_weapon_category,
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
                    source=source
                )
                weapons[name] = weapon_obj
            
            except IndexError:
                # print(f"Warning: Skipping row {row_number} for weapon '{name}' due to IndexError. Row data: {row}")
                continue
            except Exception as e:
                # print(f"Warning: An unexpected error occurred while processing row {row_number} for weapon '{name}': {e}. Row data: {row}")
                continue
                
    return weapons


if __name__ == '__main__':
    # --- Load Equipment ---
    equipment_csv_path = "Game Csv Data/Armor, Accesories, Shields.csv"
    
    if not os.path.exists(equipment_csv_path):
        print(f"Test CSV file for equipment not found at {equipment_csv_path}. Creating a dummy file for basic testing.")
        dummy_dir = os.path.dirname(equipment_csv_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        with open(equipment_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Armor","","Tier","Recipe","Equip Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max Hp","Max Mp","Extra Increases","Additional Changes","Source"])
            writer.writerow(["Leather Cap","","Common","2 Leather","Helmet","","2","","","1","","","","","","Crafted"])
    
    print(f"Attempting to load equipment from: {os.path.abspath(equipment_csv_path)}")
    try:
        loaded_equipment = load_equipment_from_csv(equipment_csv_path)
        print(f"\nTotal equipment pieces loaded: {len(loaded_equipment)}")
        if "Leather Cap" in loaded_equipment:
            print(f"  Example Equipment: {loaded_equipment['Leather Cap']}")
    except FileNotFoundError:
        print(f"Error: Equipment CSV file was not found at '{equipment_csv_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during equipment loading: {e}")
    print("\nEquipment loading test finished.")

    # --- Load Consumables and Materials ---
    consumables_csv_path = "Game Csv Data/Potions, Consumables, Materials.csv"

    if not os.path.exists(consumables_csv_path):
        print(f"Test CSV file for consumables/materials not found at {consumables_csv_path}. Creating a dummy file for basic testing.")
        dummy_dir = os.path.dirname(consumables_csv_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        with open(consumables_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Potions", "", "Effect Notes", "", ""])
            writer.writerow(["Crude Health Potion", "", "Restores 25 HP", "", ""])
            writer.writerow(["Special Consumable", "Rarity", "", "Effect Notes", ""])
            writer.writerow(["Crystal Glow Berry", "Uncommon", "", "Grants Night Vision for 5 minutes", ""])
            writer.writerow(["Food", "Rarity", "Effect", "Recipe", ""])
            writer.writerow(["Dried Meat", "Common", "Restores 5 HP over 10 seconds", "1x Raw Meat, 1x Salt", ""])
            writer.writerow(["Raw Ingriedient", "Rarity", "", "", ""])
            writer.writerow(["Chomper Filet", "Common", "", "", ""])

    print(f"\nAttempting to load consumables and materials from: {os.path.abspath(consumables_csv_path)}")
    try:
        loaded_items = load_consumables_and_materials_from_csv(consumables_csv_path)
        print(f"\nTotal consumables and materials loaded: {len(loaded_items)}")
        sample_items_to_check = {"Crude Health Potion": Consumable, "Crystal Glow Berry": Consumable, "Dried Meat": Consumable, "Chomper Filet": Material}
        for item_name, item_type in sample_items_to_check.items():
            if item_name in loaded_items:
                item = loaded_items[item_name]
                print(f"  Example {item_type.__name__}: {item_name} - {item.description[:50]}...")
    except FileNotFoundError:
        print(f"Error: Consumables/Materials CSV file was not found at '{consumables_csv_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during consumables/materials loading: {e}")
    print("\nConsumables and materials loading test finished.")

    # --- Load Weapons ---
    weapons_csv_path = "Game Csv Data/Revised Weapon Sheet.csv"

    if not os.path.exists(weapons_csv_path):
        print(f"Test CSV file for weapons not found at {weapons_csv_path}. Creating a dummy file for basic testing.")
        dummy_dir = os.path.dirname(weapons_csv_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        with open(weapons_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Swords Level 1-50,Level Range,Source,Tier,Attack Type,Attack,Defense,M.Attack,M.Defense,Agility,Luck,Max HP,Max MP,Recipe,Extra Increases
            writer.writerow(["Swords Level 1-50","Level Range","Source","Tier","Attack Type","Attack","Defense","M.Attack","M.Defense","Agility","Luck","Max HP","Max MP","Recipe","Extra Increases"])
            writer.writerow(["Sharp Vine Stick","1-5","Gathering","Basic","Physical","3","","","","1","","","","","Vine Whip"])
            writer.writerow(["Iron Sword","5-10","Crafting","Common","Physical","10","1","","","","1","5","","","Heavy Swing"])
            writer.writerow([",,,,,,,,,,,,,,"]) # Separator
            # Daggers Level 1-50,Level Range,,Tier,Attack Type,Attack Damage,Defense,M.Attack,M.Defense,Agility,Luck,Max HP,Max MP,,Extra Increases
            writer.writerow(["Daggers Level 1-50","Level Range","","Tier","Attack Type","Attack Damage","Defense","M.Attack","M.Defense","Agility","Luck","Max HP","Max MP","","Extra Increases"])
            writer.writerow(["Rusty Knife","1-5","Bandit Drop","Basic","Physical","2","","","","-1","","","","","Tetanus Shot"])
            writer.writerow(["Chomper Tooth Dagger","5-10","Chomper Drop","Common","Physical","8","","","1","2","1","","","1x Chomper Tooth, 1x Vine","Quick Stab"])

    print(f"\nAttempting to load weapons from: {os.path.abspath(weapons_csv_path)}")
    try:
        loaded_weapons = load_weapons_from_csv(weapons_csv_path)
        print(f"\nTotal weapons loaded: {len(loaded_weapons)}")
        
        sample_weapons_to_check = ["Sharp Vine Stick", "Iron Sword", "Rusty Knife", "Chomper Tooth Dagger"]
        for weapon_name in sample_weapons_to_check:
            if weapon_name in loaded_weapons:
                weapon = loaded_weapons[weapon_name]
                print(f"\n--- Details for {weapon_name} ---")
                print(f"  Name: {weapon.name}, Category: {weapon.weapon_category}, Attack Type: {weapon.attack_type}")
                print(f"  Tier: {weapon.tier}, Equip Type: {weapon.equip_type}")
                print(f"  Description: {weapon.description}")
                print(f"  ATK: {weapon.attack_bonus}, DEF: {weapon.defense_bonus}, M.ATK: {weapon.magic_attack_bonus}, M.DEF: {weapon.magic_defense_bonus}")
                print(f"  AGI: {weapon.agility_bonus}, LCK: {weapon.luck_bonus}, MaxHP: {weapon.max_hp_bonus}, MaxMP: {weapon.max_mp_bonus}")
                print(f"  Recipe: '{weapon.recipe}', Source: '{weapon.source}'")
                print(f"  Extra: '{weapon.extra_increases}'")
                print(f"  Full __str__: {weapon}")
            else:
                print(f"\nWeapon '{weapon_name}' not found in loaded weapons.")
    except FileNotFoundError:
        print(f"Error: Weapons CSV file was not found at '{weapons_csv_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during weapons loading: {e}")

    print("\nWeapons loading test finished.")
