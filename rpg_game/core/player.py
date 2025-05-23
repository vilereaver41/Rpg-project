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
    # Current XP: 50. XP to next: 100. Needs 50 more for level up.
    # Gaining 70 XP. 50 + 70 = 120.
    # Level up: XP becomes 120 - 100 = 20. Level 2. Next XP target: 150.
    # Stats increase: Str+2, Dex+2, Int+2, Con+2, Luck+1
    # Con becomes 12. Max HP becomes 120. HP restored to 120.
    # Int becomes 12. Max MP becomes 60. MP restored to 60.
    leveled = player.gain_xp(70) 
    print(f"Leveled up: {leveled}") # Expected: True
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") # Expected: L2, 20/150 XP
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}") # Expected: 120/120 HP, 60/60 MP
    print(f"Primary Stats: {player.stats}") # Str:12, Dex:12, Int:12, Con:12, Luck:6
    print(f"Derived Stats: {player.derived_stats}") # Atk:24, Def:18, MagP:24, Crit:0.3, Acc:1.2, Eva:0.24
    print("-" * 20)

    # Test another level up to ensure XP carry-over and multiple level ups work
    print(f"Gaining 200 XP...")
    # Current XP: 20. XP to next: 150. Needs 130 more.
    # Gaining 200 XP. 20 + 200 = 220.
    # Level up 1 (to L3): XP becomes 220 - 150 = 70. Next XP target: 200.
    # Stats increase: Str+2, Dex+2, Int+2, Con+2, Luck+1
    # Con becomes 14. Max HP becomes 140. HP restored to 140.
    # Int becomes 14. Max MP becomes 70. MP restored to 70.
    leveled = player.gain_xp(200)
    print(f"Leveled up: {leveled}") # Expected: True
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") # Expected: L3, 70/200 XP
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}") # Expected: 140/140 HP, 70/70 MP
    print(f"Primary Stats: {player.stats}") # Str:14, Dex:14, Int:14, Con:14, Luck:7
    print(f"Derived Stats: {player.derived_stats}") # Atk:28, Def:21, MagP:28, Crit:0.35, Acc:1.4, Eva:0.28
    print("-" * 20)
    
    # Test multiple level ups from a single XP gain
    player.xp = 0
    player.level = 1
    player.stats = {'strength': 10, 'dexterity': 10, 'intelligence': 10, 'constitution': 10, 'luck': 5}
    player.xp_to_next_level = 100
    player._calculate_derived_stats()
    player.hp = player.max_hp
    player.mp = player.max_mp
    print(f"Reset player to Level 1 for multi-level test. XP: {player.xp}/{player.xp_to_next_level}")
    print(f"Gaining 250 XP (enough for two levels)...")
    # L1 -> L2: Needs 100 XP. 250 - 100 = 150 remaining. Next XP target: 150.
    # L2 -> L3: Needs 150 XP. 150 - 150 = 0 remaining. Next XP target: 200.
    leveled = player.gain_xp(250)
    print(f"Leveled up: {leveled}") # Expected: True
    print(f"Level: {player.level}, XP: {player.xp}/{player.xp_to_next_level}") # Expected: L3, 0/200 XP
    print(f"HP: {player.hp}/{player.max_hp}, MP: {player.mp}/{player.max_mp}") # Expected: Con 14 -> 140/140 HP, Int 14 -> 70/70 MP
    print(f"Primary Stats: {player.stats}") # Str:14, Dex:14, Int:14, Con:14, Luck:7
    print(f"Derived Stats: {player.derived_stats}")
    print("-" * 20)

    # Test take_damage to 0
    player.take_damage(player.max_hp + 50) # Take more than max HP
    print(f"HP after taking critical damage: {player.hp}/{player.max_hp}") # Expected: 0
    print("-" * 20)
    player.heal(player.max_hp)
    print(f"HP after healing to max: {player.hp}/{player.max_hp}") # Expected: max_hp (140)

    # Test derived stat calculation after direct stat modification
    print(f"Constitution before manual change: {player.stats['constitution']}") # Expected: 14
    print(f"Max HP before: {player.max_hp}") # Expected: 140
    print(f"Defense before: {player.derived_stats['defense']}") # Expected: 21
    player.stats['constitution'] += 10 # Manually increase constitution
    player._calculate_derived_stats() # Recalculate
    # Note: current HP is not automatically adjusted here unless it exceeds new max_hp,
    # or healed. This is typically fine as direct stat changes are rare outside leveling.
    print(f"Updated Constitution: {player.stats['constitution']}") # Expected: 24
    print(f"Updated Max HP: {player.max_hp}") # Expected: 240
    print(f"Updated Defense: {player.derived_stats['defense']}") # Expected: 36
    print(f"Current HP: {player.hp}/{player.max_hp}") # Expected: 140/240 (HP didn't change)
    print("-" * 20)

    print("Testing negative XP gain (should do nothing).")
    initial_xp = player.xp
    leveled = player.gain_xp(-50)
    print(f"Leveled up: {leveled}") # Expected: False
    print(f"XP after negative gain: {player.xp}") # Expected: same as initial_xp
    print("-" * 20)

    print("Testing zero XP gain (should do nothing).")
    leveled = player.gain_xp(0)
    print(f"Leveled up: {leveled}") # Expected: False
    print(f"XP after zero gain: {player.xp}") # Expected: same as initial_xp
    print("-" * 20)

    # Test that current HP is capped if max_hp decreases due to stat change
    player.hp = player.max_hp # Heal to current max (240)
    print(f"HP set to max: {player.hp}/{player.max_hp}")
    player.stats['constitution'] -= 15 # Drastically reduce constitution
    player._calculate_derived_stats() # Recalculate
    print(f"Updated Constitution: {player.stats['constitution']}") # Expected: 24-15 = 9
    print(f"Updated Max HP: {player.max_hp}") # Expected: 90
    print(f"HP after constitution decrease: {player.hp}/{player.max_hp}") # Expected: 90/90 (capped)
    print("-" * 20)

```
