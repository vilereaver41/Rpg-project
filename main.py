import random
from player import Player
from enemy import Enemy
from combat import start_battle
from items import Weapon, Armor, ItemRarity # Import ItemRarity

def create_random_enemy(player_level: int) -> Enemy:
    """Creates a somewhat scaled enemy based on player level."""
    enemy_types = [
        {"name": "Goblin Scout", "base_hp": 30, "base_atk": 8, "base_def": 4, "base_xp": 20, "acc": 70, "eva": 10, "crit": 5},
        {"name": "Wolf", "base_hp": 40, "base_atk": 10, "base_def": 3, "base_xp": 25, "acc": 75, "eva": 15, "crit": 8},
        {"name": "Bandit Thug", "base_hp": 50, "base_atk": 12, "base_def": 5, "base_xp": 30, "acc": 65, "eva": 5, "crit": 10},
        {"name": "Orc Grunt", "base_hp": 70, "base_atk": 15, "base_def": 8, "base_xp": 50, "acc": 60, "eva": 0, "crit": 12},
    ]
    
    chosen_type = random.choice(enemy_types)
    
    # Scale stats slightly with player level
    level_multiplier = 1 + (player_level -1) / 5.0 # e.g. at level 6, multiplier is 2.0
    
    enemy_hp = int(chosen_type["base_hp"] * level_multiplier)
    enemy_atk = int(chosen_type["base_atk"] * level_multiplier)
    enemy_def = int(chosen_type["base_def"] * level_multiplier)
    enemy_xp = int(chosen_type["base_xp"] * level_multiplier)

    return Enemy(
        name=chosen_type["name"],
        max_hp=enemy_hp,
        attack_power=enemy_atk,
        defense=enemy_def,
        accuracy=chosen_type["acc"],
        evasion=chosen_type["eva"],
        critical_hit_chance=chosen_type["crit"],
        xp_reward=enemy_xp
    )

def game():
    """Main function to run the RPG game."""
    player_name = input("Enter your character's name: ")
    player = Player(name=player_name)

    # Give starting gear
    try:
        starter_sword = Weapon(name="Old Sword", description="A bit rusty but still sharp.", 
                               rarity=ItemRarity.COMMON, attack_bonus=3, strength_bonus=1)
        starter_vest = Armor(name="Leather Vest", description="Simple leather protection.", 
                             rarity=ItemRarity.COMMON, equip_slot="chest", defense_bonus=2, max_hp_bonus=5)
        
        player.add_item_to_inventory(starter_sword)
        player.equip(starter_sword)
        player.add_item_to_inventory(starter_vest)
        player.equip(starter_vest)
    except Exception as e:
        print(f"Error giving starting gear: {e}")


    print(f"\nWelcome, {player.name}!")
    player.display_stats()

    game_round = 1
    while True:
        print(f"\n--- Round {game_round} ---")
        
        # Create a new enemy for each fight
        current_enemy = create_random_enemy(player.get_level())
        print(f"\nA wild {current_enemy.get_name()} (Lvl ~{player.get_level()}) appears!")
        print(f"{current_enemy.get_name()} - HP: {current_enemy.get_max_hp()}, ATK: {current_enemy.get_attack_power()}, DEF: {current_enemy.get_defense()}")


        start_battle(player, current_enemy)

        if player.is_alive():
            print(f"\nCongratulations! You defeated the {current_enemy.get_name()}!")
            # XP and level up are handled within player.gain_xp() called by start_battle
            player.display_stats() # Show updated stats

            # Heal player slightly after a win (e.g. 25% of max HP and MP)
            heal_hp_amount = player.get_max_hp() // 4
            heal_mp_amount = player.get_max_mp() // 4
            player.current_hp = min(player.get_max_hp(), player.get_current_hp() + heal_hp_amount)
            player.current_mp = min(player.get_max_mp(), player.get_current_mp() + heal_mp_amount)
            print(f"{player.name} healed for {heal_hp_amount} HP and {heal_mp_amount} MP.")
            print(f"Current HP: {player.current_hp}/{player.get_max_hp()}, MP: {player.current_mp}/{player.get_max_mp()}")

        else:
            print("\n--- You have been defeated. Game Over. ---")
            break # End game

        choice = input("\nDo you want to fight another enemy? (y/n): ").lower()
        if choice != 'y':
            break
        game_round += 1

    print("\nThanks for playing!")
