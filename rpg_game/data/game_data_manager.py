import os
from typing import Dict, Optional, Union

# Loader function imports (using relative imports as this file is in the 'data' package)
try:
    from .enemy_loader import load_enemies_from_csv
    from .item_loader import load_equipment_from_csv, load_consumables_and_materials_from_csv, load_weapons_from_csv
    from .skill_loader import load_skills_from_csv
    from .status_effect_loader import load_status_effects_from_csv
except ImportError: # Fallback for running script directly for testing, if rpg_game is in PYTHONPATH
    from enemy_loader import load_enemies_from_csv
    from item_loader import load_equipment_from_csv, load_consumables_and_materials_from_csv, load_weapons_from_csv
    from skill_loader import load_skills_from_csv
    from status_effect_loader import load_status_effects_from_csv


# Core class imports for type hinting
try:
    from rpg_game.core.enemy import Enemy
    from rpg_game.core.item import Item
    from rpg_game.core.equipment import Equipment
    from rpg_game.core.consumable import Consumable
    from rpg_game.core.material import Material
    from rpg_game.core.weapon import Weapon
    from rpg_game.core.skill import Skill, Ability, PassiveSkill, Spell
    from rpg_game.core.status_effect import StatusEffect
except ImportError: # Fallback
    # This assumes the script might be run from 'rpg_game/data' or 'rpg_game' is in path
    # Adjusting path to find 'core' if running from 'data'
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Go up to rpg_game directory
    from core.enemy import Enemy
    from core.item import Item
    from core.equipment import Equipment
    from core.consumable import Consumable
    from core.material import Material
    from core.weapon import Weapon
    from core.skill import Skill, Ability, PassiveSkill, Spell
    from core.status_effect import StatusEffect


class GameDataManager:
    """
    Manages loading and accessing all game data from CSV files.
    """
    def __init__(self):
        self.enemies: Dict[str, Enemy] = {}
        self.equipment: Dict[str, Equipment] = {}
        self.consumables: Dict[str, Consumable] = {}
        self.materials: Dict[str, Material] = {}
        self.weapons: Dict[str, Weapon] = {}
        self.skills: Dict[str, Skill] = {} # Holds Abilities, Spells, PassiveSkills
        self.status_effects: Dict[str, StatusEffect] = {}
        
        self.all_items: Dict[str, Item] = {} # Combined for convenience

    def load_all_data(self, base_csv_path: str = "Game Csv Data") -> None:
        """
        Loads all game data from the specified CSV files.
        """
        print(f"Starting data loading process from base path: '{base_csv_path}'...")

        # 1. Load Status Effects
        status_effects_path = os.path.join(base_csv_path, "Buffs & Debuffs.csv")
        print(f"\nLoading status effects from: {status_effects_path}")
        try:
            self.status_effects = load_status_effects_from_csv(status_effects_path)
            print(f"  Loaded {len(self.status_effects)} status effects.")
        except FileNotFoundError:
            print(f"  ERROR: Status effects file not found at {status_effects_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load status effects: {e}")


        # 2. Load Skills
        skills_path = os.path.join(base_csv_path, "Spells & Abilitys.csv")
        print(f"\nLoading skills from: {skills_path}")
        try:
            self.skills = load_skills_from_csv(skills_path)
            print(f"  Loaded {len(self.skills)} skills.")
        except FileNotFoundError:
            print(f"  ERROR: Skills file not found at {skills_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load skills: {e}")


        # 3. Load Equipment (Armor, Accessories, Shields)
        equipment_path = os.path.join(base_csv_path, "Armor, Accesories, Shields.csv")
        print(f"\nLoading equipment from: {equipment_path}")
        try:
            self.equipment = load_equipment_from_csv(equipment_path)
            print(f"  Loaded {len(self.equipment)} pieces of equipment.")
        except FileNotFoundError:
            print(f"  ERROR: Equipment file not found at {equipment_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load equipment: {e}")


        # 4. Load Consumables and Materials
        consumables_materials_path = os.path.join(base_csv_path, "Potions, Consumables, Materials.csv")
        print(f"\nLoading consumables and materials from: {consumables_materials_path}")
        try:
            consumables_and_materials = load_consumables_and_materials_from_csv(consumables_materials_path)
            for name, item_obj in consumables_and_materials.items():
                if isinstance(item_obj, Consumable):
                    self.consumables[name] = item_obj
                elif isinstance(item_obj, Material):
                    self.materials[name] = item_obj
            print(f"  Loaded {len(self.consumables)} consumables.")
            print(f"  Loaded {len(self.materials)} materials.")
        except FileNotFoundError:
            print(f"  ERROR: Consumables/materials file not found at {consumables_materials_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load consumables/materials: {e}")
            

        # 5. Load Weapons
        weapons_path = os.path.join(base_csv_path, "Revised Weapon Sheet.csv")
        print(f"\nLoading weapons from: {weapons_path}")
        try:
            self.weapons = load_weapons_from_csv(weapons_path)
            print(f"  Loaded {len(self.weapons)} weapons.")
        except FileNotFoundError:
            print(f"  ERROR: Weapons file not found at {weapons_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load weapons: {e}")

        # 6. Create self.all_items
        print("\nCombining all item types into 'all_items' dictionary...")
        self.all_items.update(self.equipment)
        self.all_items.update(self.consumables)
        self.all_items.update(self.materials)
        self.all_items.update(self.weapons)
        print(f"  Total items in 'all_items': {len(self.all_items)}.")

        # 7. Load Enemies
        # Note: Enemy linking logic will be added in a subsequent step.
        # For now, it loads enemies but doesn't link their skills/loot yet.
        enemies_path = os.path.join(base_csv_path, "Enemy's Sheet.csv")
        print(f"\nLoading enemies from: {enemies_path}")
        try:
            # Pass self.skills and self.all_items to the enemy loader
            self.enemies = load_enemies_from_csv(enemies_path, self.skills, self.all_items)
            print(f"  Loaded {len(self.enemies)} enemies.")
        except FileNotFoundError:
            print(f"  ERROR: Enemies file not found at {enemies_path}. Skipping.")
        except Exception as e:
            print(f"  ERROR: Failed to load enemies: {e}")
            
        print("\nAll data loading attempted.")

    # Getter Methods
    def get_enemy(self, name: str) -> Optional[Enemy]:
        return self.enemies.get(name)

    def get_item(self, name: str) -> Optional[Item]:
        """Searches for an item in all loaded item categories."""
        return self.all_items.get(name)

    def get_skill(self, name: str) -> Optional[Skill]:
        return self.skills.get(name)

    def get_status_effect(self, name: str) -> Optional[StatusEffect]:
        return self.status_effects.get(name)

