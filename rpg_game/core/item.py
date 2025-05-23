class Item:
    """
    Represents a generic item in the RPG game.
    """
    def __init__(self, name: str, description: str):
        """
        Initializes a new item.

        Args:
            name: The name of the item.
            description: A short description of the item.
        """
        self.name: str = name
        self.description: str = description

    def __str__(self) -> str:
        """
        Returns a string representation of the item.

        Returns:
            A string in the format "name: description".
        """
        return f"{self.name}: {self.description}"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    potion = Item("Health Potion", "Restores a small amount of HP.")
    sword = Item("Iron Sword", "A basic but reliable sword.")
    
    print("Created Items:")
    print(potion)
    print(sword)

    print(f"\nItem Name: {potion.name}")
    print(f"Item Description: {potion.description}")

    print(f"\nItem Name: {sword.name}")
    print(f"Item Description: {sword.description}")
