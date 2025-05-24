from typing import List, Optional

class Zone:
    """
    Represents a zone in the RPG game, containing a list of enemy names.
    """
    def __init__(self, 
                 name: str, 
                 enemy_names: Optional[List[str]] = None):
        """
        Initializes a new zone.

        Args:
            name: The name of the zone (e.g., "Forest Zone").
            enemy_names: A list of enemy names found in this zone. 
                         If None, initializes to an empty list.
        """
        self.name: str = name
        self.enemy_names: List[str] = enemy_names if enemy_names is not None else []

    def add_enemy_name(self, enemy_name: str) -> None:
        """
        Adds an enemy name to the zone's list of enemy names.

        Args:
            enemy_name: The name of the enemy to add.
        """
        if enemy_name not in self.enemy_names: # Avoid duplicates if desired
            self.enemy_names.append(enemy_name)

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the zone.
        """
        return f"Zone: {self.name} (Enemies: {len(self.enemy_names)})"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    print("--- Zone Class Test ---")
    
    forest_zone = Zone(name="Forest Test Zone")
    print(f"Created zone: {forest_zone}")
    print(f"Initial enemy names: {forest_zone.enemy_names}")

    forest_zone.add_enemy_name("Goblin")
    forest_zone.add_enemy_name("Wolf")
    forest_zone.add_enemy_name("Forest Sprite")
    print(f"After adding enemies: {forest_zone}")
    print(f"Current enemy names: {forest_zone.enemy_names}")

    # Test adding a duplicate name (should not add if duplicate check is active)
    forest_zone.add_enemy_name("Goblin")
    print(f"After attempting to add 'Goblin' again: {forest_zone}")
    print(f"Enemy names: {forest_zone.enemy_names}")

    # Create a zone with initial enemies
    mountain_zone = Zone(name="Mountain Pass", enemy_names=["Giant Spider", "Harpy", "Rock Golem"])
    print(f"\nCreated zone: {mountain_zone}")
    print(f"Initial enemy names: {mountain_zone.enemy_names}")
    mountain_zone.add_enemy_name("Wyvern")
    print(f"After adding 'Wyvern': {mountain_zone}")
    print(f"Enemy names: {mountain_zone.enemy_names}")

    print("\n--- Zone Class Test Finished ---")
