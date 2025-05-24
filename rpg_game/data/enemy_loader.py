import csv
from typing import Dict, List, Tuple, Optional
# Adjust the import path based on your project structure.
try:
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.skill import Skill # For type hinting and dummy data
    from rpg_game.core.item import Item   # For type hinting and dummy data
    from rpg_game.core.consumable import Consumable # For dummy item data
    from rpg_game.core.material import Material # For dummy item data
    from rpg_game.world.zone import Zone # Import Zone

except ImportError:
    # Fallback for cases where the script might be run directly
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # To find 'core'
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'world')) # To find 'world'
    from core.enemy import Enemy
    from core.skill import Skill
    from core.item import Item
    from core.consumable import Consumable
    from core.material import Material
    from world.zone import Zone


def parse_list_from_string(s: str) -> List[str]:
    """Parses a comma-separated string into a list of strings."""
    if not s:
        return []
    return [item.strip() for item in s.split(',') if item.strip()]

def load_enemies_from_csv(file_path: str, 
                          skills_data: Dict[str, Skill], 
                          items_data: Dict[str, Item]) -> Tuple[Dict[str, Enemy], Dict[str, Zone]]:
    """
    Loads enemy data from a CSV file and returns a dictionary of Enemy objects,
    linking abilities/spells and loot to actual Skill and Item objects.
    Also loads zone information from the same CSV.
    """
    enemies: Dict[str, Enemy] = {}
    zones: Dict[str, Zone] = {}
    current_zone: Optional[Zone] = None
    
    expected_headers = [
        "Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", 
        "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", 
        "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"
    ]

    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Skip header row

            # Verify header (optional but good practice)
            if header != expected_headers:
                print(f"Warning: CSV header mismatch. Expected {expected_headers}, got {header}")
                # You might want to raise an error or handle this more gracefully

            for row_number, row in enumerate(reader, start=2): # start=2 because 1 is header, 2 is first data row
                if not any(row): # Skip completely empty rows
                    print(f"Skipping empty row at line {row_number}")
                    continue

                name_cell = row[0].strip()

                # Zone Marker Detection
                # Heuristic: first cell contains "Zone", "Den", "Citadel" etc.
                # AND other critical cells (like HP at index 4, Attack at index 6) are empty.
                is_zone_marker = False
                if name_cell:
                    zone_keywords = ["zone", "den", "citadel", "lair", "sanctum", "ruins", "plains", "forest", "mountain", "cave", "swamp"]
                    is_potential_zone = any(keyword in name_cell.lower() for keyword in zone_keywords)
                    
                    # Check if critical stat cells are empty (or non-numeric, though empty check is simpler here)
                    # Assuming HP is row[4], Attack is row[6]
                    if is_potential_zone and len(row) > 6 and \
                       (not row[4].strip() and not row[6].strip()):
                        is_zone_marker = True

                if is_zone_marker:
                    zone_name = name_cell
                    current_zone = Zone(name=zone_name)
                    zones[zone_name] = current_zone
                    print(f"Detected Zone: {zone_name} at row {row_number}")
                    continue # Skip to the next row

                # Existing check for rows that look like separators but aren't formal zone markers
                # e.g. "Goblinoid Lair,,,,,,,,,,,,,,," (if the above didn't catch it as a Zone)
                if name_cell and all(not c.strip() for c in row[1:len(expected_headers)-1]): # Check if all other expected cells are empty
                    # This might be a sub-header or separator not intended as a new Zone object.
                    # If it was meant to be a Zone, it should have been caught by the more specific check above.
                    # For now, we'll just skip these as they are not valid enemies.
                    # If this row *should* define a zone, the heuristic above needs adjustment.
                    print(f"Skipping potential sub-header or separator row: {name_cell} at line {row_number}")
                    continue


                if len(row) != len(expected_headers):
                    print(f"Warning: Skipping row {row_number} due to incorrect number of columns. Expected {len(expected_headers)}, got {len(row)}. Row: '{','.join(row)}'")
                    continue

                try:
                    name = name_cell # Already stripped
                    if not name: # Skip if name is empty (should be caught by `any(row)` or zone checks mostly)
                        print(f"Warning: Skipping row {row_number} due to empty enemy name.")
                        continue
                    
                    # If it's an enemy row, and a zone is active, add enemy to zone
                    if current_zone:
                        current_zone.add_enemy_name(name)

                    level_range = row[1].strip()
                    spawn_chance = row[2].strip()
                    enemy_type = row[3].strip()
                    
                    # Numeric fields with error handling
                    try:
                        max_hp = int(row[4]) if row[4] else 0
                        max_mp = int(row[5]) if row[5] else 0
                        attack_power = int(row[6]) if row[6] else 0
                        defense = int(row[7]) if row[7] else 0
                        magic_attack = int(row[8]) if row[8] else 0
                        magic_defense = int(row[9]) if row[9] else 0 # M.Defense.
                        agility = int(row[10]) if row[10] else 0
                        luck = int(row[11]) if row[11] else 0
                    except ValueError as e:
                        print(f"Warning: Skipping enemy '{name}' (row {row_number}) due to invalid numeric value: {e}. Row data: {row}")
                        continue

                    has_sprite = row[12].strip().lower() == "yes"
                    
                    abilities_spells_str_list = parse_list_from_string(row[13])
                    resolved_abilities_spells: List[Skill] = []
                    for skill_name_str in abilities_spells_str_list:
                        skill_obj = skills_data.get(skill_name_str.strip())
                        if skill_obj:
                            resolved_abilities_spells.append(skill_obj)
                        else:
                            print(f"Warning: Skill '{skill_name_str}' not found for enemy '{name}'.")
                    
                    # row[14] is the empty column, skipped
                    loot_str_list = parse_list_from_string(row[15])
                    resolved_loot_items: List[Item] = []
                    for item_name_str in loot_str_list:
                        item_obj = items_data.get(item_name_str.strip())
                        if item_obj:
                            resolved_loot_items.append(item_obj)
                        else:
                            print(f"Warning: Loot item '{item_name_str}' not found for enemy '{name}'.")

                    enemy_obj = Enemy(
                        name=name,
                        max_hp=max_hp,
                        attack_power=attack_power,
                        defense=defense,
                        level_range=level_range,
                        spawn_chance=spawn_chance,
                        enemy_type=enemy_type,
                        max_mp=max_mp,
                        magic_attack=magic_attack,
                        magic_defense=magic_defense,
                        agility=agility,
                        luck=luck,
                        has_sprite=has_sprite,
                        abilities_spells=resolved_abilities_spells,
                        loot=resolved_loot_items,
                        zone_name=current_zone.name if current_zone else None
                    )
                    enemies[name] = enemy_obj
                
                except IndexError:
                    print(f"Warning: Skipping row {row_number} due to missing columns for enemy '{name if 'name' in locals() else 'Unknown'}'. Row data: {row}")
                    continue
                except Exception as e:
                    print(f"Warning: An unexpected error occurred while processing enemy row {row_number} for '{name if 'name' in locals() else 'Unknown'}': {e}. Row data: {row}")
                    continue
                    
    except FileNotFoundError:
        # Let FileNotFoundError propagate as per previous discussions for loaders
        print(f"Error: The file '{file_path}' was not found.")
        raise # Re-raise the exception
    except Exception as e:
        print(f"An error occurred while opening or reading the file: {e}")
        # For other critical errors during file processing, return empty dicts
        return {}, {}

    return enemies, zones

