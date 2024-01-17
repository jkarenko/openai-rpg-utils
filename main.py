from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
from starlette.responses import Response
import os
from rpg_utils.dice import Dice as d
from rpg_utils.character import CharacterSheet, Item, Weapon, Armor, Money, SpellList, SpellSlot, Stats

characters = {}

class RollActionResult(BaseModel):
    result: int
    instructions: str = "If this was to hit a target, compare the result to the target's armor class. If this was a skill check, compare the result to the DC of the check and add the appropriate modifiers."
    message_to_display: str = "[{character_or_enemy_name} rolls a {result + modifiers}] {description_of_what_happens_next}"

class RollDamageResult(BaseModel):
    rolls: List[int]
    result: int
    instructions: str = "Apply this damage and modifiers to the target and have the target take the next action immediately."
    message_to_display: str = "[{character_or_enemy_name} deals {result + modifiers} damage to {character_or_enemy_name}] {description_of_the_attack}."

class RollStatsResult(BaseModel):
    result: List[int]
    instructions: str = "Assign these numbers to your stats."

class CharacterSheetResult(BaseModel):
    result: CharacterSheet
    instructions: str = "This is a player's character sheet."
    message_to_display: str = "{character_sheet}"

class CharacterSheetSpecResult(BaseModel):
    result: str = f"A character sheet must contain these fields: {CharacterSheet.__annotations__}, Stats: {Stats.__annotations__}"
    message_to_display: str = "{character_sheet}"

class StatBlockSpecResult(BaseModel):
    result: str = f"An enemy stat block must contain these fields: {str(Stats.__annotations__)}, weapon, armor, ac, hit_points, speed, and actions_and_equipment."

class InvalidEndpointResponse(BaseModel):
    message: str


app = FastAPI(
    root_path=os.getenv("ROOT_PATH", "http://localhost:8000"),
)

v1_router = APIRouter(prefix="/rpg-utils/api/v1")
default_router = APIRouter()


@default_router.get("/", response_class=Response)
def default_root() -> str:
    return f"<html><body style='background-color: #1a1a1a; color: #f0f0f0;'>Welcome to the RPG Utils API! Check out the OpenAPI documentation at <a href={app.root_path}/docs style='color: #f0f0f0;'>{app.root_path}/docs</a>.</body></html>"


@v1_router.get("/privacy", response_class=Response)
def v1_privacy_policy() -> str:
    """
    Get the privacy policy of the API.

    This endpoint returns a string that describes the privacy policy of the API.

    Returns:
        str: A string that describes the privacy policy of the API.
    """
    return "This API may temporarily and anonymously store information about your game session. No data is stored in a database and all data is ephemeral."


@v1_router.get("/roll/action/", response_model=RollActionResult)
def v1_roll_action() -> RollActionResult:
    """
    Roll a d20 for an action.

    This endpoint rolls a d20 for an action in a game. The result is returned along with instructions on how to interpret it.

    Returns:
        RollActionResult: The result of the roll and instructions on how to interpret it.
    """
    roll_results = d(20).roll()
    return RollActionResult(result=roll_results)


@v1_router.get("/roll/d{dice_type}/{dice_count}/", response_model=RollDamageResult)
def v1_roll_damage(dice_type: int, dice_count: int = 1) -> RollDamageResult:
    """
    Roll a specified type of dice a certain number of times.

    Args:
        dice_type (int): The type of dice to roll (e.g., d6, d20, etc.).
        dice_count (int, optional): The number of dice to roll. Defaults to 1.

    Returns:
        RollDamageResult: The result of the dice roll(s).
    """
    roll_results = [d(dice_type).roll() for _ in range(dice_count)]
    return RollDamageResult(rolls=roll_results, result=sum(roll_results))


@v1_router.get("/roll/stats/", response_model=RollStatsResult)
def v1_roll_stats() -> RollStatsResult:
    """
    Roll 4d6 and drop the lowest die 6 times.

    This endpoint rolls 4d6 and drops the lowest die 6 times. The result is returned as a list of integers.

    Returns:
        RollStatsResult: The result of the roll.
    """
    roll_results = [sorted([d(6).roll() for _ in range(4)])[1:] for _ in range(6)]
    return RollStatsResult(result=[sum(roll) for roll in roll_results])



@v1_router.get("/character/spec/", response_model=CharacterSheetSpecResult)
def v1_get_sheet_spec() -> CharacterSheetSpecResult:
    """
    Get the specification for a character sheet.

    This endpoint returns a string that describes the required fields for a character sheet.

    Returns:
        CharacterSheetSpecResult: A string that describes the required fields for a character sheet.
    """
    return CharacterSheetSpecResult()

@v1_router.get("/enemy/spec/", response_model=StatBlockSpecResult)
def v1_get_enemy_spec() -> StatBlockSpecResult:
    """
    Get the specification for an enemy stat block.

    This endpoint returns a string that describes the required fields for an enemy stat block.

    Returns:
        StatBlockSpecResult: A string that describes the required fields for an enemy stat block.
    """
    return StatBlockSpecResult()


@v1_router.post("/character/create/", response_model=CharacterSheetResult)
def v1_create_character(character_sheet: CharacterSheet) -> CharacterSheetResult:
    """
    Create a new character.

    This endpoint accepts a character sheet, validates it, and stores it in the server's memory.

    Args:
        character_sheet (CharacterSheet): The character sheet to create.

    Returns:
        CharacterSheetResult: The created character sheet.
    """
    characters[character_sheet.name] = character_sheet
    return CharacterSheetResult(result=character_sheet)

app.include_router(v1_router)
app.include_router(default_router)
