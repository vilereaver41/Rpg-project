from typing import List, Dict, Any

class Skill:
    """
    Represents a base skill in the RPG game.
    """
    def __init__(self, 
                 name: str, 
                 description: str, 
                 skill_rarity: str, 
                 skill_type_csv: str, # e.g., "Active", "Passive" from CSV
                 category: str):    # e.g., "Combat", "Utility", "Class Specific"
        """
        Initializes a new base skill.

        Args:
            name: The name of the skill.
            description: A short description of the skill.
            skill_rarity: The rarity of the skill (e.g., "Common", "Legendary").
            skill_type_csv: The type of skill as listed in a CSV (e.g., "Active", "Passive").
            category: The category the skill belongs to.
        """
        self.name: str = name
        self.description: str = description
        self.skill_rarity: str = skill_rarity
        self.skill_type_csv: str = skill_type_csv # Type from CSV, might be "Active" or "Passive"
        self.category: str = category

    def __str__(self) -> str:
        return f"{self.name} ({self.skill_rarity} {self.category} {self.skill_type_csv}): {self.description}"


class Ability(Skill):
    """
    Represents an activatable ability, inheriting from Skill.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 skill_rarity: str,
                 skill_type_csv: str, # Should typically be "Active" for abilities/spells
                 category: str,
                 scope: str = "",       # e.g., "1 Enemy", "All Allies", "Self"
                 cost: str = "",        # e.g., "5 MP", "10% HP" (kept as string for flexibility)
                 dmg_type: str = "",    # e.g., "Physical", "Magical", "Hybrid"
                 element: str = "",     # e.g., "Fire", "Nil Element", "Holy"
                 occasion: str = "",    # e.g., "Battle Only", "Anytime"
                 formula: str = "",     # e.g., "PATK * 2 - PDEF", "MATK * 1.5"
                 variance: str = "",    # e.g., "20%" (kept as string)
                 critical: str = "",    # e.g., "Yes", "No", "PATK * 0.5" (formula for crit bonus)
                 hit_type: str = "",    # e.g., "Physical", "Magical", "Certain Hit"
                 animation: str = "",   # Name or ID of the animation to play
                 requirement: str = "", # e.g., "Sword Equipped", "Level > 10"
                 effects_csv: str = "", # Description of effects, e.g. "Inflict Poison (30%, 3 turns)"
                 additional_notes: str = ""):
        """
        Initializes a new ability.
        """
        super().__init__(name, description, skill_rarity, skill_type_csv, category)
        self.scope: str = scope
        self.cost: str = cost
        self.dmg_type: str = dmg_type
        self.element: str = element
        self.occasion: str = occasion
        self.formula: str = formula
        self.variance: str = variance
        self.critical: str = critical
        self.hit_type: str = hit_type
        self.animation: str = animation
        self.requirement: str = requirement
        self.effects_csv: str = effects_csv # Effects from CSV field
        self.additional_notes: str = additional_notes

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} [Cost: {self.cost}, Scope: {self.scope}, Element: {self.element}] Effects: {self.effects_csv}"


class PassiveSkill(Skill):
    """
    Represents a passive skill, inheriting from Skill.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 skill_rarity: str,
                 skill_type_csv: str, # Should typically be "Passive"
                 category: str,
                 effects_csv: str = ""): # Description of passive effects
        """
        Initializes a new passive skill.
        """
        super().__init__(name, description, skill_rarity, skill_type_csv, category)
        self.effects_csv: str = effects_csv

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} Effects: {self.effects_csv}"


