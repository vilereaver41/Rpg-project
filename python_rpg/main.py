# This is the main file for the RPG game.
from game_core.player import Player
from game_core.monster import Monster
from utils.input_helpers import get_non_empty_string

def main():
    """Main function to run the RPG game."""
    print("Welcome to the Python RPG!")

    # player_name = get_non_empty_string("Enter your character's name: ") # Input disabled for non-interactive environment
    player_name = "Hero" # Hardcoded for non-interactive testing
    player = Player(player_name)

    print("\n--- Your Character ---")
    print(player)

    # Create a monster for combat - Adjusted stats for new player system
    monster = Monster(name="Training Dummy", hp=20, attack_power=6, defense=3, xp_reward=10, gold_reward=0)
    print(f"\nA wild {monster.name} appears! {monster}")

    # Combat Loop
    while player.is_alive() and monster.is_alive():
        print("\n--- Combat Status ---")
        print(player)
        print(monster)
        print("---------------------")

        # action = get_non_empty_string("Choose action: (attack / run): ").lower() # Input disabled
        # For testing, let's script the first few actions
        if monster.hp > 10 : # Attack if monster has decent HP
             action = "attack"
             print(f"Action chosen: {action}")
        else: # Then try to run
             action = "run"
             print(f"Action chosen: {action}")


        if action == "attack":
            player_defeated_monster = player.attack_target(monster)
            if player_defeated_monster: # or not monster.is_alive()
                print(f"{monster.name} defeated!")
                player.add_xp(monster.xp_reward)
                break

            if monster.is_alive(): # Monster attacks back if not defeated by player
                print(f"\n{monster.name} attacks {player.name}!")
                # For simplicity, monster's attack is direct damage, not using an attack_target method
                player_took_fatal_damage = player.take_damage(monster.attack_power)
                if player_took_fatal_damage: # or not player.is_alive()
                    # Defeat message is printed by player.take_damage()
                    # print(f"{player.name} has been defeated by {monster.name}! Game Over.")
                    break
        
        elif action == "run":
            print(f"{player.name} safely retreats from the {monster.name}.")
            break
        else:
            print("Invalid action. Try 'attack' or 'run'.") # Should not happen with hardcoded actions

    # After combat loop
    print("\n--- Combat Ended ---")
    if not player.is_alive():
        print("You have fallen in battle.")
    elif not monster.is_alive():
        print("Victory! You stand triumphant.")
    else: # Ran away or other conditions
        print("The dust settles.")


if __name__ == "__main__":
    main()
