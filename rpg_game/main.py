from core.player import Player
from core.enemy import Enemy
from core.combat import start_combat
from core.item import Item # Imported as requested, though not actively used in this loop
from data.game_data_manager import GameDataManager # Added import

def main():
    """
    Main function to run the RPG game.
    """
    print("Loading all game data, please wait...")
    data_manager = GameDataManager()
    data_manager.load_all_data() # Uses default CSV path "Game Csv Data/"
    # Optional: Add a check here if data loading failed critically,
    # for example, if data_manager.enemies is empty, print an error and exit.
    if not data_manager.enemies or not data_manager.all_items:
        print("ERROR: Critical game data (enemies or items) could not be loaded. Exiting.")
        return # Exit the main function
    print("Game data loaded successfully!")

    player_name = input("Enter your character's name: ")
    player = Player(player_name)

    print(f"\nWelcome, {player.name}, to this basic RPG adventure!")

    # Grant starting items and skills
    print("\n--- Granting Starting Equipment and Skills ---")
    # Grant Starting Weapon
    starting_weapon = data_manager.get_item("Iron Sword")
    if starting_weapon:
        player.add_item_to_inventory(starting_weapon)
        print(f"{player.name} starts with an {starting_weapon.name}!")
    else:
        print("Warning: Starting weapon 'Iron Sword' not found in game data.")

    # Grant Starting Armor
    starting_armor = data_manager.get_item("Leather Cap")
    if starting_armor:
        player.add_item_to_inventory(starting_armor)
        print(f"{player.name} equipped with a {starting_armor.name}!") # Assuming equip logic is part of add or separate
    else:
        print("Warning: Starting armor 'Leather Cap' not found.")

    # Grant Starting Skills/Abilities
    basic_attack_skill = data_manager.get_skill("Attack (Base Attack)")
    if basic_attack_skill:
        player.learn_skill(basic_attack_skill)
    else:
        print("Warning: Basic attack skill 'Attack (Base Attack)' not found.")

    power_strike_skill = data_manager.get_skill("Power Strike")
    if power_strike_skill:
        player.learn_skill(power_strike_skill)
    else:
        print("Warning: Skill 'Power Strike' not found.")
        
    # Grant Starting Spell
    heal_spell = data_manager.get_skill("Heal")
    if heal_spell:
        player.learn_skill(heal_spell)
    else:
        print("Warning: Spell 'Heal' not found.")
    print("--- Starting Setup Complete ---")


    # Example: Retrieve a specific enemy if needed later
    # sample_goblin_from_manager = data_manager.get_enemy("Goblin") # Assuming "Goblin" is a key

    while True:
        print("\n" + "="*30)
        print(f"HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp} | Level: {player.level}")
        print("="*30)
        print("\nChoose an action:")
        print("1. View Stats")
        print("2. View Inventory")
        print("3. View Skills")
        print("4. Fight an Enemy")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Your Stats ---")
            print(f"Name: {player.name}")
            print(f"Level: {player.level}")
            print(f"XP: {player.xp}/{player.xp_to_next_level}")
            print(f"HP: {player.hp}/{player.max_hp}")
            print(f"MP: {player.mp}/{player.max_mp}")
            print("\nPrimary Stats:")
            for stat, value in player.stats.items():
                print(f"  {stat.capitalize()}: {value}")
            print("\nDerived Stats:")
            for stat, value in player.derived_stats.items():
                if isinstance(value, float):
                    print(f"  {stat.replace('_', ' ').capitalize()}: {value:.2%}") # Format percentages
                else:
                    print(f"  {stat.replace('_', ' ').capitalize()}: {value}")
            print("--- End Stats ---")

        elif choice == "2":
            player.view_inventory()
            
        elif choice == "3":
            player.view_skills()

        elif choice == "4":
            available_enemy_names = list(data_manager.enemies.keys())
            if not available_enemy_names:
                print("No enemies loaded! Perhaps check the CSV files or loading paths.")
                continue # Go back to the main menu

            print("\nChoose an enemy to fight:")
            display_limit = min(10, len(available_enemy_names)) 
            
            if display_limit == 0 : # Should be caught by the check above, but defensive
                print("No enemies available to display for fighting.")
                continue

            for i, name in enumerate(available_enemy_names[:display_limit]):
                enemy_obj_preview = data_manager.get_enemy(name)
                if enemy_obj_preview:
                    zone_display = enemy_obj_preview.zone_name if enemy_obj_preview.zone_name else 'N/A'
                    level_display = enemy_obj_preview.level_range if hasattr(enemy_obj_preview, 'level_range') else 'N/A'
                    print(f"{i + 1}. {name} (Lvl: {level_display}, Zone: {zone_display})")
                else: # Should not happen if keys are from data_manager.enemies
                    print(f"{i + 1}. {name}")
            
            enemy_choice_str = input(f"Enter your choice (1-{display_limit}), or 0 to cancel: ").strip()

            if not enemy_choice_str: # Empty input
                print("No choice made, returning to menu.")
                continue

            try:
                enemy_choice_num = int(enemy_choice_str)
                if enemy_choice_num == 0:
                    print("Fight cancelled.")
                    continue
                if not (1 <= enemy_choice_num <= display_limit):
                    print("Invalid choice. Please enter a number from the list.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            chosen_enemy_name = available_enemy_names[enemy_choice_num - 1]
            enemy_to_fight = data_manager.get_enemy(chosen_enemy_name)

            if enemy_to_fight:
                print(f"\nYou encounter a {enemy_to_fight.name}!")
                start_combat(player, enemy_to_fight)
            else:
                # This case should ideally not be reached if chosen_enemy_name comes from available_enemy_names
                print(f"Error: Could not find enemy data for {chosen_enemy_name}.")

            if player.hp <= 0:
                print("\nGame Over. Thank you for playing!")
                break # Exit the main game loop

        elif choice == "5":
            print("\nThank you for playing!")
            break # Exit the main game loop

        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == '__main__':
    main()
