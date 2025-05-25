import time
from os import environ
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from openai import OpenAI
import random

#DEEPSEEK_KEY = environ["DEEPSEEK_API_KEY"]
#client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
OPENAI_KEY = environ["GEMINI_API_KEY"]

client = OpenAI(api_key=OPENAI_KEY,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
countries = ["England","Austria","Italy","Turkey","Germany","Russia","France"]
class YN(Enum):
     Y = "yes"
     N = "no"
class YesNo(BaseModel):
    yn: YN

'''print(client.beta.chat.completions.parse(
    model="gemini-2.0-flash",
    messages=[{"role": "user", "content": "yes or no"}],
     response_format=YesNo,
    ))'''

personalities = [
    ["chaotic","lawful"],["evil","moral"],["friendly"],["devious"],["trustworthy","untrustworthy"],
    ["secretly in love with the "+random.choice(countries) + " player", "despises the "+random.choice(countries) + " player"],
    ["impatient","patient"],["quirky"],["distracted"],["strange"],["unhinged"],["a total bro"],["drunk"],["whimsical"],["massively overuses emoji"],["extremely excitable","completely chill"],
    ["can't use the letter " + random.choice(["a","e","i","o","u","s","t"]) + " while messaging other players"],["very occasionally asks one question that's way too personal"],
    ["efficient"],["cold","warm"],["contrarian"],["broken"],["caveman"],["ancient","childish"],["fae"],["addicted to Twitch slang"],["constatly lie about other player's moves"],["1920s mobster boss"],["massive risk taker"],["Must speak like a dr, suess book"],["neurotic"],["Finance speculator: loves investing and crypto and gives unsolicited advice"],["surfer dude"],["Gleeful","Gloomy"],["would do any bet"],["keeps making references to stories from their childhood"],["Goofball"],["Steadfast","Paranoid"],["Hot-Headed"],["Genius"],["Creative"],["Self-Assured","Insecure"],["Ambitious"]
    ]

#Brings everything back to something from childhood
#believes they're in a simulation.
#would do any bet

#print("There are a total of "+ str(len(personalities)) + " traits.")

def get_personality(num_traits):
    global personalities
    traits = ""
    for i in range(num_traits):
        choice = random.choice(personalities)
        traits += random.choice(choice) + ", "
        personalities.remove(choice)
    #traits  += "keeps making references to stories from their childhood"
    #print(traits)
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "developer", "content": "Your job is to summarise a list of randomly generated 'Personality traits' into a maximum of 2 sentances instructing an llm who will be playing the board game diplomacy how to act. You **MUST** include all listed traits, even if they are nonsensical or contradictory"},
            {"role": "user", "content": traits}
        ]
    )
    personality = response.choices[0].message.content
    print(personality)
    time.sleep(4)
    return personality


class Country(Enum):
    AUSTRIA = "Austria"
    ENGLAND = "England"
    FRANCE = "France"
    GERMANY = "Germany"
    ITALY = "Italy"
    RUSSIA = "Russia"
    TURKEY = "Turkey"

class Message(BaseModel):
    to: list[Country]
    body: str
class Unit(Enum):
    ARMY = 'a'
    FLEET = 'f'
class MoveType(Enum):
    HOLD = "hold"
    MOVE = "move"
    SUPPORT = "support"
    CONVOY = "convoy"
class UnitLocation(BaseModel):
    unit_type: Unit
    location: str = Field(description = "Map tile this unit is located on. 3 letter string (except for split coasts)")
class Order(BaseModel):
    unit: UnitLocation
    move_type: MoveType
    target_start: str = Field("Map tile the unit targeted starts on. In the case of a move or hold, identical to the units location. Otherwise the tile on which the unit that 'unit' is targetting is located.")
    target_end: str = Field("Ditto above but for end location instead.")

class Retreat(BaseModel):
    unit: UnitLocation
    destination: str  = Field(description = "Map tile this unit should retreat to. 3 letter string (except for split coasts)")
class Build(BaseModel):
    builds: list[UnitLocation] = Field(description = "List of new units to be built this turn.")
class Disband(BaseModel):
    disbands: list[UnitLocation] = Field(description = "List of locations of units to remove this turn.")

class Discussion(BaseModel):
    messages: list[Message]
    #submit: bool Field(description = "Whether or not to submit orders. True if you have finished all the turn's discussions, False otherwise.")
    turn_readyness: float = Field(description = "A confindence interval between 0 and 1 on how confident you are that you have finished discussion and are ready to move on")
class Orders(BaseModel):
    orders: list[Order]
    
'''completion = client.beta.chat.completions.parse(
    model="gemini-2.0-flash",
    #model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are playing a game of diplomacy as France." + personality},
        {"role": "user", "content": "It is turn 2; Fall 1901\n The Current State of the board is as follows...Austria,\na bud\nf tri\na vie\nEngland,\nf edi\nf lon\na lvp\nFrance,\nf bre\na mar\na par\nGermany,\na ber\nf kie\na mun\nItaly,\nf nap\na rom\na ven\nRussia,\na mos\nf sev\nf stp_sc\na war\nTurkey,\nf ank\na con\na smy|"},
    ],
    response_format=Discussion,
)
x = completion.choices[0].message.parsed
print(x)
'''