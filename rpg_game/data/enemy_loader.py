import csv
from typing import Dict, List
# Adjust the import path based on your project structure.
try:
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.skill import Skill # For type hinting and dummy data
    from rpg_game.core.item import Item   # For type hinting and dummy data
    from rpg_game.core.consumable import Consumable # For dummy item data
    from rpg_game.core.material import Material # For dummy item data

except ImportError:
    # Fallback for cases where the script might be run directly
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # To find 'core'
    from core.enemy import Enemy
    from core.skill import Skill
    from core.item import Item
    from core.consumable import Consumable
    from core.material import Material


def parse_list_from_string(s: str) -> List[str]:
    """Parses a comma-separated string into a list of strings."""
    if not s:
        return []
    return [item.strip() for item in s.split(',') if item.strip()]

def load_enemies_from_csv(file_path: str, 
                          skills_data: Dict[str, Skill], 
                          items_data: Dict[str, Item]) -> Dict[str, Enemy]:
    """
    Loads enemy data from a CSV file and returns a dictionary of Enemy objects,
    linking abilities/spells and loot to actual Skill and Item objects.
    """
    enemies: Dict[str, Enemy] = {}
    
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
                if not any(row) or (row[0] and all(not c for c in row[1:])): # Skip empty rows or zone separators
                    if row[0] and ("Zone" in row[0] or "Den" in row[0]): # Heuristic for zone separators
                         print(f"Skipping zone separator or empty row: {row[0]}")
                         continue
                    elif not any(row): # Completely empty row
                        print(f"Skipping empty row at line {row_number}")
                        continue


                if len(row) != len(expected_headers):
                    print(f"Warning: Skipping row {row_number} due to incorrect number of columns. Expected {len(expected_headers)}, got {len(row)}. Data: {row}")
                    continue

                try:
                    name = row[0].strip()
                    if not name: # Skip if name is empty
                        print(f"Warning: Skipping row {row_number} due to empty enemy name.")
                        continue

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
                        loot=resolved_loot_items
                    )
                    enemies[name] = enemy_obj
                
                except IndexError:
                    print(f"Warning: Skipping row {row_number} due to missing columns. Data: {row}")
                    continue
                except Exception as e:
                    print(f"Warning: An unexpected error occurred while processing row {row_number} for enemy '{row[0] if row else 'Unknown'}': {e}. Data: {row}")
                    continue
                    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {} # Return empty dict if file not found
    except Exception as e:
        print(f"An error occurred while opening or reading the file: {e}")
        return {}

    return enemies

