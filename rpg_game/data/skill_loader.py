import csv
from typing import Dict, Union, Tuple, Optional

# Adjust import path based on project structure
try:
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.skill import Skill, Ability, PassiveSkill, Spell

def _normalize_cell_value(value: str) -> str:
    """Converts 'Null' or empty strings to an empty string, otherwise strips whitespace."""
    stripped_value = value.strip()
    if stripped_value.lower() == "null" or stripped_value == "":
        return ""
    return stripped_value

def _determine_skill_category_and_type(first_cell_value: str) -> Optional[Tuple[str, str]]:
    """
    Determines the skill category and type (Passive, Spell, Ability) from a section header.
    Returns a tuple (parsed_category_name, class_type_str) or None.
    """
    first_cell_lower = first_cell_value.lower()
    
    # Order matters for more specific matches first
    passive_keywords = ["passives", "passive"]
    spell_keywords = ["spells", "magic", "spellbook", "sorcery", "wizardry", "elemental", "light", "dark", "fire", "ice", "wind", "earth", "thunder", "water", "arcane"] # Add more as needed
    
    # Check for Passives first
    for pk in passive_keywords:
        if pk in first_cell_lower:
            # Extract category name more cleanly, e.g., "Sword Passives" -> "Sword"
            category_name = first_cell_value.replace(pk, "").strip()
            if not category_name and "all class passive" in first_cell_lower: category_name = "All Class" # Specific case
            elif not category_name: category_name = "Generic Passive" # Fallback
            return category_name, "PassiveSkill"

    # Then check for Spells
    for sk in spell_keywords:
        if sk in first_cell_lower:
            # E.g. "Light Spells" -> "Light"
            category_name = first_cell_value.replace(sk, "").strip()
            if not category_name: category_name = first_cell_value # Use original if stripping leaves nothing
            return category_name, "Spell"

    # Default to Ability for other weapon/skill categories
    # e.g., "Sword", "Daggers", "Universal Melee", "Shields", "Staves", "Maces"
    # We can list explicit ability category keywords if needed, or assume anything not passive/spell is ability.
    ability_category_keywords = ["sword", "daggers", "axe", "bow", "gun", "melee", "shields", "staves", "maces", "polearm", "universal", "class", "job", "skills", "abilities"]
    for ak in ability_category_keywords:
        if ak in first_cell_lower:
            # E.g., "Sword Level 1-10" -> "Sword"
            category_name = first_cell_value.split("Level")[0].strip().split("Skills")[0].strip()
            if not category_name: category_name = first_cell_value
            return category_name, "Ability"
            
    # If it's a very generic header not caught above, but we expect data rows after
    # e.g. "General Skills" -> "General", "Ability"
    if "skills" in first_cell_lower or "abilities" in first_cell_lower:
        category_name = first_cell_value.split("Skills")[0].strip().split("Abilities")[0].strip()
        if not category_name: category_name = "Generic"
        return category_name, "Ability"

    return None # Not a recognized section header for skill categorization

