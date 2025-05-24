import os
import sys

# Ensure the 'rpg_game' directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpg_game.data.game_data_manager import GameDataManager

if __name__ == '__main__':
    print("Attempting to load actual game data using GameDataManager...")
    
    data_manager = GameDataManager()
    
    # Call load_all_data, relying on its default base_csv_path="Game Csv Data"
    # This assumes "Game Csv Data" exists at the root of the repository where
    # this script or the overall execution context is based.
    data_manager.load_all_data() 
    
    print("\n--- Data Loading Summary (from load_actual_data.py) ---")
    print(f"Total Enemies Loaded: {len(data_manager.enemies)}")
    if data_manager.enemies:
        # Check a sample enemy for linked data, if any were loaded
        # For example, pick the first one by iteration if names are unknown
        sample_enemy_name = next(iter(data_manager.enemies))
        sample_enemy = data_manager.enemies[sample_enemy_name]
        print(f"  Sample Enemy '{sample_enemy_name}':")
        if sample_enemy.abilities_spells:
            print(f"    Abilities: {[s.name for s in sample_enemy.abilities_spells if s is not None]} (linked: {sum(1 for s in sample_enemy.abilities_spells if s is not None)}/{len(sample_enemy.abilities_spells)})")
        else:
            print(f"    Abilities: None or empty list.")
        if sample_enemy.loot:
            print(f"    Loot: {[i.name for i in sample_enemy.loot if i is not None]} (linked: {sum(1 for i in sample_enemy.loot if i is not None)}/{len(sample_enemy.loot)})")
        else:
            print(f"    Loot: None or empty list.")


    print(f"Total Equipment Loaded: {len(data_manager.equipment)}")
    print(f"Total Consumables Loaded: {len(data_manager.consumables)}")
    print(f"Total Materials Loaded: {len(data_manager.materials)}")
    print(f"Total Weapons Loaded: {len(data_manager.weapons)}")
    print(f"Total Skills Loaded: {len(data_manager.skills)}")
    print(f"Total Status Effects Loaded: {len(data_manager.status_effects)}")
    print(f"Total Items in all_items: {len(data_manager.all_items)}")
    
    print("\nActual data loading process finished.")
