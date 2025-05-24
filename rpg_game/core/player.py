from typing import List, Optional # Ensure List and Optional are imported

# Assuming Item, Ability, Spell, Skill will be imported for type hints
# Adjust if Item is in a different relative path or if Skill etc. are in different files
try:
    from .item import Item
    from .skill import Skill, Ability, Spell
except ImportError: # Fallback for running __main__ block or if structure differs
    # This might happen if player.py is run directly for its __main__
    # and the current directory is 'core', so direct imports work.
    from item import Item
    from skill import Skill, Ability, Spell


class Player:
    """
    Represents the player character in the RPG game.
    """
    def __init__(self, name: str):
        """
        Initializes a new player.

        Args:
            name: The name of the player.
        """
        self.name: str = name
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100
        self.hp: int = 100 # Initial HP, will be set by _calculate_derived_stats based on constitution
        self.max_hp: int = 100 # Initial Max HP
        self.mp: int = 50 # Initial MP, will be set by _calculate_derived_stats based on intelligence
        self.max_mp: int = 50 # Initial Max MP
        self.stats: dict[str, int] = {
            'strength': 10,
            'dexterity': 10,
            'intelligence': 10,
            'constitution': 10, # Initial constitution
            'luck': 5,
        }
        self.derived_stats: dict[str, float | int] = {} # Critical hit chance, accuracy, evasion can be float
        
        # Initialize hp and mp based on initial stats
        self._calculate_derived_stats() # Calculate max_hp/max_mp first
        self.hp = self.max_hp # Set current HP to max
        self.mp = self.max_mp # Set current MP to max

        # Inventory and Skills
        self.inventory: List[Item] = []
        self.known_abilities: List[Ability] = []
        self.known_spells: List[Spell] = []


    def _calculate_derived_stats(self):
        """
        Calculates and updates derived stats based on primary stats.
        Also updates max_hp and max_mp.
        """
        self.max_hp = self.stats['constitution'] * 10
        self.max_mp = self.stats['intelligence'] * 5

        # Adjust current HP/MP if they exceed new max values (e.g., after a debuff to constitution)
        # Typically, on level up, HP/MP are fully restored, so this is more for other scenarios.
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        
        self.derived_stats['attack_power'] = self.stats['strength'] * 2
        self.derived_stats['defense'] = int(self.stats['constitution'] * 1.5)
        self.derived_stats['magic_power'] = self.stats['intelligence'] * 2
        self.derived_stats['critical_hit_chance'] = self.stats['luck'] * 0.05 # e.g., 5 luck = 0.25 (25%)
        self.derived_stats['accuracy'] = self.stats['dexterity'] * 0.1 # e.g., 10 dex = 1.0 base accuracy factor
        self.derived_stats['evasion'] = self.stats['dexterity'] * 0.02 # e.g., 10 dex = 0.2 base evasion factor

    def take_damage(self, amount: int) -> int:
        """
        Reduces player's HP by the given amount.

        Args:
            amount: The amount of damage to take.

        Returns:
            The actual amount of damage taken.
        """
        damage_taken = min(amount, self.hp)
        self.hp -= damage_taken
        return damage_taken

    def heal(self, amount: int) -> int:
        """
        Increases player's HP by the given amount.

        Args:
            amount: The amount of HP to restore.

        Returns:
            The actual amount of HP healed.
        """
        amount_to_heal = min(amount, self.max_hp - self.hp)
        self.hp += amount_to_heal
        return amount_to_heal

    def gain_xp(self, amount: int) -> bool:
        """
        Increases player's XP by the given amount and checks for level up.

        Args:
            amount: The amount of XP gained.

        Returns:
            True if the player leveled up at least once, False otherwise.
        """
        if amount <= 0:
            return False
            
        self.xp += amount
        leveled_up_this_gain = False
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            leveled_up_this_gain = True
        return leveled_up_this_gain

    def level_up(self):
        """
        Handles the player leveling up.
        Increases level, stats, resets XP (carries over overflow), 
        increases XP to next level, heals player, and recalculates derived stats.
        """
        self.level += 1
        self.xp -= self.xp_to_next_level 
        self.xp_to_next_level += 50  # Increase XP needed for next level (e.g., simple linear increase)

        # Increase primary stats (fixed increases for now)
        self.stats['strength'] += 2
        self.stats['dexterity'] += 2
        self.stats['intelligence'] += 2
        self.stats['constitution'] += 2
        self.stats['luck'] += 1

        # Recalculate derived stats (which also updates max_hp, max_mp)
        self._calculate_derived_stats()

        # Heal player to full HP and MP on level up
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        print(f"Congratulations! {self.name} reached level {self.level}!")

    def add_item_to_inventory(self, item: Item) -> None:
        """Appends the item to self.inventory."""
        self.inventory.append(item)
        print(f"{item.name} added to inventory.")

    def learn_skill(self, skill: Skill) -> None:
        """Learns a new skill, adding it to the appropriate list."""
        if isinstance(skill, Ability) and not isinstance(skill, Spell): # Ensure it's an Ability but not a Spell
            if skill not in self.known_abilities:
                self.known_abilities.append(skill)
                print(f"{self.name} learned ability: {skill.name}!")
            else:
                print(f"{self.name} already knows the ability: {skill.name}.")
        elif isinstance(skill, Spell):
            if skill not in self.known_spells:
                self.known_spells.append(skill)
                print(f"{self.name} learned spell: {skill.name}!")
            else:
                print(f"{self.name} already knows the spell: {skill.name}.")
        else: # This includes PassiveSkill or any other Skill subclass
            # For now, we are not specifically tracking other skill types like PassiveSkill
            # in separate lists on the Player, but they could be learned conceptually.
            # The prompt only asks for abilities and spells to be added to lists.
            print(f"Cannot specifically categorize skill: {skill.name} of type {type(skill).__name__}. It's a general skill.")


    def view_inventory(self) -> None:
        """Prints the contents of the player's inventory."""
        print("\n--- Inventory ---")
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for i, item_obj in enumerate(self.inventory):
                print(f"{i + 1}. {item_obj.name} - {item_obj.description}")
        print("-----------------")

    def view_skills(self) -> None:
        """Prints the player's known abilities and spells."""
        print("\n--- Skills ---")
        if not self.known_abilities and not self.known_spells:
            print("No skills learned.")
        
        if self.known_abilities:
            print("Abilities:")
            for i, ability in enumerate(self.known_abilities):
                print(f"  {i + 1}. {ability.name} - {ability.description}")
        else:
            print("No abilities learned.")
            
        if self.known_spells:
            print("Spells:")
            for i, spell in enumerate(self.known_spells):
                print(f"  {i + 1}. {spell.name} - {spell.description}")
        else:
            print("No spells learned.")
        print("--------------")


