from .player import Player
from .enemy import Enemy
from .item import Item # Added import for Item
from .skill import Skill, Ability, Spell # Added imports for skill types
import random # Added import for random

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
        player_action_taken = False
        while not player_action_taken:
            print("\nPlayer's turn. Choose an action:")
            print("1. Attack (Basic)")
            print("2. Use Skill/Spell")
            # print("3. View Inventory (Not implemented in combat)") # Skipping for now
            print("4. Flee (Not implemented)")
            
            action_choice = input("Enter your choice: ").lower().strip()

            if action_choice == "1": # Basic Attack
                player_attack_power = player.derived_stats.get('attack_power', player.stats['strength']) 
                damage_to_enemy = calculate_damage(player_attack_power, enemy.defense)
                actual_damage_dealt = enemy.take_damage(damage_to_enemy)
                print(f"{player.name} attacks {enemy.name} for {actual_damage_dealt} damage.")
                player_action_taken = True
            elif action_choice == "2": # Use Skill/Spell
                all_learnable_skills: list[Skill] = [] # Use base Skill for the list type
                all_learnable_skills.extend(player.known_abilities)
                all_learnable_skills.extend(player.known_spells)

                if not all_learnable_skills:
                    print("You don't know any skills or spells!")
                    continue # Go back to action choice

                print("\nAvailable Skills/Spells:")
                for i, skill in enumerate(all_learnable_skills):
                    skill_type_display = "Ability"
                    if isinstance(skill, Spell):
                        skill_type_display = "Spell"
                    cost_display = skill.cost if hasattr(skill, 'cost') and skill.cost else "N/A"
                    print(f"{i + 1}. {skill.name} ({skill_type_display}) - Cost: {cost_display}")
                
                skill_choice_str = input(f"Choose a skill/spell (1-{len(all_learnable_skills)}) or 0 to go back: ").strip()
                try:
                    skill_choice_num = int(skill_choice_str)
                    if skill_choice_num == 0:
                        continue # Go back to action choice
                    if 1 <= skill_choice_num <= len(all_learnable_skills):
                        chosen_skill = all_learnable_skills[skill_choice_num - 1]
                        print(f"{player.name} uses {chosen_skill.name}!")
                        if chosen_skill.description:
                            print(f"> {chosen_skill.description}")
                        
                        # Simulated Effect
                        if isinstance(chosen_skill, Ability) and hasattr(chosen_skill, 'dmg_type') and chosen_skill.dmg_type == "Hp Damage":
                            # Simplified damage for skill, can be expanded with formula
                            player_base_attack = player.derived_stats.get('attack_power', player.stats['strength'])
                            # Example: skill adds +5 to base attack for calculation, or uses a multiplier
                            skill_modified_attack = player_base_attack + 5 # Simple modifier
                            damage = calculate_damage(skill_modified_attack, enemy.defense)
                            enemy.take_damage(damage)
                            print(f"{chosen_skill.name} hits {enemy.name} for {damage} damage.")
                        elif isinstance(chosen_skill, Spell): # Basic placeholder for spells
                            # Example: Spell uses magic_power, could have different effects
                            if hasattr(chosen_skill, 'dmg_type') and chosen_skill.dmg_type == "Hp Damage": # Offensive spell
                                player_magic_power = player.derived_stats.get('magic_power', player.stats['intelligence'])
                                # Example: spell adds +3 to magic power for calculation
                                spell_modified_attack = player_magic_power + 3
                                damage = calculate_damage(spell_modified_attack, enemy.magic_defense if hasattr(enemy, 'magic_defense') else enemy.defense) # Target magic defense if available
                                enemy.take_damage(damage)
                                print(f"{chosen_skill.name} magically strikes {enemy.name} for {damage} damage.")
                            else: # Non-damaging spell or other type
                                print(f"{chosen_skill.name} affects {enemy.name} with a mystical energy!")
                        else: # For other skill types or non-damaging abilities
                            print(f"{chosen_skill.name} is activated!")
                        
                        # (MP/TP cost deduction not implemented yet)
                        player_action_taken = True
                    else:
                        print("Invalid skill choice.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif action_choice == "4": # Flee
                print("Fleeing is not implemented yet.")
                # player_action_taken = True # Or set to False to re-prompt if flee fails
            else:
                print("Invalid action. Choose from the available options.")

            if enemy.is_alive() and player_action_taken: # Check if enemy is still alive after player's action
                # Enemy's Turn
                print(f"\n{enemy.name}'s turn...")
                if enemy.abilities_spells and random.random() < 0.5: # 50% chance to use a skill if available
                    chosen_enemy_skill = random.choice(enemy.abilities_spells)
                    print(f"{enemy.name} uses {chosen_enemy_skill.name}!")
                    if chosen_enemy_skill.description:
                        print(f"> {chosen_enemy_skill.description}")
                    
                    # Simplified effect for enemy skill
                    if isinstance(chosen_enemy_skill, Ability) and hasattr(chosen_enemy_skill, 'dmg_type') and chosen_enemy_skill.dmg_type == "Hp Damage":
                        base_enemy_attack = enemy.magic_attack if hasattr(enemy, 'magic_attack') and enemy.magic_attack > enemy.attack_power else enemy.attack_power
                        # Example: skill adds +2 to enemy base attack
                        enemy_skill_modified_attack = base_enemy_attack + 2
                        damage_to_player = calculate_damage(enemy_skill_modified_attack, player.derived_stats.get('defense', 0))
                        player.take_damage(damage_to_player)
                        print(f"{chosen_enemy_skill.name} hits {player.name} for {damage_to_player} damage.")
                    elif isinstance(chosen_enemy_skill, Spell): # Basic placeholder for spells
                        if hasattr(chosen_enemy_skill, 'dmg_type') and chosen_enemy_skill.dmg_type == "Hp Damage":
                            enemy_magic_power = enemy.magic_attack if hasattr(enemy, 'magic_attack') else enemy.attack_power
                            enemy_spell_modified_attack = enemy_magic_power + 2
                            damage_to_player = calculate_damage(enemy_spell_modified_attack, player.derived_stats.get('magic_defense', player.derived_stats.get('defense',0))) # Target MDEF if player has it
                            player.take_damage(damage_to_player)
                            print(f"{chosen_enemy_skill.name} magically strikes {player.name} for {damage_to_player} damage.")
                        else:
                            print(f"{chosen_enemy_skill.name} affects {player.name} with a strange power!")
                    else:
                        print(f"{chosen_enemy_skill.name} is used by {enemy.name}!")
                else:
                    # Basic attack (existing logic)
                    player_defense = player.derived_stats.get('defense', 0) 
                    damage_to_player = calculate_damage(enemy.attack_power, player_defense)
                    actual_damage_taken = player.take_damage(damage_to_player)
                    print(f"{enemy.name} attacks {player.name} for {actual_damage_taken} damage.")

        if not enemy.is_alive():
            print(f"{enemy.name} has been defeated!") # Moved this message to after player's turn if enemy defeated by player
            break 
            
        if player.hp <= 0: # Check if player is defeated
            print(f"{player.name} has been defeated! Game Over.")
            break
        
        turn += 1
        print("-" * 20) # Separator for next turn

    # After combat loop
    if player.hp > 0 and not enemy.is_alive():
        print(f"\n--- Victory! ---")
        # Loot drops logic added here, before XP gain
        print(f"The {enemy.name} has been defeated!") # Already printed inside loop, but good for clarity here too or remove from loop.
                                                 # The prompt asked for it here.
        if enemy.loot:
            print(f"The {enemy.name} dropped:")
            for item_obj in enemy.loot:
                print(f"- {item_obj.name}")
                player.add_item_to_inventory(item_obj) # Assumes player has this method
        else:
            print(f"The {enemy.name} dropped nothing.")

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
    # Mock Skill and Item classes for standalone testing if real ones are complex to init here
    class MockSkill(Skill): # Using base Skill for simplicity in __main__
        def __init__(self, name, description="A mock skill.", skill_rarity="Common", skill_type_csv="Active", category="Test", dmg_type="Hp Damage", cost="0"):
            super().__init__(name, description, skill_rarity, skill_type_csv, category)
            self.dmg_type = dmg_type # Add dmg_type for testing effect
            self.cost = cost

    class MockAbility(Ability): # Using Ability for testing
         def __init__(self, name, description="A mock ability.", skill_rarity="Common", skill_type_csv="Active", category="Test", dmg_type="Hp Damage", cost="0 MP"):
            super().__init__(name, description, skill_rarity, skill_type_csv, category, dmg_type=dmg_type, cost=cost)

    class MockSpell(Spell): # Using Spell for testing
         def __init__(self, name, description="A mock spell.", skill_rarity="Common", skill_type_csv="Active", category="Test", dmg_type="Hp Damage", cost="0 MP"):
            super().__init__(name, description, skill_rarity, skill_type_csv, category, dmg_type=dmg_type, cost=cost)


    class MockItem(Item):
        def __init__(self, name, description="A mock item"):
            super().__init__(name, description)

    mock_loot_item1 = MockItem("Goblin Ear")
    mock_loot_item2 = MockItem("Rusty Coin")
    
    # Give player some skills
    player_power_strike = MockAbility(name="Power Strike", description="A strong hit.", cost="5 TP", dmg_type="Hp Damage")
    player_heal_spell = MockSpell(name="Minor Heal", description="Heals a bit.", cost="10 MP", dmg_type="Healing") # Non-Hp Damage type
    test_player.learn_skill(player_power_strike)
    test_player.learn_skill(player_heal_spell)
    
    # Give enemy some skills
    enemy_bash_skill = MockAbility(name="Goblin Bash", description="A clumsy bash.", cost="0", dmg_type="Hp Damage")
    enemy_weak_spell = MockSpell(name="Weak Curse", description="A weak curse.", cost="0", dmg_type="Debuff") # Non-Hp Damage

    test_enemy = Enemy(name="Goblin Grunt", max_hp=60, attack_power=10, defense=5,
                       level_range="1-2", spawn_chance="Common", enemy_type="Goblinoid",
                       max_mp=0, magic_attack=8, magic_defense=2, agility=3, luck=1,
                       has_sprite=False, abilities_spells=[enemy_bash_skill, enemy_weak_spell], 
                       loot=[mock_loot_item1, mock_loot_item2])
    print(f"Enemy Initial Stats: HP {test_enemy.hp}/{test_enemy.max_hp}, Atk {test_enemy.attack_power}, Def {test_enemy.defense}")
    print(f"Enemy Skills: {[s.name for s in test_enemy.abilities_spells]}")
    print(f"Enemy Loot Table: {[item.name for item in test_enemy.loot]}")

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
        strong_enemy_loot = [MockItem("Orc Tusk")]
        strong_enemy = Enemy(name="Orc Warlord", max_hp=150, attack_power=25, defense=15,
                             level_range="5-7", spawn_chance="Rare", enemy_type="Orcish",
                             max_mp=10, magic_attack=5, magic_defense=5, agility=5, luck=3,
                             has_sprite=True, abilities_spells=[], loot=strong_enemy_loot)
        print(f"Player Initial Stats: HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}, Def {test_player.derived_stats['defense']}")
        print(f"Enemy Initial Stats: HP {strong_enemy.hp}/{strong_enemy.max_hp}, Atk {strong_enemy.attack_power}, Def {strong_enemy.defense}")
        print(f"Enemy Loot Table: {[item.name for item in strong_enemy.loot]}")
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


    high_defense_enemy = Enemy(name="Iron Golem", max_hp=100, attack_power=5, defense=20, # Player Atk (e.g. 10) < Golem Def (20)
                               level_range="8-10", spawn_chance="Uncommon", enemy_type="Construct",
                               max_mp=0, magic_attack=0, magic_defense=10, agility=1, luck=0,
                               has_sprite=True, abilities_spells=[], loot=[]) # No loot for this one
    print(f"Player Initial Stats: HP {test_player.hp}/{test_player.max_hp}, Atk {test_player.derived_stats['attack_power']}, Def {test_player.derived_stats['defense']}")
    print(f"Enemy Initial Stats: HP {high_defense_enemy.hp}/{high_defense_enemy.max_hp}, Atk {high_defense_enemy.attack_power}, Def {high_defense_enemy.defense}")
    print(f"Enemy Loot Table: {[item.name for item in high_defense_enemy.loot]}")
    start_combat(test_player, high_defense_enemy)
    print("\n--- Combat Finished ---")

    # Test player viewing inventory after combat
    test_player.view_inventory()
