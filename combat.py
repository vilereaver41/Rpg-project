import random
from player import Player # Assuming player.py is in the same directory
from enemy import Enemy   # Import the new Enemy class

def calculate_hit(attacker_accuracy: float, defender_evasion: float) -> bool:
    """
    Calculates if an attack hits based on accuracy and evasion.
    Hit Chance = Attacker's Accuracy - Defender's Evasion.
    Clamped between 5% and 95%.
    """
    hit_chance = attacker_accuracy - defender_evasion
    effective_hit_chance = max(5.0, min(hit_chance, 95.0))
    roll = random.uniform(0, 100)
    # print(f"Accuracy: {attacker_accuracy}, Evasion: {defender_evasion}, Effective Hit Chance: {effective_hit_chance}, Roll: {roll}") # Debug
    if roll <= effective_hit_chance:
        return True
    return False

def combat_attack(attacker, defender):
    """
    Handles the attack action from attacker to defender.
    `attacker` and `defender` can be Player or Enemy objects.
    """
    attacker_name = attacker.get_name()
    defender_name = defender.get_name()
    
    # Attacker stops defending if they choose to attack.
    # This applies to both Player and the new Enemy class, as both have reset_defense()
    attacker.reset_defense()

    print(f"\n{attacker_name} attacks {defender_name}...")

    if not calculate_hit(attacker.get_accuracy(), defender.get_evasion()):
        print(f"{attacker_name}'s attack MISSED {defender_name}!")
        return

    # Calculate base damage using base defense
    damage = attacker.get_attack_power() - defender.get_defense()

    # Critical Hit Check
    crit_roll = random.uniform(0, 100)
    is_critical = False
    if crit_roll <= attacker.get_critical_hit_chance():
        is_critical = True
        damage = int(damage * 1.5) # 1.5x damage for critical hits
        print("It's a CRITICAL HIT!")

    # Ensure damage is at least 1 if the attack hits (before defense reduction)
    damage = max(1, damage)
    
    # Defender's take_damage method will handle damage reduction if they are defending
    # and will also reset their is_defending flag.
    # This applies to both Player and the new Enemy class.
    print(f"{attacker_name} hits {defender_name} (pre-defense reduction damage: {damage})!")
    defender.take_damage(damage)


def start_battle(player: Player, enemy: Enemy): # Type hint for enemy is now enemy.Enemy
    """
    Manages a turn-based battle between a player and an enemy.
    """
    print(f"\n--- Battle Start: {player.get_name()} vs {enemy.get_name()} ---")
    turn = 1

    # Ensure both combatants start fresh, not defending from a previous state.
    player.reset_defense()
    enemy.reset_defense()

    while player.get_current_hp() > 0 and enemy.get_current_hp() > 0:
        print(f"\n--- Turn {turn} ---")
        print(f"{player.get_name()}: {player.get_current_hp()}/{player.get_max_hp()} HP (Defending: {player.is_defending}) | {enemy.get_name()}: {enemy.get_current_hp()}/{enemy.get_max_hp()} HP (Defending: {enemy.is_defending})")

        # --- Player's turn ---
        player_action = ""
        # Player automatically stops defending at the start of their turn if they were defending,
        # unless they choose to defend again. Attacking also stops defense (handled in combat_attack).
        # player.reset_defense() # Moved to combat_attack for attacker, and take_damage for defender

        while player_action not in ["1", "2"]:
            action_prompt = "Player's action: (1) Attack (2) Defend"
            player_action = input(action_prompt + "\nChoose action: ")

        if player_action == "1": # Attack
            combat_attack(player, enemy)
        elif player_action == "2": # Defend
            player.start_defending()

        if not enemy.is_alive(): # Use is_alive() method
            print(f"\n{enemy.get_name()} was defeated!")
            player.gain_xp(enemy.xp_reward)
            break # End battle

        # --- Enemy's turn ---
        if enemy.is_alive(): # Use is_alive() method
            # Enemy AI:
            # - If already defending, it will attack (reset_defense is called in combat_attack).
            # - If HP < 25% and not defending, 60% chance to defend.
            # - Otherwise, 20% chance to defend.
            
            enemy_choice = "attack" # Default action
            critically_low_hp = enemy.get_current_hp() < (enemy.get_max_hp() * 0.25)
            
            if enemy.is_defending: # If was defending, must attack now (reset_defense in combat_attack handles this)
                enemy_choice = "attack"
            elif critically_low_hp:
                if random.random() < 0.60: # 60% chance to defend if low HP
                    enemy_choice = "defend"
            elif random.random() < 0.20: # 20% chance to defend otherwise
                enemy_choice = "defend"

            if enemy_choice == "attack":
                combat_attack(enemy, player)
            else: # Defend
                enemy.start_defending() # Uses Enemy.start_defending()
        
        if not player.is_alive(): # Now uses Player.is_alive()
            print(f"\n{player.get_name()} was defeated!")
            break # End battle
        
        turn += 1
        if turn > 100: # Safety break for extremely long fights
            print("The battle is taking too long! It ends in a draw.")
            break
            
    # Reset defense status for both after combat ends, regardless of outcome
    player.reset_defense()
    enemy.reset_defense()
    print("--- Battle End ---")
