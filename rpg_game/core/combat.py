from .player import Player
from .enemy import Enemy

def calculate_damage(attack_power: int, defense: int) -> int:
    """
    Calculates damage dealt after considering defense.
    Ensures damage is at least 1 if the attack hits (attack_power > defense).
    If defense is higher or equal to attack_power, damage is 0.
    """
    damage = attack_power - defense
    if damage <= 0:
        return 0 # No damage if defense is higher or equal
    return max(1, damage) # Ensures at least 1 damage if attack_power > defense


def start_combat(player: Player, enemy: Enemy):
    """
    Manages a combat encounter between the player and an enemy.

    Args:
        player: The player object.
        enemy: The enemy object.
    """
    print(f"\nA wild {enemy.name} appears!\n")

    turn = 1
    while player.hp > 0 and enemy.is_alive():
        print(f"--- Turn {turn} ---")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP | {enemy.name}: {enemy.hp}/{enemy.max_hp} HP")

        # Player's Turn
        action = ""
        while action != "attack":
            action = input("Choose your action (attack): ").lower().strip()
            if action == "attack":
                # Player attacks enemy
                player_attack_power = player.derived_stats.get('attack_power', 0) # type: ignore
                damage_to_enemy = calculate_damage(player_attack_power, enemy.defense)
                
                actual_damage_dealt = enemy.take_damage(damage_to_enemy)
                print(f"{player.name} attacks {enemy.name} for {actual_damage_dealt} damage.")

                if not enemy.is_alive():
                    print(f"{enemy.name} has been defeated!")
                    break
            else:
                print("Invalid action. Type 'attack'.")
        
        if not enemy.is_alive():
            break # Exit combat loop if enemy is defeated

        # Enemy's Turn
        print(f"\n{enemy.name}'s turn...")
        player_defense = player.derived_stats.get('defense', 0) # type: ignore
        damage_to_player = calculate_damage(enemy.attack_power, player_defense)
        
        actual_damage_taken = player.take_damage(damage_to_player)
        print(f"{enemy.name} attacks {player.name} for {actual_damage_taken} damage.")

        if player.hp <= 0: # Check if player is defeated
            print(f"{player.name} has been defeated! Game Over.")
            break
        
        turn += 1
        print("-" * 20) # Separator for next turn

    # After combat loop
    if player.hp > 0 and not enemy.is_alive():
        print(f"\n--- Victory! ---")
        xp_gained = 50 # Example: Fixed XP for defeating an enemy
        print(f"{player.name} gained {xp_gained} XP.")
        player.gain_xp(xp_gained)
        # Player.gain_xp already prints level up message if it happens
    elif player.hp <= 0:
        print(f"\n--- Defeat ---")
        # Game over logic would typically be handled by the main game loop

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    # Initialize a player
    test_player = Player("Hero")
    test_player.stats['strength'] = 15 # Boost strength for more damage
    test_player.stats['constitution'] = 12
    test_player._calculate_derived_stats()
    test_player.hp = test_player.max_hp # Heal to full
    
    print(f"Player Initial Stats: HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}, Def {test_player.derived_stats['defense']}")

    # Initialize an enemy
    test_enemy = Enemy("Goblin Grunt", 60, 10, 5)
    print(f"Enemy Initial Stats: HP {test_enemy.hp}/{test_enemy.max_hp}, Atk {test_enemy.attack_power}, Def {test_enemy.defense}")

    # Start combat
    start_combat(test_player, test_enemy)

    print("\n--- Combat Finished ---")
    print(f"{test_player.name}'s final status:")
    print(f"Level: {test_player.level}, XP: {test_player.xp}/{test_player.xp_to_next_level}")
    print(f"HP: {test_player.hp}/{test_player.max_hp}")

    # Test with a stronger enemy where player might lose
    if test_player.hp > 0: # Only if player survived previous fight
        print("\n--- Next Fight (Stronger Enemy) ---")
        test_player.hp = test_player.max_hp # Heal player
        strong_enemy = Enemy("Orc Warlord", 150, 25, 15)
        print(f"Player Initial Stats: HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}, Def {test_player.derived_stats['defense']}")
        print(f"Enemy Initial Stats: HP {strong_enemy.hp}/{strong_enemy.max_hp}, Atk {strong_enemy.attack_power}, Def {strong_enemy.defense}")
        start_combat(test_player, strong_enemy)

        print("\n--- Combat Finished ---")
        print(f"{test_player.name}'s final status:")
        print(f"Level: {test_player.level}, XP: {test_player.xp}/{test_player.xp_to_next_level}")
        print(f"HP: {test_player.hp}/{test_player.max_hp}")

    # Test scenario where player attack power is less than enemy defense
    print("\n--- Next Fight (High Defense Enemy) ---")
    if test_player.hp > 0:
        test_player.hp = test_player.max_hp # Heal player
    else: # Revive player for this test if defeated
        test_player.level = 1
        test_player.xp = 0
        test_player.stats = {'strength': 5, 'dexterity': 10, 'intelligence': 10, 'constitution': 10, 'luck': 5}
        test_player.xp_to_next_level = 100
        test_player._calculate_derived_stats()
        test_player.hp = test_player.max_hp
        print(f"Player revived and stats reset for testing. HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}")


    high_defense_enemy = Enemy("Iron Golem", 100, 5, 20) # Player Atk (e.g. 10) < Golem Def (20)
    print(f"Player Initial Stats: HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}, Def {test_player.derived_stats['defense']}")
    print(f"Enemy Initial Stats: HP {high_defense_enemy.hp}/{high_defense_enemy.max_hp}, Atk {high_defense_enemy.attack_power}, Def {high_defense_enemy.defense}")
    start_combat(test_player, high_defense_enemy)
    print("\n--- Combat Finished ---")

```