if __name__ == '__main__':
    # Create a dummy CSV file for testing if it doesn't exist.
    # The actual path "Game Csv Data/Enemy's Sheet.csv" suggests it's outside the repo
    # For standalone testing of this loader, create dummy skills and items data.
    # In the actual game, GameDataManager would provide these.
    
    # Dummy Skill and Item classes for standalone testing if real ones are complex
    class MockSkill(Skill): # Inherit from real Skill to satisfy type hints
        def __init__(self, name, description="Mock Skill Desc", skill_rarity="Common", skill_type_csv="Active", category="Mock Category"):
            super().__init__(name, description, skill_rarity, skill_type_csv, category)
        def __repr__(self): return f"Skill(name='{self.name}')"

    class MockItem(Item): # Inherit from real Item
        def __init__(self, name, description="Mock Item Desc"):
            super().__init__(name, description)
        def __repr__(self): return f"Item(name='{self.name}')"

    dummy_skills_data = {
        "Acorn Toss": MockSkill(name="Acorn Toss"),
        "Backhand": MockSkill(name="Backhand"),
        "Crack Pot": MockSkill(name="Crack Pot"),
        "Fade": MockSkill(name="Fade"),
        "Spirit Bolt": MockSkill(name="Spirit Bolt")
    }
    dummy_items_data = {
        "Nut": Material(name="Nut", description="A simple nut.", rarity="Common"),
        "Twig": Material(name="Twig", description="A small twig.", rarity="Common"),
        "Small Coin": Material(name="Small Coin", description="A bit of currency.", rarity="Common"),
        "Rusty Shank": Item(name="Rusty Shank", description="A crude, rusty knife."), # Generic Item
        "Ectoplasm": Material(name="Ectoplasm", description="Ghostly residue.", rarity="Uncommon"),
        "Faint Glow": Material(name="Faint Glow", description="A faintly glowing wisp.", rarity="Common")
    }
    
    # Determine base path for CSVs, assuming this script is in rpg_game/data
    # and "Game Csv Data" is at the project root (e.g., /app/Game Csv Data)
    # The path used here assumes running from within rpg_game/data
    # For running from project root like '/app', it would be "Game Csv Data/Enemy's Sheet.csv"
    
    # Try to make the path more robust for common execution contexts
    script_dir = os.path.dirname(__file__)
    project_root_candidate1 = os.path.abspath(os.path.join(script_dir, "..", "..")) # If script is in /app/rpg_game/data
    project_root_candidate2 = os.path.abspath(os.path.join(script_dir, ".."))      # If script is in /app/data
    
    test_csv_relative_path = "Game Csv Data/Enemy's Sheet.csv"
    
    if os.path.exists(os.path.join(project_root_candidate1, test_csv_relative_path)):
        base_path_for_csv = project_root_candidate1
    elif os.path.exists(os.path.join(project_root_candidate2, test_csv_relative_path)):
         base_path_for_csv = project_root_candidate2
    elif os.path.exists(test_csv_relative_path): # Running from a dir that has "Game Csv Data" as subdir
        base_path_for_csv = "."
    else: # Fallback if structure is unexpected, try relative to script dir (might fail if not in place)
        base_path_for_csv = os.path.join(script_dir, "..", "..") # Default assumption for typical sandbox
        print(f"Warning: Could not auto-detect CSV path structure well. Falling back to: {base_path_for_csv}")

    test_csv_path = os.path.join(base_path_for_csv, test_csv_relative_path)

    # Ensure dummy CSV directory and file exist if the actual one is not found
    # This is primarily for making this __main__ block runnable in test environments.
    if not os.path.exists(test_csv_path):
        print(f"Actual enemy CSV not found at '{test_csv_path}'. Creating a dummy file for testing.")
        # Ensure the directory for the dummy CSV exists
        dummy_csv_dir = os.path.dirname(test_csv_path)
        if dummy_csv_dir and not os.path.exists(dummy_csv_dir):
            try:
                os.makedirs(dummy_csv_dir)
                print(f"Created directory: {dummy_csv_dir}")
            except OSError as e:
                print(f"Failed to create directory {dummy_csv_dir}: {e}")
        
        # Create the dummy CSV file
        if dummy_csv_dir : # Only proceed if directory creation was successful or dir exists
            with open(test_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Name", "Level Range", "Spawn Chance", "Type", "Max Hp Lowest Level", 
                    "Max Mp", "Attack", "Defense", "M.Attack", "M.Defense.", "Agility", 
                    "Luck", "Has Sprite?", "Abilitys & Spells", "", "Enemy Loot"
                ])
                writer.writerow(["Squirrelkin", "1-2", "Common", "Beast", "30", "5", "5", "2", "0", "1", "8", "3", "Yes", "Acorn Toss", "", "Nut, Twig"])
                writer.writerow(["Goblin Crook", "2-4", "Common", "Goblinoid", "45", "10", "8", "4", "2", "2", "6", "2", "Yes", "Backhand, Crack Pot", "", "Small Coin, Rusty Shank"])
                writer.writerow(["Night Wisp", "3-5", "Uncommon", "Spirit", "25", "30", "2", "5", "10", "8", "10", "5", "No", "Fade, Spirit Bolt", "", "Ectoplasm, Faint Glow"])
        else:
            print(f"Skipping dummy CSV creation as directory '{dummy_csv_dir}' could not be confirmed/created.")


    print(f"Attempting to load enemies from: {os.path.abspath(test_csv_path)}")
    # Only proceed if test_csv_path exists (either originally or created as dummy)
    if os.path.exists(test_csv_path):
        loaded_enemies = load_enemies_from_csv(test_csv_path, dummy_skills_data, dummy_items_data)
        print(f"\nTotal enemies loaded: {len(loaded_enemies)}")

        if "Squirrelkin" in loaded_enemies:
            sq = loaded_enemies["Squirrelkin"]
            print(f"\nDetails for Squirrelkin:")
            print(f"  Name: {sq.name}, HP: {sq.max_hp}, Attack: {sq.attack_power}")
            # Display names of resolved skill and item objects
            sq_skill_names = [s.name for s in sq.abilities_spells]
            sq_loot_names = [l.name for l in sq.loot]
            print(f"  Abilities: {sq_skill_names}")
            print(f"  Loot: {sq_loot_names}")
            if sq.abilities_spells and isinstance(sq.abilities_spells[0], Skill):
                 print("  Squirrelkin abilities are Skill objects.")
            if sq.loot and isinstance(sq.loot[0], Item):
                 print("  Squirrelkin loot are Item objects.")


        if "Goblin Crook" in loaded_enemies:
            gc = loaded_enemies["Goblin Crook"]
            print(f"\nDetails for Goblin Crook:")
            gc_skill_names = [s.name for s in gc.abilities_spells]
            gc_loot_names = [l.name for l in gc.loot]
            print(f"  Abilities: {gc_skill_names}") # Should be list of Skill objects
            print(f"  Loot: {gc_loot_names}")         # Should be list of Item objects
    else:
        print(f"Enemy CSV file '{test_csv_path}' not found and dummy creation failed. Skipping enemy loading for __main__ test.")


    # Test with a non-existent file (should now raise FileNotFoundError from open())
    print("\nTesting with a non-existent file (expect FileNotFoundError):")
    try:
        non_existent_enemies = load_enemies_from_csv("non_existent_enemy_sheet.csv", dummy_skills_data, dummy_items_data)
        print(f"Total enemies loaded from non-existent file: {len(non_existent_enemies)}")
    except FileNotFoundError as e:
        print(f"  Successfully caught FileNotFoundError: {e}")
    except Exception as e:
        print(f"  Unexpected error for non-existent file: {e}")


    print("\nEnemy loading test finished.")