if __name__ == '__main__':
    # This block assumes that the script is run from the 'rpg_game/data' directory,
    # or that 'Game Csv Data' is relative to where it's run.
    # For more robust execution, you might want to calculate base_csv_path relative to this file.
    
    # Determine a base path for CSVs, assuming 'Game Csv Data' is at the project root (parent of 'data')
    # If this script is in rpg_game/data/, then ../../Game Csv Data
    # If this script is run from project root, then Game Csv Data
    
    # Simplified: if the script is in 'rpg_game/data', we go up one level to 'rpg_game'
    # then expect 'Game Csv Data' to be a sibling of 'rpg_game' or inside it.
    # For this example, let's assume 'Game Csv Data' is at the same level as the 'rpg_game' package,
    # or directly where the script is run.
    # A common setup is to have a 'data' or 'assets' folder at the project root.
    
    # If running this __main__ directly, it's likely from within rpg_game/data.
    # So, base_csv_path should point to where "Game Csv Data" is relative to that.
    # If "Game Csv Data" is at the project root (e.g. /app/Game Csv Data),
    # and this script is /app/rpg_game/data/game_data_manager.py
    # then the relative path is "../../Game Csv Data"
    
    # However, the loader functions themselves use "Game Csv Data/..." in their main blocks,
    # implying they expect to be run from a context where "Game Csv Data" is a direct subdirectory.
    # Let's use a path that's relative to the project root for consistency with those.
    # Assuming project root is the parent of "rpg_game" dir.
    
    # If this script is rpg_game/data/game_data_manager.py
    # Project root could be parent of rpg_game.
    # For simplicity, let's try a path often used in these sandbox tasks.
    # The task description implies "Game Csv Data" as a top-level dir for CSVs.
    
    # Create dummy CSV files if they don't exist (minimal versions for testing)
    # This is to make the __main__ block runnable without external dependencies.
    # In a real application, these files would be part of the game's assets.
    dummy_csv_base_path = "Game Csv Data" # As specified in load_all_data default
    
    files_to_check_or_create = {
        "Buffs & Debuffs.csv": ["Positive States\nName,Element,Duration,Effect,Notes\nRegen,Light,3 Turns,Heals 10 HP/turn,Good vibes"],
        "Spells & Abilitys.csv": ["Sword Skills\nName,Rarity,Type,,,,,,,,,,,,,,Description\nSlash,Common,Active,,,,,,,,,,,,,,A basic slash"],
        "Armor, Accesories, Shields.csv": ["Armor\nName,,Tier,Recipe,Equip Type,Attack,Defense\nLeather Vest,,Common,,Armor,,5"],
        "Potions, Consumables, Materials.csv": ["Potions\nName,,Effect Notes\nMinor Health Potion,,Restores 10 HP\nRaw Ingriedient\nName,Rarity\nIron Ore,Common"],
        "Revised Weapon Sheet.csv": ["Swords Level 1-50\nName,Level Range,Source,Tier,Attack Type,Attack\nBasic Sword,1-5,Starter,Common,Physical,5"],
        "Enemy's Sheet.csv": ["Name,Level Range,Spawn Chance,Type,Max Hp Lowest Level,Max Mp,Attack,Defense,M.Attack,M.Defense.,Agility,Luck,Has Sprite?,Abilitys & Spells,,Enemy Loot\nGoblin,1-3,Common,Goblinoid,30,0,5,2,0,0,3,1,Yes,Scratch,,Gold Coin"]
    }

    if not os.path.exists(dummy_csv_base_path):
        os.makedirs(dummy_csv_base_path, exist_ok=True)

    for filename, content_lines in files_to_check_or_create.items():
        filepath = os.path.join(dummy_csv_base_path, filename)
        if not os.path.exists(filepath):
            print(f"Creating dummy CSV: {filepath}")
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                # For simplicity, just write lines. CSV writer can be used for more complex dummies.
                for line in content_lines:
                    f.write(line + "\n")
        
    print("--- GameDataManager Test ---")
    data_manager = GameDataManager()
    data_manager.load_all_data(base_csv_path=dummy_csv_base_path) # Use the potentially dummy path

    print("\n--- Sample Data Retrieval ---")
    
    # Try to get an enemy
    sample_enemy_name = "Goblin" # From dummy CSV
    enemy = data_manager.get_enemy(sample_enemy_name)
    if enemy:
        print(f"Found Enemy '{sample_enemy_name}': HP {enemy.max_hp}, Attack {enemy.attack_power}")
    else:
        print(f"Enemy '{sample_enemy_name}' not found.")

    # Try to get an item (e.g., equipment)
    sample_item_name = "Leather Vest" # From dummy CSV
    item = data_manager.get_item(sample_item_name)
    if item:
        print(f"Found Item '{sample_item_name}': {item.description}")
        if isinstance(item, Equipment):
            print(f"  It's Equipment with Defense: {item.defense_bonus}")
    else:
        print(f"Item '{sample_item_name}' not found.")
        
    # Try to get another item (e.g., consumable)
    sample_consumable_name = "Minor Health Potion" # From dummy CSV
    consumable_item = data_manager.get_item(sample_consumable_name)
    if consumable_item:
        print(f"Found Item '{sample_consumable_name}': {consumable_item.description}")
        if isinstance(consumable_item, Consumable):
            print(f"  It's a Consumable of category: {consumable_item.category}, Effect: {consumable_item.effect_description}")
    else:
        print(f"Item '{sample_consumable_name}' not found.")


    # Try to get a skill
    sample_skill_name = "Slash" # From dummy CSV
    skill = data_manager.get_skill(sample_skill_name)
    if skill:
        print(f"Found Skill '{sample_skill_name}': Category {skill.category}, Type {skill.skill_type_csv}")
    else:
        print(f"Skill '{sample_skill_name}' not found.")

    # Try to get a status effect
    sample_status_effect_name = "Regen" # From dummy CSV
    status_effect = data_manager.get_status_effect(sample_status_effect_name)
    if status_effect:
        print(f"Found Status Effect '{sample_status_effect_name}': Type {status_effect.effect_type}, Duration {status_effect.duration_str}")
    else:
        print(f"Status Effect '{sample_status_effect_name}' not found.")

    print("\n--- GameDataManager Test Finished ---")