if __name__ == '__main__':
    # For standalone testing of this loader, create dummy skills and items data.
    class MockSkill(Skill): 
        def __init__(self, name, description="Mock Skill Desc", skill_rarity="Common", skill_type_csv="Active", category="Mock Category"):
            super().__init__(name, description, skill_rarity, skill_type_csv, category)
        def __repr__(self): return f"Skill(name='{self.name}')"

    class MockItem(Item):
        def __init__(self, name, description="Mock Item Desc"):
            super().__init__(name, description)
        def __repr__(self): return f"Item(name='{self.name}')"

    dummy_skills_data = {
        "Acorn Toss": MockSkill(name="Acorn Toss"), "Backhand": MockSkill(name="Backhand"), 
        "Crack Pot": MockSkill(name="Crack Pot"), "Fade": MockSkill(name="Fade"), 
        "Spirit Bolt": MockSkill(name="Spirit Bolt"), "Sand Bite": MockSkill(name="Sand Bite")
    }
    dummy_items_data = {
        "Nut": Material(name="Nut", description="A simple nut.", rarity="Common"), 
        "Twig": Material(name="Twig", description="A small twig.", rarity="Common"),
        "Small Coin": Material(name="Small Coin", description="A bit of currency.", rarity="Common"), 
        "Rusty Shank": Item(name="Rusty Shank", description="A crude, rusty knife."),
        "Ectoplasm": Material(name="Ectoplasm", description="Ghostly residue.", rarity="Uncommon"), 
        "Faint Glow": Material(name="Faint Glow", description="A faintly glowing wisp.", rarity="Common"),
        "Snake Scale": Material(name="Snake Scale", description="A dry scale.", rarity="Common")
    }
    
    script_dir = os.path.dirname(__file__)
    # Try to find project root assuming script is in rpg_game/data or similar
    project_root_candidate = os.path.abspath(os.path.join(script_dir, "..", "..")) 
    test_csv_relative_path = "Game Csv Data/Enemy's Sheet.csv"
    
    if os.path.exists(os.path.join(project_root_candidate, test_csv_relative_path)):
        base_path_for_csv = project_root_candidate
    else: # Fallback for running directly in a flat structure or if 'Game Csv Data' is sibling to script's dir
        base_path_for_csv = "." 
        if not os.path.exists(test_csv_relative_path): # If still not found, assume it's in a standard test location
             base_path_for_csv = os.path.join(script_dir, "..", "..") # Typical sandbox root relative to this file
             print(f"Warning: CSV path auto-detection is approximate. Using base: {base_path_for_csv}")


    test_csv_path = os.path.join(base_path_for_csv, test_csv_relative_path)

    if not os.path.exists(test_csv_path):
        print(f"Actual enemy CSV not found at '{test_csv_path}'. Creating a dummy file for testing.")
        dummy_csv_dir = os.path.dirname(test_csv_path)
        if dummy_csv_dir and not os.path.exists(dummy_csv_dir):
            os.makedirs(dummy_csv_dir, exist_ok=True)
        
        if dummy_csv_dir or os.path.exists(os.path.dirname(test_csv_path)): # Check dir exists or can be made
            with open(test_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"])
                writer.writerow(["Forest Zone", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
                writer.writerow(["Squirrelkin", "1-2", "Common", "Beast", "30", "5", "5", "2", "0", "1", "8", "3", "Yes", "Acorn Toss", "", "Nut, Twig"])
                writer.writerow(["Goblin Crook", "2-4", "Common", "Goblinoid", "45", "10", "8", "4", "2", "2", "6", "2", "Yes", "Backhand, Crack Pot", "", "Small Coin, Rusty Shank"])
                writer.writerow(["Desert Zone", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
                writer.writerow(["Sand Snake", "3-4", "Common", "Beast", "40", "0", "7", "3", "0", "0", "5", "2", "Yes", "Sand Bite", "", "Snake Scale"])
        else:
            print(f"Skipping dummy CSV creation as directory for '{test_csv_path}' is problematic.")

    print(f"Attempting to load enemies and zones from: {os.path.abspath(test_csv_path)}")
    if os.path.exists(test_csv_path):
        try:
            loaded_enemies, loaded_zones = load_enemies_from_csv(test_csv_path, dummy_skills_data, dummy_items_data)
            print(f"\nTotal enemies loaded: {len(loaded_enemies)}")
            print(f"Total zones loaded: {len(loaded_zones)}")

            for enemy_name in ["Squirrelkin", "Goblin Crook", "Sand Snake"]:
                if enemy_name in loaded_enemies:
                    enemy = loaded_enemies[enemy_name]
                    print(f"\nDetails for {enemy.name}: HP {enemy.max_hp}, ATK {enemy.attack_power}, Zone: {enemy.zone_name}")
                    skill_names = [s.name for s in enemy.abilities_spells]
                    loot_names = [l.name for l in enemy.loot]
                    print(f"  Abilities: {skill_names}, Loot: {loot_names}")

            if "Forest Zone" in loaded_zones:
                fz = loaded_zones["Forest Zone"]
                print(f"\nDetails for Forest Zone: Name '{fz.name}'")
                print(f"  Enemies in Forest Zone: {fz.enemy_names}")
            
            if "Desert Zone" in loaded_zones:
                dz = loaded_zones["Desert Zone"]
                print(f"\nDetails for Desert Zone: Name '{dz.name}'")
                print(f"  Enemies in Desert Zone: {dz.enemy_names}")
                if "Sand Snake" in dz.enemy_names and "Sand Snake" in loaded_enemies:
                    print("  Sand Snake correctly listed in Desert Zone and loaded.")


        except FileNotFoundError:
            print(f"  Error: File not found during __main__ execution: {test_csv_path}")
        except Exception as e:
            print(f"  An unexpected error occurred in __main__: {e}")

    else:
        print(f"Enemy CSV file '{test_csv_path}' not found and dummy creation possibly failed. Skipping enemy/zone loading test in __main__.")

    print("\nEnemy loader __main__ test finished.")
