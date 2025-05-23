from core.player import Player
from core.enemy import Enemy
from core.combat import start_combat
from core.item import Item # Imported as requested, though not actively used in this loop

def main():
    """
    Main function to run the RPG game.
    """
    player_name = input("Enter your character's name: ")
    player = Player(player_name)

    print(f"\nWelcome, {player.name}, to this basic RPG adventure!")

    while True:
        print("\n" + "="*30)
        print(f"HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp} | Level: {player.level}")
        print("="*30)
        print("\nChoose an action:")
        print("1. View Stats")
        print("2. Fight an Enemy")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ").strip()

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
            # For simplicity, create a new enemy each time
            # In a more complex game, you might have predefined enemies or enemy generation
            enemy = Enemy(name="Goblin", hp=30, attack_power=8, defense=2)
            print(f"\nYou encounter a {enemy.name}!")
            
            start_combat(player, enemy)

            if player.hp <= 0:
                print("\nGame Over. Thank you for playing!")
                break # Exit the main game loop

        elif choice == "3":
            print("\nThank you for playing!")
            break # Exit the main game loop

        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")

if __name__ == '__main__':
    main()
