import unittest
from items import Item, Equipment, Weapon, Armor, ItemRarity

class TestItems(unittest.TestCase):
    def test_item_creation(self):
        item = Item(name="Scroll", description="A magical scroll.", rarity=ItemRarity.UNCOMMON)
        self.assertEqual(item.name, "Scroll")
        self.assertEqual(item.description, "A magical scroll.")
        self.assertEqual(item.rarity, ItemRarity.UNCOMMON)
        self.assertEqual(str(item), "Scroll (Uncommon)")

    def test_equipment_creation(self):
        # Valid equipment
        ring = Equipment(name="Ring of Power", description="A powerful ring.", 
                         rarity=ItemRarity.RARE, equip_slot="ring", 
                         stat_bonuses={'strength': 3, 'intelligence': 2})
        self.assertEqual(ring.name, "Ring of Power")
        self.assertEqual(ring.equip_slot, "ring")
        self.assertEqual(ring.stat_bonuses['strength'], 3)
        self.assertEqual(str(ring), "Ring of Power (Rare) - Slot: ring, Bonuses: {'strength': 3, 'intelligence': 2}")

        # Invalid equip_slot
        with self.assertRaises(ValueError):
            Equipment(name="Invalid Boots", description="These won't fit.",
                      rarity=ItemRarity.COMMON, equip_slot="shoes", stat_bonuses={})

    def test_weapon_creation(self):
        sword = Weapon(name="Great Sword", description="A large two-handed sword.",
                       rarity=ItemRarity.EPIC, attack_bonus=15, strength_bonus=5, dexterity_bonus=2)
        self.assertEqual(sword.name, "Great Sword")
        self.assertEqual(sword.equip_slot, "weapon")
        self.assertEqual(sword.stat_bonuses['attack_power'], 15)
        self.assertEqual(sword.stat_bonuses['strength'], 5)
        self.assertEqual(sword.stat_bonuses['dexterity'], 2)
        self.assertEqual(str(sword), "Great Sword (Epic) - Slot: weapon, Bonuses: {'attack_power': 15, 'strength': 5, 'dexterity': 2}")

        # Weapon with only one bonus
        dagger = Weapon(name="Dagger", description="A small dagger.", rarity=ItemRarity.COMMON, attack_bonus=3)
        self.assertEqual(dagger.stat_bonuses['attack_power'], 3)
        self.assertNotIn('strength', dagger.stat_bonuses) # Ensure other bonuses are not present if 0

    def test_armor_creation(self):
        plate_armor = Armor(name="Steel Plate", description="Heavy steel plate armor.",
                            rarity=ItemRarity.LEGENDARY, equip_slot="chest",
                            defense_bonus=20, constitution_bonus=7, max_hp_bonus=50)
        self.assertEqual(plate_armor.name, "Steel Plate")
        self.assertEqual(plate_armor.equip_slot, "chest")
        self.assertEqual(plate_armor.stat_bonuses['defense'], 20)
        self.assertEqual(plate_armor.stat_bonuses['constitution'], 7)
        self.assertEqual(plate_armor.stat_bonuses['max_hp'], 50)
        self.assertEqual(str(plate_armor), "Steel Plate (Legendary) - Slot: chest, Bonuses: {'defense': 20, 'constitution': 7, 'max_hp': 50}")

        shield = Armor(name="Iron Shield", description="A basic shield.", rarity=ItemRarity.COMMON,
                       equip_slot="shield", defense_bonus=5)
        self.assertEqual(shield.equip_slot, "shield")
        self.assertEqual(shield.stat_bonuses['defense'], 5)

        # Invalid equip_slot for armor
        with self.assertRaises(ValueError):
            Armor(name="Invalid Hat", description="Not really armor.", rarity=ItemRarity.COMMON,
                  equip_slot="ring", defense_bonus=1) # Ring is not an armor slot

if __name__ == '__main__':
    unittest.main()
