from dataclasses import dataclass
from typing import List
from enum import Enum

class SkillLevel(Enum):
    false = None
    true = "Proficient"
    EXPERT = "Expert"

@dataclass
class Skills:
    athletics: SkillLevel = SkillLevel.false
    acrobatics: SkillLevel = SkillLevel.false
    sleight_of_hand: SkillLevel = SkillLevel.false
    stealth: SkillLevel = SkillLevel.false
    arcana: SkillLevel = SkillLevel.false
    history: SkillLevel = SkillLevel.false
    investigation: SkillLevel = SkillLevel.false
    nature: SkillLevel = SkillLevel.false
    religion: SkillLevel = SkillLevel.false
    animal_handling: SkillLevel = SkillLevel.false
    insight: SkillLevel = SkillLevel.false
    medicine: SkillLevel = SkillLevel.false
    perception: SkillLevel = SkillLevel.false
    survival: SkillLevel = SkillLevel.false
    deception: SkillLevel = SkillLevel.false
    intimidation: SkillLevel = SkillLevel.false
    performance: SkillLevel = SkillLevel.false
    persuasion: SkillLevel = SkillLevel.false

@dataclass
class Stats:
    str: int
    dex: int
    con: int
    int: int
    wis: int
    cha: int


@dataclass
class SpellSlot:
    total: int
    used: int

@dataclass
class SpellList:
    cantrips: List[str] = None
    level_1: SpellSlot = None
    level_2: SpellSlot = None
    level_3: SpellSlot = None
    level_4: SpellSlot = None
    level_5: SpellSlot = None
    level_6: SpellSlot = None
    level_7: SpellSlot = None
    level_8: SpellSlot = None
    level_9: SpellSlot = None

@dataclass
class Money:
    copper: int
    silver: int
    gold: int
    platinum: int

    def __post_init__(self):
        # Convert 100 copper to 1 silver, 100 silver to 1 gold, etc.
        self.silver += self.copper // 100
        self.copper %= 100
        self.gold += self.silver // 100
        self.silver %= 100
        self.platinum += self.gold // 100
        self.gold %= 100

@dataclass
class Item:
    name: str
    quantity: int
    weight: int
    description: str
    cost: Money

@dataclass
class Weapon(Item):
    dice_sides: int
    dice_number: int
    bonus: int
    damage_type: str
    properties: List[str]

@dataclass
class Armor(Item):
    ac: int
    strength_requirement: int
    stealth_disadvantage: bool

@dataclass
class CharacterSheet:
    name: str
    race: str
    character_class: str
    background: str
    level: int
    experience: int
    ac: int
    max_hit_points: int
    current_hit_points: int
    hit_dice: str
    proficiency_bonus: int
    speed: int
    stats: Stats
    skills: Skills
    actions_and_equipment: List[str]
    other_proficiencies_languages: List[str]
    racial_features: List[str]
    class_features: List[str]
    misc_features: List[str]
    notes: List[str]
    equipment: List[str]
    magic_items: List[str]
    money: Money
    spell_list: SpellList

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Race: {self.race}\n"
            f"Class: {self.character_class}\n"
            f"Background: {self.background}\n"
            f"Level: {self.level}\n"
            f"Experience: {self.experience}\n"
            f"AC: {self.ac}\n"
            f"Max Hit Points: {self.max_hit_points}\n"
            f"Current Hit Points: {self.current_hit_points}\n"
            f"Hit Dice: {self.hit_dice}\n"
            f"Proficiency Bonus: {self.proficiency_bonus}\n"
            f"Speed: {self.speed}\n"
            f"Stats: {self.stats}\n"
            "Skills: " + ', '.join([f"{skill}: {level.value}" for skill, level in self.skills.__dict__.items() if level != SkillLevel.false]) + "\n"
            f"Actions and Equipment: {self.actions_and_equipment}\n"
            f"Other Proficiencies/Languages: {self.other_proficiencies_languages}\n"
            f"Racial Features: {self.racial_features}\n"
            f"Class Features: {self.class_features}\n"
            f"Misc Features: {self.misc_features}\n"
            f"Notes: {self.notes}\n"
            f"Equipment: {self.equipment}\n"
            f"Magic Items: {self.magic_items}\n"
            f"Money: {self.money}\n"
            f"Spell List: {self.spell_list}\n"
        )