if __name__ == '__main__':
    # Example Usage (for testing purposes)
    player = Player("Hero")
    print(f"Initial Stats for {player.name}:")
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}")
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}")
    print(f"Primary Stats: {player.stats}")
    print(f"Derived Stats: {player.derived_stats}")
    print("-" * 20)

    player.take_damage(30)
    print(f"HP after taking 30 damage: {player.hp}/{player.max_hp}") # Expected: 70/100
    player.heal(20)
    print(f"HP after healing 20: {player.hp}/{player.max_hp}") # Expected: 90/100
    player.heal(100) # Try to heal beyond max
    print(f"HP after healing 100 (max): {player.hp}/{player.max_hp}") # Expected: 100/100
    print("-" * 20)

    print(f"Gaining 50 XP...")
    player.gain_xp(50)
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") # Expected: L1, 50/100 XP
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}")
    print(f"Primary Stats: {player.stats}")
    print(f"Derived Stats: {player.derived_stats}")
    print("-" * 20)

    print(f"Gaining 70 XP (enough to level up)...")
    leveled = player.gain_xp(70) 
    print(f"Leveled up: {leveled}") 
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") 
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}") 
    print(f"Primary Stats: {player.stats}") 
    print(f"Derived Stats: {player.derived_stats}") 
    print("-" * 20)
    
    # --- Test Inventory and Skills ---
    print("\n--- Testing Inventory and Skills ---")
    # Mock objects for testing
    # (Assuming Item, Ability, Spell classes are defined as in previous subtasks)
    # If not, define simple mock classes here for the __main__ block to run
    try:
        # Try to use the actual classes if they are importable and instantiable
        mock_potion = Item("Health Potion", "Restores 20 HP.")
        mock_sword = Item("Iron Sword", "A basic sword.")
        
        mock_power_strike = Ability(name="Power Strike", description="A powerful attack.", skill_rarity="Common", skill_type_csv="Active", category="Combat", cost="5 MP", formula="ATK * 1.5")
        mock_fireball = Spell(name="Fireball", description="Hurls a ball of fire.", skill_rarity="Common", skill_type_csv="Active", category="Elemental Magic", cost="10 MP", element="Fire", formula="MATK * 2")
        # A general skill that is not an Ability or Spell (e.g., could be a PassiveSkill if that class existed and inherited Skill)
        mock_toughness = Skill(name="Toughness", description="Increases HP.", skill_rarity="Uncommon", skill_type_csv="Passive", category="Defense")

    except NameError: # If Item, Skill, Ability, Spell are not defined here (e.g. direct run of player.py)
        print("WARN: Using very basic mocks for Item/Skill in Player __main__")
        class MockItem:
            def __init__(self, name, description=""): self.name = name; self.description = description
        class MockSkill:
            def __init__(self, name, description="", skill_rarity="", skill_type_csv="", category=""): 
                self.name = name; self.description = description; self.skill_rarity = skill_rarity
                self.skill_type_csv = skill_type_csv; self.category = category
        class MockAbility(MockSkill):
            def __init__(self, name, description="", skill_rarity="", skill_type_csv="Active", category="", cost="", formula=""):
                super().__init__(name, description, skill_rarity, skill_type_csv, category)
                self.cost = cost; self.formula = formula
        class MockSpell(MockAbility):
            def __init__(self, name, description="", skill_rarity="", skill_type_csv="Active", category="", cost="", element="", formula=""):
                super().__init__(name, description, skill_rarity, skill_type_csv, category, cost, formula)
                self.element = element
        
        mock_potion = MockItem("Health Potion", "Restores 20 HP.")
        mock_sword = MockItem("Iron Sword", "A basic sword.")
        mock_power_strike = MockAbility(name="Power Strike", description="A powerful attack.", cost="5 MP")
        mock_fireball = MockSpell(name="Fireball", description="Hurls a ball of fire.", cost="10 MP", element="Fire")
        mock_toughness = MockSkill(name="Toughness", description="Increases HP.", skill_type_csv="Passive")


    player.add_item_to_inventory(mock_potion)
    player.add_item_to_inventory(mock_sword)
    
    player.learn_skill(mock_power_strike)
    player.learn_skill(mock_fireball)
    player.learn_skill(mock_toughness) # Test with a generic Skill object

    player.view_inventory()
    player.view_skills()

    print("\nDirectly printing lists:")
    print(f"Inventory: {[(item.name) for item in player.inventory]}")
    print(f"Abilities: {[(ability.name) for ability in player.known_abilities]}")
    print(f"Spells: {[(spell.name) for spell in player.known_spells]}")
    print("--- End Inventory and Skills Test ---")


    # Reset player to Level 1 for multi-level test.
    player.xp = 0
    player.level = 1
    player.stats = {'strength': 10, 'dexterity': 10, 'intelligence': 10, 'constitution': 10, 'luck': 5}
    player.xp_to_next_level = 100
    player._calculate_derived_stats()
    player.hp = player.max_hp
    player.mp = player.max_mp
    print(f"\nReset player to Level 1 for multi-level test. XP: {player.xp}/{player.xp_to_next_level}")
    print(f"Gaining 250 XP (enough for two levels)...")
    leveled = player.gain_xp(250)
    print(f"Leveled up: {leveled}") 
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") 
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}") 
    print(f"Primary Stats: {player.stats}") 
    print(f"Derived Stats: {player.derived_stats}")
    print("-" * 20)

    # Test take_damage to 0
    player.take_damage(player.max_hp + 50) # Take more than max HP
    print(f"HP after taking critical damage: {player.hp}/{player.max_hp}") 
    print("-" * 20)
    player.heal(player.max_hp)
    print(f"HP after healing to max: {player.hp}/{player.max_hp}") 

    # Test derived stat calculation after direct stat modification
    print(f"Constitution before manual change: {player.stats['constitution']}") 
    print(f"Max HP before: {player.max_hp}") 
    print(f"Defense before: {player.derived_stats['defense']}") 
    player.stats['constitution'] += 10 # Manually increase constitution
    player._calculate_derived_stats() # Recalculate
    print(f"Updated Constitution: {player.stats['constitution']}") 
    print(f"Updated Max HP: {player.max_hp}") 
    print(f"Updated Defense: {player.derived_stats['defense']}") 
    print(f"Current HP: {player.hp}/{player.max_hp}") 
    print("-" * 20)

    print("Testing negative XP gain (should do nothing).")
    initial_xp = player.xp
    leveled = player.gain_xp(-50)
    print(f"Leveled up: {leveled}") 
    print(f"XP after negative gain: {player.xp}") 
    print("-" * 20)

    print("Testing zero XP gain (should do nothing).")
    leveled = player.gain_xp(0)
    print(f"Leveled up: {leveled}") 
    print(f"XP after zero gain: {player.xp}") 
    print("-" * 20)

    # Test that current HP is capped if max_hp decreases due to stat change
    player.hp = player.max_hp 
    print(f"HP set to max: {player.hp}/{player.max_hp}")
    player.stats['constitution'] -= 15 # Drastically reduce constitution
    player._calculate_derived_stats() # Recalculate
    print(f"Updated Constitution: {player.stats['constitution']}") 
    print(f"Updated Max HP: {player.max_hp}") 
    print(f"HP after constitution decrease: {player.hp}/{player.max_hp}") 
    print("-" * 20)

```