def load_skills_from_csv(file_path: str) -> Dict[str, Skill]:
    skills: Dict[str, Skill] = {}
    current_category_tuple: Optional[Tuple[str, str]] = None # (parsed_category_name, class_type_str)
    skip_next_row_as_header: bool = False
    
    # CSV Column mapping (0-indexed) based on typical full header:
    # Name(0), Rarity(1), Type(2), Scope(3), Cost(4), Dmg Type(5), Element(6), Occasion(7), 
    # Formula(8), Variance(9), Critical(10), Hit Type(11), Animation(12), Requirement(13),
    # Effect(14), Additional Notes(15), Description(16)

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row_number, row in enumerate(reader, start=1):
            if not row or not any(_normalize_cell_value(cell) for cell in row): # Skip fully empty rows
                continue

            first_cell_norm = _normalize_cell_value(row[0])

            # Try to detect a new section category
            category_detection = _determine_skill_category_and_type(row[0].strip()) # Use raw value for detection
            if category_detection:
                current_category_tuple = category_detection
                skip_next_row_as_header = True
                # print(f"Row {row_number}: Detected section: {current_category_tuple[0]} as {current_category_tuple[1]}")
                continue

            if skip_next_row_as_header:
                skip_next_row_as_header = False
                # print(f"Row {row_number}: Skipped as column header for {current_category_tuple[0] if current_category_tuple else 'Unknown'}")
                continue

            if not current_category_tuple:
                # print(f"Row {row_number}: Skipped as no current category is active. Data: {row[0]}")
                continue
            
            parsed_category_name, class_type_str = current_category_tuple

            # Data Row Parsing
            if not first_cell_norm or first_cell_norm.lower() == parsed_category_name.lower():
                # print(f"Row {row_number}: Skipped empty name or name matching category. Data: {row[0]}")
                continue

            # Ensure row has enough columns for all expected fields up to description (index 16)
            if len(row) < 17:
                # print(f"Row {row_number}: Skipped due to insufficient columns ({len(row)}). Data: {row[0]}")
                continue

            name = first_cell_norm
            
            # Normalize all expected cells
            # Name(0) already done
            skill_rarity = _normalize_cell_value(row[1])
            skill_type_csv = _normalize_cell_value(row[2]) # e.g. "Active", "Passive"
            scope = _normalize_cell_value(row[3])
            cost = _normalize_cell_value(row[4])
            dmg_type = _normalize_cell_value(row[5])
            element = _normalize_cell_value(row[6])
            occasion = _normalize_cell_value(row[7])
            formula = _normalize_cell_value(row[8])
            variance = _normalize_cell_value(row[9])
            critical = _normalize_cell_value(row[10])
            hit_type = _normalize_cell_value(row[11])
            animation = _normalize_cell_value(row[12])
            requirement = _normalize_cell_value(row[13])
            effects_csv = _normalize_cell_value(row[14]) # "Effect" column
            additional_notes = _normalize_cell_value(row[15])
            description = _normalize_cell_value(row[16])
            
            # If description is empty, use effects_csv or a generic one.
            if not description:
                description = effects_csv if effects_csv else f"A {skill_rarity} {parsed_category_name} {class_type_str.lower().replace('skill','')}."


            skill_obj: Optional[Skill] = None
            try:
                if class_type_str == "PassiveSkill":
                    skill_obj = PassiveSkill(
                        name=name, description=description, skill_rarity=skill_rarity,
                        skill_type_csv=skill_type_csv if skill_type_csv else "Passive", # Default if CSV type empty
                        category=parsed_category_name,
                        effects_csv=effects_csv
                    )
                elif class_type_str == "Spell":
                    skill_obj = Spell(
                        name=name, description=description, skill_rarity=skill_rarity,
                        skill_type_csv=skill_type_csv if skill_type_csv else "Active", # Default if CSV type empty
                        category=parsed_category_name, scope=scope, cost=cost, dmg_type=dmg_type,
                        element=element, occasion=occasion, formula=formula, variance=variance,
                        critical=critical, hit_type=hit_type, animation=animation,
                        requirement=requirement, effects_csv=effects_csv,
                        additional_notes=additional_notes
                    )
                elif class_type_str == "Ability":
                    skill_obj = Ability(
                        name=name, description=description, skill_rarity=skill_rarity,
                        skill_type_csv=skill_type_csv if skill_type_csv else "Active", # Default if CSV type empty
                        category=parsed_category_name, scope=scope, cost=cost, dmg_type=dmg_type,
                        element=element, occasion=occasion, formula=formula, variance=variance,
                        critical=critical, hit_type=hit_type, animation=animation,
                        requirement=requirement, effects_csv=effects_csv,
                        additional_notes=additional_notes
                    )
                else:
                    # print(f"Row {row_number}: Unknown class type '{class_type_str}' for category '{parsed_category_name}'. Skipping '{name}'.")
                    continue
                
                if name in skills:
                    # print(f"Warning: Duplicate skill name '{name}' found. Overwriting previous entry.")
                    pass # Allow overwrite, or handle as error
                skills[name] = skill_obj

            except Exception as e:
                # print(f"Error instantiating skill '{name}' at row {row_number}: {e}. Data: {row[:17]}")
                continue
                
    return skills