class Spell(Ability):
    """
    Represents a spell, inheriting from Ability.
    Spells are a specific type of Ability, often with MP costs and magical effects.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 skill_rarity: str,
                 skill_type_csv: str, # Should typically be "Active"
                 category: str, # Often "Magic", "Elemental", "Healing" etc.
                 scope: str = "",
                 cost: str = "", # Typically MP for spells
                 dmg_type: str = "Magical", # Default to Magical for spells
                 element: str = "",
                 occasion: str = "Battle Only", # Default for many spells
                 formula: str = "",
                 variance: str = "",
                 critical: str = "No", # Spells might have different crit rules
                 hit_type: str = "Magical", # Default to Magical hit type
                 animation: str = "",
                 requirement: str = "",
                 effects_csv: str = "",
                 additional_notes: str = ""):
        """
        Initializes a new spell.
        """
        super().__init__(name=name, description=description, skill_rarity=skill_rarity,
                         skill_type_csv=skill_type_csv, category=category, scope=scope, cost=cost,
                         dmg_type=dmg_type, element=element, occasion=occasion, formula=formula,
                         variance=variance, critical=critical, hit_type=hit_type, animation=animation,
                         requirement=requirement, effects_csv=effects_csv, additional_notes=additional_notes)
        # Future: Spells might have specific attributes like charge time, spell school, etc.
        # For now, its structure is identical to Ability but allows for type differentiation.

    def __str__(self) -> str:
        # Could refine this further for spells if needed
        return super().__str__()


if __name__ == '__main__':
    print("--- Example Skills ---")

    # Ability Example
    power_strike = Ability(
        name="Power Strike",
        description="A strong attack that deals extra damage.",
        skill_rarity="Common",
        skill_type_csv="Active",
        category="Combat Maneuver",
        scope="1 Enemy",
        cost="5 Stamina",
        dmg_type="Physical",
        element="Nil Element",
        occasion="Battle Only",
        formula="PATK * 1.5",
        variance="10%",
        critical="Yes",
        hit_type="Physical",
        animation="anim_power_strike",
        requirement="Melee Weapon Equipped",
        effects_csv="Deals 150% weapon damage.",
        additional_notes="Basic warrior skill."
    )
    print("\nAbility Example:")
    print(power_strike)
    print(f"  Formula: {power_strike.formula}")
    print(f"  Requirements: {power_strike.requirement}")
    print(f"  Additional Notes: {power_strike.additional_notes}")


    # PassiveSkill Example
    blade_reaver = PassiveSkill(
        name="Blade Reaver",
        description="Increases critical hit chance with swords.",
        skill_rarity="Rare",
        skill_type_csv="Passive",
        category="Swordsmanship",
        effects_csv="Critical Chance +5% when a sword is equipped."
    )
    print("\nPassive Skill Example:")
    print(blade_reaver)
    print(f"  Effects (from effects_csv): {blade_reaver.effects_csv}")

    # Spell Example (modeling "Heal")
    # Assuming "Heal" from a CSV might have some fields blank, but we know it's a Spell.
    heal_spell = Spell(
        name="Heal",
        description="Restores a moderate amount of HP to an ally.",
        skill_rarity="Common",
        skill_type_csv="Active", # Spells are active
        category="Restoration Magic",
        scope="1 Ally",
        cost="10 MP",
        dmg_type="Healing", # Using dmg_type to indicate healing
        element="Light",    # Or "Nil Element" if no specific elemental affinity for healing
        occasion="Battle Only",
        formula="MATK * 1.2 + Spirit * 0.5", # Example healing formula
        variance="5%",
        critical="No", # Healing usually doesn't crit unless specified
        hit_type="Certain Hit", # Healing usually doesn't miss
        animation="anim_heal_spell",
        requirement="Staff Equipped OR Class = Healer",
        effects_csv="Restores HP.", # Simplified effect description
        additional_notes="Basic healing spell."
    )
    print("\nSpell Example:")
    print(heal_spell)
    print(f"  Cost: {heal_spell.cost}")
    print(f"  Formula: {heal_spell.formula}")
    print(f"  Element: {heal_spell.element}")
    print(f"  Effects (from effects_csv): {heal_spell.effects_csv}")

    # Another PassiveSkill example
    toughness = PassiveSkill(
        name="Toughness",
        description="Permanently increases maximum HP.",
        skill_rarity="Uncommon",
        skill_type_csv="Passive",
        category="Survival",
        effects_csv="Max HP +10%"
    )
    print("\nAnother Passive Skill Example:")
    print(toughness)

    # Another Ability example - a debuff
    armor_break = Ability(
        name="Armor Break",
        description="Weakens an enemy's defense.",
        skill_rarity="Uncommon",
        skill_type_csv="Active",
        category="Debuff",
        scope="1 Enemy",
        cost="8 MP",
        dmg_type="Nil Element", # Or "Physical" if it's a physical strike that applies it
        element="Nil Element",
        occasion="Battle Only",
        formula="", # No direct damage, effect based
        variance="0%",
        critical="No",
        hit_type="Physical", # The check to see if it lands
        animation="anim_armor_break",
        requirement="",
        effects_csv="Reduces target's PDEF by 20% for 3 turns.",
        additional_notes=""
    )
    print("\nDebuff Ability Example:")
    print(armor_break)
