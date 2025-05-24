import csv
from typing import Dict, Optional

# Adjust import path based on project structure
try:
    from rpg_game.core.status_effect import StatusEffect
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.status_effect import StatusEffect

def _normalize_status_cell_value(value: str) -> str:
    """Converts 'Null' or empty strings to an empty string, otherwise strips whitespace."""
    stripped_value = value.strip()
    if stripped_value.lower() == "null" or stripped_value == "":
        return ""
    return stripped_value

def load_status_effects_from_csv(file_path: str) -> Dict[str, StatusEffect]:
    """
    Loads status effect data from a CSV file.
    The CSV is section-based: "Positive States" and "Negative States".
    """
    status_effects: Dict[str, StatusEffect] = {}
    current_effect_type: Optional[str] = None

    section_headers = {
        "Positive States": "Positive",
        "Negative States": "Negative"
    }
    
    # Expected columns for data rows (0-indexed):
    # Name (0), Element (1), Duration (2), Effect (3), Notes (4)

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row_number, row in enumerate(reader, start=1):
            if not row or not any(_normalize_status_cell_value(cell) for cell in row): # Skip fully empty rows
                continue

            first_cell_raw = row[0].strip()

            # Check if this row defines a new section
            if first_cell_raw in section_headers:
                current_effect_type = section_headers[first_cell_raw]
                # print(f"Row {row_number}: Switched to section: {current_effect_type}")
                continue

            if not current_effect_type:
                # print(f"Row {row_number}: Skipped as no effect type section is active. Data: {row[0]}")
                continue
            
            # Data Row Parsing
            name = _normalize_status_cell_value(first_cell_raw)
            if not name or name == "Positive States" or name == "Negative States": # Skip if name is empty or a section title
                # print(f"Row {row_number}: Skipped due to empty name or name matching section title. Name: '{name}'")
                continue

            # Ensure row has enough columns for all expected fields up to Notes (index 4)
            if len(row) < 5:
                # print(f"Row {row_number}: Skipped due to insufficient columns ({len(row)}). Data: {row[0]}")
                continue
            
            element = _normalize_status_cell_value(row[1])
            duration_str = _normalize_status_cell_value(row[2])
            effect_str = _normalize_status_cell_value(row[3]) # Main effect description
            notes = _normalize_status_cell_value(row[4])

            # Create a general description. Can be refined.
            description = f"{current_effect_type} effect. {effect_str}" if effect_str else f"A {current_effect_type.lower()} status effect."
            if not effect_str and notes: # If no main effect, but notes exist, use notes for description.
                 description = notes
            elif not effect_str and not notes: # Fallback if both are empty
                 description = f"A {current_effect_type.lower()} status effect named {name}."


            try:
                status_effect_obj = StatusEffect(
                    name=name,
                    description=description,
                    effect_type=current_effect_type,
                    element=element,
                    duration_str=duration_str,
                    effect_description=effect_str, # This is the primary mechanical effect
                    notes=notes
                )
                
                if name in status_effects:
                    # print(f"Warning: Duplicate status effect name '{name}' found at row {row_number}. Overwriting previous entry.")
                    pass 
                status_effects[name] = status_effect_obj

            except Exception as e:
                # print(f"Error instantiating status effect '{name}' at row {row_number}: {e}. Data: {row[:5]}")
                continue
                
    return status_effects

if __name__ == '__main__':
    csv_file_path = "Game Csv Data/Buffs & Debuffs.csv"

    # Create a dummy CSV if it doesn't exist for basic testing
    if not os.path.exists(csv_file_path):
        print(f"Test CSV file for status effects not found at {csv_file_path}. Creating a dummy file.")
        dummy_dir = os.path.dirname(csv_file_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Headers and sample data matching the expected CSV structure
            # Name,Element,Duration,Effect,Notes,,,,,,,,,,,,
            writer.writerow(["Positive States", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Element","Duration","Effect","Notes"]) # Actual column header (usually skipped by logic if name matches section)
            writer.writerow(["Distorted Reality","Arcane","Until End of Battle","Increases chance to dodge magical attacks by 25%.","Often applied by powerful dimensional beings."])
            writer.writerow(["Enlightened","Light","5 Turns","Increases Magic Attack and Magic Defense by 15%.","A state of pure focus."])
            writer.writerow(["Null","Null","Null","Null","Null"]) # Test "Null" conversion
            
            writer.writerow(["Negative States", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Element","Duration","Effect","Notes"]) # Actual column header
            writer.writerow(["Poison","Nature","3 Turns","Deals 5% of Max HP as Nature damage at the start of each turn.","Can be cured by Antidote."])
            writer.writerow(["Silence","Dark","2 Turns","Prevents casting of spells.","Frustrating for mages."])

    print(f"Attempting to load status effects from: {os.path.abspath(csv_file_path)}")
    try:
        loaded_status_effects = load_status_effects_from_csv(csv_file_path)
        print(f"\nTotal status effects loaded: {len(loaded_status_effects)}")

        effects_to_verify = ["Distorted Reality", "Poison", "Enlightened", "Silence"]
        if "Null" in loaded_status_effects: # Should not be loaded as a valid name if logic is correct
            print("Error: 'Null' was loaded as a status effect name.")
        
        for effect_name in effects_to_verify:
            if effect_name in loaded_status_effects:
                effect = loaded_status_effects[effect_name]
                print(f"\n--- Details for {effect_name} ---")
                print(f"  Name: {effect.name}")
                print(f"  Type: {effect.effect_type}")
                print(f"  Description: {effect.description}")
                print(f"  Element: {effect.element}")
                print(f"  Duration: {effect.duration_str}")
                print(f"  Effect Desc: {effect.effect_description}")
                print(f"  Notes: {effect.notes}")
            else:
                print(f"\nStatus Effect '{effect_name}' not found in loaded effects.")
                if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) < 200:
                     print(f"  (Note: This might be due to using a minimal dummy CSV for testing.)")

    except FileNotFoundError:
        print(f"Error: The status effects CSV file was not found at '{csv_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during status effect loading: {e}")

    print("\nStatus effect loading test finished.")
