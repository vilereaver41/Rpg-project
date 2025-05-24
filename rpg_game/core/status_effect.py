from typing import Dict, Any

class StatusEffect:
    """
    Represents a status effect in the RPG game.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 effect_type: str,  # "Positive" or "Negative"
                 element: str = "",
                 duration_str: str = "",  # Raw duration string from CSV e.g. "3 Turns", "Permanent"
                 effect_description: str = "", # From "Effect" column in CSV
                 notes: str = ""):
        """
        Initializes a new status effect.

        Args:
            name: The name of the status effect.
            description: A short description of the status effect.
            effect_type: The type of effect ("Positive" or "Negative").
            element: The elemental affinity of the status effect, if any.
            duration_str: The duration of the effect as a string (e.g., "3 Turns").
            effect_description: Description of the actual mechanical effect.
            notes: Additional notes or flavor text.
        """
        self.name: str = name
        self.description: str = description
        self.effect_type: str = effect_type
        self.element: str = element
        self.duration_str: str = duration_str
        self.effect_description: str = effect_description
        self.notes: str = notes

    def __str__(self) -> str:
        """
        Returns a string representation of the status effect.
        """
        return (f"{self.name} ({self.effect_type}) - Duration: {self.duration_str}\n"
                f"  Description: {self.description}\n"
                f"  Effect: {self.effect_description}\n"
                f"  Element: {self.element if self.element else 'None'}\n"
                f"  Notes: {self.notes if self.notes else 'N/A'}")

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    distorted_reality = StatusEffect(
        name="Distorted Reality",
        description="The fabric of reality seems to warp around the affected.",
        effect_type="Positive",
        element="Arcane",
        duration_str="Until End of Battle",
        effect_description="Increases chance to dodge magical attacks by 25%.",
        notes="Often applied by powerful dimensional beings."
    )

    poison = StatusEffect(
        name="Poison",
        description="Deals damage over time.",
        effect_type="Negative",
        element="Nature", # Or could be "Poison" as an element type
        duration_str="3 Turns",
        effect_description="Deals 5% of Max HP as Nature damage at the start of each turn.",
        notes="Can be cured by Antidote."
    )
    
    blessed_aura = StatusEffect(
        name="Blessed Aura",
        description="A holy aura that enhances defensive capabilities.",
        effect_type="Positive",
        element="Light",
        duration_str="5 Turns",
        effect_description="Increases Defense and Magic Defense by 10.",
        notes="" # No notes for this one
    )

    print("--- Created Status Effects ---")
    print(f"\n{distorted_reality}")
    print(f"\n{poison}")
    print(f"\n{blessed_aura}")

    print(f"\n--- Individual Attribute Check: {distorted_reality.name} ---")
    print(f"  Name: {distorted_reality.name}")
    print(f"  Description: {distorted_reality.description}")
    print(f"  Effect Type: {distorted_reality.effect_type}")
    print(f"  Element: {distorted_reality.element}")
    print(f"  Duration String: {distorted_reality.duration_str}")
    print(f"  Effect Description: {distorted_reality.effect_description}")
    print(f"  Notes: {distorted_reality.notes}")

    print(f"\n--- Individual Attribute Check: {poison.name} ---")
    print(f"  Name: {poison.name}")
    print(f"  Description: {poison.description}")
    print(f"  Effect Type: {poison.effect_type}")
    print(f"  Element: {poison.element}")
    print(f"  Duration String: {poison.duration_str}")
    print(f"  Effect Description: {poison.effect_description}")
    print(f"  Notes: {poison.notes}")
    
    print(f"\n--- Individual Attribute Check: {blessed_aura.name} ---")
    print(f"  Name: {blessed_aura.name}")
    print(f"  Description: {blessed_aura.description}")
    print(f"  Effect Type: {blessed_aura.effect_type}")
    print(f"  Element: {blessed_aura.element}")
    print(f"  Duration String: {blessed_aura.duration_str}")
    print(f"  Effect Description: {blessed_aura.effect_description}")
    print(f"  Notes: {blessed_aura.notes}")