if __name__ == '__main__':
    csv_file_path = "Game Csv Data/Spells & Abilitys.csv"

    # Create a dummy CSV if it doesn't exist for basic testing
    if not os.path.exists(csv_file_path):
        print(f"Test CSV file for skills not found at {csv_file_path}. Creating a dummy file.")
        dummy_dir = os.path.dirname(csv_file_path)
        if dummy_dir and not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir, exist_ok=True)
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Headers and sample data
            writer.writerow(["Sword Skills Level 1-10", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Rarity","Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effect","Additional Notes","Description"])
            writer.writerow(["Power Strike","Common","Active","1 Enemy","5 TP","Physical","Nil","Battle","PATK*1.5","10%","Yes","Physical","anim_power_strike","Sword Equipped","Deals 150% damage","A basic sword attack.","A powerful blow with a sword."])
            writer.writerow(["Sword Passives", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Rarity","Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effect","Additional Notes","Description"])
            writer.writerow(["Blade Reaver","Rare","Passive","Null","Null","Null","Null","Null","Null","Null","Null","Null","Null","Sword Equipped","Crit Chance +5% with swords.","","Increases critical hit chance with swords."])
            writer.writerow(["Light Spells", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Rarity","Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effect","Additional Notes","Description"])
            writer.writerow(["Heal","Common","Active","1 Ally","10 MP","Healing","Light","Battle","MATK*1.2","5%","No","Certain Hit","anim_heal","","Restores HP.","Basic healing.","Restores a small amount of HP to an ally."])
            writer.writerow(["Fire Spells", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            writer.writerow(["Name","Rarity","Type","Scope","Cost","Dmg Type","Element","Occasion","Formula","Variance","Critical","Hit Type","Animation","Requirement","Effect","Additional Notes","Description"])
            writer.writerow(["Fireball","Common","Active","1 Enemy","8 MP","Magical","Fire","Battle","MATK*1.8","10%","Yes","Magical","anim_fireball","","Deals fire damage.","","Hurls a ball of fire at an enemy."])

    print(f"Attempting to load skills from: {os.path.abspath(csv_file_path)}")
    try:
        loaded_skills = load_skills_from_csv(csv_file_path)
        print(f"\nTotal skills loaded: {len(loaded_skills)}")

        skills_to_verify = {
            "Power Strike": Ability, 
            "Blade Reaver": PassiveSkill, 
            "Heal": Spell,
            "Fireball": Spell
        }

        for skill_name, expected_type in skills_to_verify.items():
            if skill_name in loaded_skills:
                skill = loaded_skills[skill_name]
                print(f"\n--- Details for {skill_name} (Type: {type(skill).__name__}) ---")
                print(f"  Name: {skill.name}, Rarity: {skill.skill_rarity}, Category: {skill.category}")
                print(f"  Description: {skill.description}")
                print(f"  CSV Type: {skill.skill_type_csv}")
                if isinstance(skill, Ability): # Also covers Spells
                    print(f"  Cost: {skill.cost}, Scope: {skill.scope}, Element: {skill.element}")
                    print(f"  Formula: {skill.formula}")
                    print(f"  Effects (CSV): {skill.effects_csv}")
                elif isinstance(skill, PassiveSkill):
                    print(f"  Effects (CSV): {skill.effects_csv}")
            else:
                print(f"\nSkill '{skill_name}' not found in loaded skills.")
                # This might happen if the dummy CSV creation logic is not perfect or full CSV is used
                if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) < 200: # Small heuristic for dummy
                     print(f"  (Note: This might be due to using a minimal dummy CSV for testing.)")


    except FileNotFoundError:
        print(f"Error: The skills CSV file was not found at '{csv_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred during skill loading: {e}")

    print("\nSkill loading test finished.")
