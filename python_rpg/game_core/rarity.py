from enum import Enum, auto

class Rarity(Enum):
    COMMON = ("Common", "grey", 0.60)
    UNCOMMON = ("Uncommon", "green", 0.25)
    RARE = ("Rare", "blue", 0.10)
    EPIC = ("Epic", "purple", 0.04)
    LEGENDARY = ("Legendary", "orange", 0.009)
    MYTHICAL = ("Mythical", "red", 0.001)

    @property
    def display_name(self) -> str:
        return self.value[0]

    @property
    def color(self) -> str:
        return self.value[1]

    @property
    def drop_rate(self) -> float:
        return self.value[2]

if __name__ == '__main__':
    print("--- All Rarities ---")
    for rarity in Rarity:
        print(f"Name: {rarity.name}")
        print(f"  Display Name: {rarity.display_name}")
        print(f"  Color: {rarity.color}")
        print(f"  Drop Rate: {rarity.drop_rate*100:.3f}%")
        print("-" * 10)

    print("\n--- Specific Rarity Example (EPIC) ---")
    epic_rarity = Rarity.EPIC
    print(f"Name: {epic_rarity.name}")
    print(f"Display Name: {epic_rarity.display_name}")
    print(f"Color: {epic_rarity.color}")
    print(f"Drop Rate: {epic_rarity.drop_rate*100:.3f}%")

    print("\n--- Accessing LEGENDARY properties ---")
    print(f"Legendary Display Name: {Rarity.LEGENDARY.display_name}")
    print(f"Legendary Color: {Rarity.LEGENDARY.color}")
    print(f"Legendary Drop Rate: {Rarity.LEGENDARY.drop_rate}")
