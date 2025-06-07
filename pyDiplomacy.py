# Deepseek, GPT 4o, Gemini, Azure AI Service (phi)????, MEta LLama, Grok? there's also one called claude
import re

from gtts import gTTS
import pyttsx3
import requests
import random
import json
from enum import Enum
from pygame import mixer
from time import sleep, time
from os import environ
from openai import OpenAI
from pydantic import BaseModel, Field
from types import SimpleNamespace
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.select import Select
from selenium.common import NoSuchElementException

from aiTest import get_personality
from flask_app import *

mixer.init()


class Tile:
    name = ""
    abbr = ""
    land_adj = None
    sea_adj = None
    unit = None
    supply = False

    def __init__(self, name, land=True, unit=None):
        self.name = name
        self.land = land
        self.unit = unit
        self.land_adj = []
        self.sea_adj = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.abbr

    def __eq__(self, t):
        return self.abbr == t.abbr

    def set_adj(self, land_tiles=[], sea_tiles=[]):
        if not isinstance(land_tiles, list):
            land_tiles = [land_tiles]
        if not isinstance(sea_tiles, list):
            sea_tiles = [sea_tiles]
        for tile in land_tiles:
            self.land_adj.append(tile)
            tile.land_adj.append(self)
        for tile in sea_tiles:
            self.sea_adj.append(tile)
            tile.sea_adj.append(self)

    def set_unit(self, unit):
        self.unit = unit
        return self


class CoastOnly(Tile):
    parent = None

    def __init__(self, name, parent, unit=None):
        super().__init__(name, False, unit)
        self.parent = parent

    def set_unit(self, unit):
        self.parent.set_unit(unit)
        self.unit = unit
        return self


class MultiCoast(Tile):
    nc = None
    sc = None

    def __init__(self, name, nc_name, sc_name, unit=None, unit_location="l"):
        super().__init__(name, True, unit)
        self.adj = []
        self.nc = CoastOnly(name + " " + nc_name, self)
        self.sc = CoastOnly(name + " " + sc_name, self)


def createBoard():
    board = {}
    board["nao"] = nao = Tile("North Atlantic Ocean", False)
    board["nwg"] = nwg = Tile("Norwegian Sea", False)
    nwg.set_adj([], nao)
    board["bar"] = bar = Tile("Barent's Sea", False)
    bar.set_adj([], nwg)
    board["stp"] = stp = MultiCoast("Saint Petersburg", "North Coast", "South Coast")
    board["stp_nc"] = stp.nc
    stp.nc.set_adj([], bar)
    board["stp_sc"] = stp.sc
    board["fin"] = fin = Tile("Finland")
    fin.set_adj(stp, stp.sc)
    board["bot"] = bot = Tile("Golf of Bothnia", False)
    bot.set_adj([], [fin, stp.sc])
    board["swe"] = swe = Tile("Sweden")
    swe.set_adj(fin, [fin, bot])
    board["nwy"] = nwy = Tile("Norway")
    nwy.set_adj([swe, stp, fin], [swe, nwg, bar, stp.nc])
    board["ska"] = ska = Tile("Skaggerak", False)
    ska.set_adj([], [swe, nwy])
    board["nth"] = nth = Tile("North Sea", False)
    nth.set_adj([], [nwg, ska, nwy])
    board["edi"] = edi = Tile("Edinburgh")
    edi.set_adj([], [nwg, nth])
    board["cly"] = cly = Tile("Clyde")
    cly.set_adj([edi], [edi, nao, nwg])
    board["lvp"] = lvp = Tile("Liverpool")
    lvp.set_adj([edi, cly], [nao, cly])
    board["iri"] = iri = Tile("Irish Sea", False)
    iri.set_adj([], [lvp, nao])
    board["yor"] = yor = Tile("Yorkshire")
    yor.set_adj([edi, lvp], [nth, edi])
    board["hel"] = hel = Tile("Helgoland Bight", False)
    hel.set_adj([], [nth])
    board["den"] = den = Tile("Denmark")
    den.set_adj([swe], [swe, nth, ska, hel])
    board["bal"] = bal = Tile("Baltic Sea", False)
    bal.set_adj([], [den, swe, bot])
    board["lvn"] = lvn = Tile("Livonia")
    lvn.set_adj([stp], [bal, bot, stp.sc])
    board["mos"] = mos = Tile("Moscow")
    mos.set_adj([lvn, stp])
    board["war"] = war = Tile("Warsaw")
    war.set_adj([mos, lvn])
    board["pru"] = pru = Tile("Prussia")
    pru.set_adj([lvn, war], [lvn, bal])
    board["ber"] = ber = Tile("Berlin")
    ber.set_adj([pru], [pru, bal])
    board["kie"] = kie = Tile("Kiel")
    kie.set_adj([ber, den], [ber, den, bal, hel])
    board["hol"] = hol = Tile("The Netherlands")
    hol.set_adj([kie], [kie, hel, nth])
    board["bel"] = bel = Tile("Belgium")
    bel.set_adj([hol], [nth, hol])
    board["pic"] = pic = Tile("Picardy")
    pic.set_adj([bel], [bel])
    board["bre"] = bre = Tile("Brest")
    bre.set_adj([pic], [pic])
    board["mao"] = mao = Tile("Mid Atlantic Ocean", False)
    mao.set_adj([], [nao, iri, bre])
    board["eng"] = eng = Tile("English Channel", False)
    eng.set_adj([], [mao, iri, bre, pic, bel])
    board["wal"] = wal = Tile("Wales")
    wal.set_adj([lvp, yor], [iri, eng, lvp])
    board["lon"] = lon = Tile("London")
    lon.set_adj([wal, yor], [wal, yor, nth, eng])
    board["gas"] = gas = Tile("Gascony")
    gas.set_adj([bre], [mao, bre])
    board["par"] = par = Tile("Paris")
    par.set_adj([bre, gas, pic])
    board["bur"] = bur = Tile("Burgundy")
    bur.set_adj([par, bel, pic, gas])
    board["ruh"] = ruh = Tile("Ruhr")
    ruh.set_adj([bur, bel, hol, kie])
    board["mun"] = mun = Tile("Munich")
    mun.set_adj([ruh, bur, ber, kie])
    board["boh"] = boh = Tile("Bohemia")
    boh.set_adj([mun])
    board["sil"] = sil = Tile("Silesia")
    sil.set_adj([boh, mun, ber, pru, war])
    board["gal"] = gal = Tile("Galacia")
    gal.set_adj([war, sil, boh])
    board["ukr"] = ukr = Tile("Ukraine")
    ukr.set_adj([gal, mos, war])
    board["sev"] = sev = Tile("Sevastopol")
    sev.set_adj([ukr, mos])
    board["rum"] = rum = Tile("Rumania")
    rum.set_adj([sev, ukr, gal], [sev])
    board["bud"] = bud = Tile("Budapest")
    bud.set_adj([rum, gal])
    board["vie"] = vie = Tile("Vienna")
    vie.set_adj([bud, gal, boh])
    board["tyr"] = tyr = Tile("Tyrolia")
    tyr.set_adj([vie, boh, mun])
    board["pie"] = pie = Tile("Piedmont")
    pie.set_adj([tyr])
    board["mar"] = mar = Tile("Marseilles")
    mar.set_adj([pie, bur, gas], [pie])
    board["spa"] = spa = MultiCoast("Spain", "North Coast", "South Coast")
    board["spa_nc"] = spa.nc
    board["spa_sc"] = spa.sc
    spa.set_adj([mar, gas])
    spa.nc.set_adj([], [mao, gas])
    spa.sc.set_adj([], [mao, mar])
    board["por"] = por = Tile("Portugal")
    por.set_adj([spa], [mao, spa.nc, spa.sc])
    board["wes"] = wes = Tile("West Mediterranean", False)
    wes.set_adj([], [mao, spa.sc])
    board["naf"] = naf = Tile("North Africa")
    naf.set_adj([], [mao, wes])
    board["lyo"] = lyo = Tile("Gulf of Lyon", False)
    lyo.set_adj([], [spa.sc, mar, pie, wes])
    board["tys"] = tys = Tile("Tyrrhenian Sea", False)
    tys.set_adj([], [lyo, wes])
    board["tun"] = tun = Tile("Tunis")
    tun.set_adj([naf], [naf, wes, tys])
    board["tus"] = tus = Tile("Tuscany")
    tus.set_adj([pie], [pie, lyo, tys])
    board["rom"] = rom = Tile("Rome")
    rom.set_adj([tus], [tus, tys])
    board["nap"] = nap = Tile("Naples")
    nap.set_adj([rom], [rom, tys])
    board["ion"] = ion = Tile("Ionian Sea", False)
    ion.set_adj([], [nap, tun, tys])
    board["apu"] = apu = Tile("Apulia")
    apu.set_adj([nap, rom], [ion, nap])
    board["ven"] = ven = Tile("Venice")
    ven.set_adj([pie, tyr, tus, rom, apu], [apu])
    board["adr"] = adr = Tile("Adriatic Sea", False)
    adr.set_adj([], [ion, ven, apu])
    board["tri"] = tri = Tile("Trieste")
    tri.set_adj([bud, vie, tyr, ven], [ven, adr])
    board["alb"] = alb = Tile("Albania")
    alb.set_adj([tri], [tri, adr, ion])
    board["ser"] = ser = Tile("Serbia")
    ser.set_adj([tri, bud, alb, rum])
    board["gre"] = gre = Tile("Greece")
    gre.set_adj([alb, ser], [alb, ion])
    board["bul"] = bul = MultiCoast("Bulgaria", "East Coast", "South Coast")
    board["bul_ec"] = bul.nc
    board["bul_sc"] = bul.sc
    bul.set_adj([ser, gre, rum])
    bul.nc.set_adj([], rum)
    bul.sc.set_adj([], gre)
    board["bla"] = bla = Tile("Black Sea", False)
    bla.set_adj([], [sev, rum, bul.nc])
    board["con"] = con = Tile("Constantinople")
    con.set_adj([bul], [bul.sc, bul.nc, bla])
    board["aeg"] = aeg = Tile("Aegean Sea", False)
    aeg.set_adj([], [gre, bul.sc, con])
    board["eas"] = eas = Tile("East Mediterranean", False)
    eas.set_adj([], [aeg, ion])
    board["smy"] = smy = Tile("Smyrna")
    smy.set_adj([con], [con, aeg, eas])
    board["ank"] = ank = Tile("Ankara")
    ank.set_adj([con, smy], [con, bla])
    board["arm"] = arm = Tile("Armenia")
    arm.set_adj([smy, ank, sev], [ank, bla, sev])
    board["syr"] = syr = Tile("Syria")
    syr.set_adj([arm, smy], [smy, eas])
    for abbr, tile in board.items():
        tile.abbr = abbr
    supply_centres = ["vie", "bud", "tri", "par", "mar", "bre", "ber", "mun", "kie", "ven", "rom", "nap", "con", "smy",
                      "ank", "mos", "war", "sev", "stp", "lvp", "lon", "edi", "nwy", "swe", "den", "bel", "hol", "spa",
                      "por", "tun", "gre", "bul", "rum", "ser"]
    for sc in supply_centres:
        board[sc].supply = True
    return board


board = createBoard()


# ----------------------------------------------------------------------------------------------------------------------------

# for tile in board.values():
# print("~"+str(tile) +":\nLand: "+str(tile.land_adj)+"\nSea: "+str(tile.sea_adj)+"\n")
class Country(Enum):
    AUSTRIA = "Austria"
    ENGLAND = "England"
    FRANCE = "France"
    GERMANY = "Germany"
    ITALY = "Italy"
    RUSSIA = "Russia"
    TURKEY = "Turkey"


class YN(Enum):
    Y = "yes"
    N = "no"


class Unit(Enum):
    ARMY = 'a'
    FLEET = 'f'


class MoveType(Enum):
    HOLD = "hold"
    MOVE = "move"
    SUPPORT = "support"
    CONVOY = "convoy"


class YesNo(BaseModel):
    yn: YN


class Message(BaseModel):
    to: list[Country]
    body: str


class MessageWithSender:
    sender = None
    to = []
    body = ""

    def __init__(self, message, sender):
        self.to = message.to
        self.body = message.body
        self.sender = sender

    def __str__(self):
        out = "Message from " + self.sender + " to " + self.to[0].value
        if len(self.to) > 1:
            out += " cc "
            for i in range(1, len(self.to)):
                out += self.to[i].value + ", "
            out = out[:-2]
        out += " reads:\n"
        out += self.body
        out += "|\n"
        return out


class UnitLocation(BaseModel):
    utype: Unit
    location: str = Field(description="Map tile this unit is located on. 3 letter string (except for split coasts)")


class Order(BaseModel):
    unit: UnitLocation
    mtype: MoveType
    # Having more than one unitlocation causes a crash that doesn't seem possible to debug
    target_start: str = Field(
        "Map tile the unit targeted starts on. In the case of a move or hold, identical to the units location. Otherwise the tile on which the unit that 'unit' is targetting is located.")
    target_end: str = Field(
        "The tile the unit should end up on for a move or the tile the target should end up on for a support or convoy. Same as target start for a support hold. Unused for simple holds.")


class InvalidOrder(BaseModel):
    reason: str

    def check_validity(self, country):
        return False, self.reason

    def __str__(self):
        return "Malformed Order"


class StrictOrder(BaseModel):
    # A more easy to process format of order. Doesn't guaruntee validity, but does guaruntee that all tiles referenced exist.
    mtype: MoveType
    unit: UnitLocation
    target_start: UnitLocation | None
    target_end: str | None

    def check_validity(self, country):
        # This doesn't guaruntee that the move is 100% possible, just performs some basic sanity checks
        def a_f(x):
            return "a fleet " if x == "f" else "an army "

        tile_self = board[self.unit.location]
        if self.target_start is not None:
            tile_target = board[self.target_start.location]
        if self.target_end is not None:
            tile_end = board[self.target_end]

        if tile_self.unit[1] != country:
            return False, "The selected unit on " + self.unit.location + "is foriegn. You may only order your own units."
        if tile_self.unit[0] != self.unit.utype.value:
            return False, "The selected unit on tile " + self.unit.location + " is " + a_f(
                tile_self.unit[0]) + "not " + a_f(self.unit.utype.value)

        if self.mtype == MoveType.HOLD:
            return True, "Hold is valid"

        if self.mtype != MoveType.MOVE:
            if self.target_start.location == self.unit.location:
                return False, "A unit may not support itself."
        if self.mtype == MoveType.CONVOY and tile_target.unit[0] == "f":
            return False, "You may only convoy armies, not fleets."

        self_adjacent = []
        if self.unit.utype == Unit.FLEET:
            self_adjacent = tile_self.sea_adj
        else:
            self_adjacent = tile_self.land_adj
        if self.mtype == MoveType.MOVE:
            if tile_end not in self_adjacent:
                return False, self.unit.location + " and " + self.target_end + " are not adjacent. " + self.unit.location + " is adjacent to " + str(
                    board[self.unit.location].land_adj) + " by land and " + str(
                    board[self.unit.location].sea_adj) + " by sea."
            else:
                return True, "Move is valid."

        if tile_target.unit[0] == "f":  # TODO: I don't think this logic is entirely correct.
            target_adjacent = tile_target.sea_adj
        else:
            target_adjacent = tile_target.land_adj
        if self.unit.utype == Unit.FLEET:
            # Checks if a unit can actually support the target eg an army can't wade across an ocean to support a fleet
            supportable_adjacent = tile_target.sea_adj + tile_target.land_adj
        else:
            supportable_adjacent = tile_target.land_adj

        if self.mtype == MoveType.SUPPORT:
            if self.target_start.location == self.unit.location:
                return False, "A unit may not support itself."
            if tile_target not in self_adjacent:
                return False, self.unit.location + " and " + self.target_start.location + " are not adjacent. " + self.unit.location + " is adjacent to " + str(
                    board[self.unit.location].land_adj) + " by land and " + str(
                    board[self.unit.location].sea_adj) + " by sea."
            elif self.target_start.location == self.target_end:
                return True, "Support Hold is valid."
            elif tile_end not in target_adjacent:
                return False, self.target_start.location + " and " + self.target_end + " are not adjacent. " + self.target_start.location + " is adjacent to " + str(
                    board[self.target_start.location].land_adj) + " by land and " + str(
                    board[self.target_start.location].sea_adj) + " by sea."
            elif tile_end not in supportable_adjacent:
                return False, a_f(
                    self.unit.utype) + " is unable to support " + self.target_start.location + " to " + self.target_end + " as " + a_f(
                    self.unit.utype) + " cannot move to that tile."
            else:
                return True, "Support is valid."

        def find_convoy_tile(target, start):
            valid = [start.adjacent]
            checked = []
            while len(valid) > 0:
                new_valid = []
                for tile in valid:
                    if tile == target:
                        return True
                    if tile.unit[0] == "f" and tile not in checked:
                        new_valid.append(tile)
                    checked.append(tile)
                valid = new_valid
            return False

        # Move Type is Convoy
        if tile_target not in self_adjacent:
            if not find_convoy_tile(tile_target, tile_self):
                return False, self.unit.location + " and " + self.target_start.location + " are not adjacent, and there isn't a path of fleets between them."
        if tile_end not in self_adjacent:
            if not find_convoy_tile(tile_end, tile_self):
                return False, self.unit.location + " and " + self.target_start.location + " are not adjacent, and there isn't a path of fleets between them."
        return True, "Convoy is valid."

    def __str__(self):
        match self.mtype:
            case MoveType.HOLD:
                return self.unit.utype.value + " " + self.unit.location + " holds"
            case MoveType.MOVE:
                return self.unit.utype.value + " " + self.unit.location + " - " + self.target_end
            case MoveType.SUPPORT:
                return self.unit.utype.value + " " + self.unit.location + " supports " + self.target_start.utype.value + " " + self.target_start.location + " - " + self.target_end
            case MoveType.CONVOY:
                return self.unit.utype.value + " " + self.unit.location + " convoys a " + self.target_start.location + " - " + self.target_end


def convert_order_to_strict(order):
    global board

    def try_simple_fixes(tile_code):
        tile_code = tile_code.lower()
        if tile_code in board.keys():
            return tile_code
        if tile_code[2:] in board.keys():
            return tile_code[2:]
        # Nuclear option
        tile_code = tile_code.title()
        for tile in board.values():
            if tile.name == tile_code:
                return tile.abbr
        return None

    if order.unit.location not in board.keys():
        fix = try_simple_fixes(order.unit.location)
        if fix is None:
            return InvalidOrder(
                reason=order.unit.location + " is not a recognised tile, please refer to the list provided.")
        else:
            order.unit.location = fix
    if board[order.unit.location].unit is None:
        return InvalidOrder(reason="There is no unit present on tile " + order.unit.location + ".")
    if order.mtype == MoveType.HOLD:
        return StrictOrder(
            mtype=MoveType.HOLD,
            unit=order.unit,
            target_start=None,
            target_end=None,
        )
    if order.target_end not in board.keys():
        fix = try_simple_fixes(order.target_end)
        if fix is None:
            return InvalidOrder(
                reason=order.target_end + " is not a recognised tile, please refer to the list provided.")
        else:
            order.target_end = fix
    if order.mtype == MoveType.MOVE:
        return StrictOrder(
            mtype=MoveType.MOVE,
            unit=order.unit,
            target_start=None,
            target_end=order.target_end,
        )
    if order.target_start not in board.keys():
        fix = try_simple_fixes(order.target_start)
        if fix is None:
            return InvalidOrder(
                reason=order.target_start + " is not a recognised tile, please refer to the list provided.")
        else:
            order.target_start = fix
    if board[order.target_start].unit is None:
        return InvalidOrder(reason="There is no unit present on tile " + order.target_start + ".")
    return StrictOrder(
        mtype=order.mtype,
        unit=order.unit,
        target_start=UnitLocation(utype=board[order.target_start].unit[0], location=order.target_start),
        target_end=order.target_end,
    )


class Discussion(BaseModel):
    messages: list[Message]
    turn_readiness: float = Field(
        description="A confidence interval between 0 and 1 on how confident you are that you have finished discussion and are ready to move on")


class Orders(BaseModel):
    orders: list[Order] = Field(description="An order for each of your units.")


class Retreat(BaseModel):
    destination: str = Field(description="Map tile this unit should retreat to, or DISBAND to delete it")


class Build(BaseModel):
    builds: list[UnitLocation] = Field(description="List of new units to be built this turn.")

    def __str__(self):
        return "Building units: " + str(self.builds)


class Disband(BaseModel):
    disbands: list[UnitLocation] = Field(description="List of locations of units to remove this turn.")

    def __str__(self):
        return "Disbanding units: " + str(self.disbands)


class Voice:
    RE_TILES = " (" + "".join((t + "|" if len(t) == 3 else "") for t in board.keys()) + ") "
    RE_UNIT_TILES = re.compile("([af])" + RE_TILES)
    RE_TILES = re.compile(RE_TILES)
    AVAILABLE = {
        'Austria': [('streamElements', 'Michael'), ('streamElements', 'Karsten'), ('streamElements', 'Szabolcs'),
                    ('streamElements', 'hu-HU-Wavenet-A'), ('gTTS', 'hu hu')],
        'Austria_at': [('streamElements', 'Michael'), ('streamElements', 'Karsten')],
        'Austria_hu': [('streamElements', 'Szabolcs'), ('streamElements', 'hu-HU-Wavenet-A'), ('gTTS', 'hu hu')],
        'England': [('streamElements', 'Sean'), ('gTTS', 'en co.uk'), ('streamElements', 'Emma'),
                    ('streamElements', 'Geraint'), ('streamElements', 'Amy'), ('streamElements', 'en-GB-Wavenet-A'),
                    ('streamElements', 'en-GB-Wavenet-B')],
        'France': [('streamElements', 'Mathieu'), ('streamElements', 'Celine'), ('streamElements', 'Chantal'),
                   ('streamElements', 'Guillaume'), ('streamElements', 'fr-CA-Standard-A'),
                   ('streamElements', 'fr-CA-Standard-B'), ('streamElements', 'fr-CA-Standard-C'),
                   ('streamElements', 'fr-CA-Standard-D'), ('streamElements', 'fr-FR-Wavenet-A'),
                   ('streamElements', 'fr-FR-Wavenet-B'), ('gTTS', 'fr fr'), ('gTTS', 'fr ca')],
        'Germany': [('streamElements', 'Hans'), ('streamElements', 'Marlene'), ('streamElements', 'Vicki'),
                    ('streamElements', 'de-DE-Wavenet-B'), ('streamElements', 'de-DE-Wavenet-A'), ('gTTS', 'de de')],
        'Italy': [('streamElements', 'Carla'), ('streamElements', 'Bianca'), ('streamElements', 'Giorgio'),
                  ('streamElements', 'it-IT-Wavenet-A'), ('streamElements', 'it-IT-Wavenet-C'),
                  ('streamElements', 'it-IT-Wavenet-D'), ('gTTS', 'it it')],
        'Russia': [('streamElements', 'Maxim'), ('streamElements', 'Tatyana'), ('streamElements', 'ru-RU-Wavenet-A'),
                   ('streamElements', 'ru-RU-Wavenet-B'), ('streamElements', 'ru-RU-Wavenet-C'),
                   ('streamElements', 'ru-RU-Wavenet-D'), ('gTTS', 'ru ru')],
        'Turkey': [('streamElements', 'Filiz'), ('streamElements', 'tr-TR-Wavenet-A'),
                   ('streamElements', 'tr-TR-Wavenet-B'), ('streamElements', 'tr-TR-Wavenet-C'),
                   ('streamElements', 'tr-TR-Wavenet-D'), ('streamElements', 'tr-TR-Wavenet-E'), ('gTTS', 'tr com.tr')],
        'Misc': [('pyttsx', 0), ('pyttsx', 1), ('streamElements', 'Heather'), ('streamElements', 'Linda'),
                 ('streamElements', 'Raveena'), ('streamElements', 'Salli'), ('streamElements', 'Kimberly'),
                 ('streamElements', 'Kendra'), ('streamElements', 'Joanna'), ('streamElements', 'Ivy'),
                 ('streamElements', 'Matthew'), ('streamElements', 'Justin'), ('streamElements', 'Joey'),
                 ('streamElements', 'Nicole'), ('streamElements', 'Russell'), ('streamElements', 'Brian'),
                 ('streamElements', 'en-US-Wavenet-A'), ('streamElements', 'en-US-Wavenet-B'),
                 ('streamElements', 'en-US-Wavenet-C'), ('streamElements', 'en-US-Wavenet-D'),
                 ('streamElements', 'en-US-Wavenet-E'), ('streamElements', 'en-US-Wavenet-F'),
                 ('streamElements', 'en-AU-Wavenet-A'), ('streamElements', 'en-AU-Wavenet-B'),
                 ('streamElements', 'en-AU-Wavenet-C'), ('streamElements', 'en-AU-Wavenet-D'),
                 ('streamElements', 'en-AU-Standard-D'), ('gTTS', 'en com.au'), ('gTTS', 'en ca'), ('gTTS', 'en co.nz'),
                 ('gTTS', 'en co.in')]}
    service = None
    name = None

    def __init__(self, service, name):
        self.service = service
        self.name = name
        if service == "pyttsx":
            self.xEngine = pyttsx3.init()
            self.xEngine.setProperty('voice', self.xEngine.getProperty('voices')[self.name].id)
        if service == "gTTS":
            name = name.split(" ")
            self.lang = name[0]
            self.tld = name[1]

    def __repr__(self):
        return '{"service": "' + self.service + '", "name": "' + self.name + '"}'

    @staticmethod
    def clean(txt):
        txt = txt.lower()
        txt = txt.replace("stp_sc", "stp")
        txt = txt.replace("stp_nc", "stp")
        txt = txt.replace("spa_sc", "spa")
        txt = txt.replace("spa_nc", "spa")
        txt = txt.replace("bul_sc", "bul")
        txt = txt.replace("bul_ec", "bul")
        txt = txt.replace("->","to")
        txt = txt.replace(" - ", "to")
        global board
        while match := re.search(Voice.RE_UNIT_TILES, txt):
            i = match.span()[0]
            txt = txt[:i] + ("army" if txt[i] == "a" else "fleet") + txt[i+1:]
        while match := re.search(Voice.RE_TILES, txt):
            i = match.span()[0]
            txt = txt[:i+1] + board[txt[i+1: i+4]].name + txt[i + 4:]
        return txt

    def say(self, txt):
        txt = self.clean(txt)
        if self.service == "streamElements":
            response = requests.get("https://api.streamelements.com/kappa/v2/speech",
                                    params={"voice": self.name, "text": txt})
            fo = open("generated_audio.wav", "wb")
            fo.write(response.content)
            fo.close()
            self.pyGamePlay()
        elif self.service == "gTTS":
            gResult = gTTS(txt, lang=self.lang, tld=self.tld)
            gResult.save("generated_audio.wav")
            self.pyGamePlay()
        elif self.service == "pyttsx":
            self.xEngine.say(txt)
            self.xEngine.runAndWait()

    def pyGamePlay(self):
        sound = mixer.Sound("generated_audio.wav")
        channel = sound.play()
        while channel.get_busy():
            sleep(0.2)


class Player(SimpleNamespace):
    global board
    ui = False
    armies = None
    fleets = None
    home_supply = None
    owned_tiles = None
    country = ""
    message_queue = []
    orders = None

    def __init__(self, country, createUnits=True, ui=False):
        self.country = country
        self.orders = []
        self.home_supply = []
        self.ui = ui
        match country:
            case "Austria":
                self.home_supply = [board["vie"], board["bud"], board["tri"]]
            case "France":
                self.home_supply = [board["par"], board["mar"], board["bre"]]
            case "Germany":
                self.home_supply = [board["mun"], board["ber"], board["kie"]]
            case "Italy":
                self.home_supply = [board["ven"], board["rom"], board["nap"]]
            case "Turkey":
                self.home_supply = [board["con"], board["smy"], board["ank"]]
            case "Russia":
                self.home_supply = [board["mos"], board["war"], board["sev"], board["stp"]]
            case "England":
                self.home_supply = [board["lvp"], board["lon"], board["edi"]]
            case _:
                raise Exception("Invalid Country")
        if createUnits:
            match country:
                case "Austria":
                    self.armies = [board["vie"].set_unit(("a", country)), board["bud"].set_unit(("a", country))]
                    self.fleets = [board["tri"].set_unit(("f", country))]
                case "France":
                    self.armies = [board["par"].set_unit(("a", country)), board["mar"].set_unit(("a", country))]
                    self.fleets = [board["bre"].set_unit(("f", country))]
                case "Germany":
                    self.armies = [board["ber"].set_unit(("a", country)), board["mun"].set_unit(("a", country))]
                    self.fleets = [board["kie"].set_unit(("f", country))]
                case "Italy":
                    self.armies = [board["ven"].set_unit(("a", country)), board["rom"].set_unit(("a", country))]
                    self.fleets = [board["nap"].set_unit(("f", country))]
                case "Turkey":
                    self.armies = [board["con"].set_unit(("a", country)), board["smy"].set_unit(("a", country))]
                    self.fleets = [board["ank"].set_unit(("f", country))]
                case "Russia":
                    self.armies = [board["mos"].set_unit(("a", country)), board["war"].set_unit(("a", country))]
                    self.fleets = [board["sev"].set_unit(("f", country)), board["stp_sc"].set_unit(("f", country))]
                case "England":
                    self.armies = [board["lvp"].set_unit(("a", country))]
                    self.fleets = [board["lon"].set_unit(("f", country)), board["edi"].set_unit(("f", country))]
                case _:
                    raise Exception("Invalid Country")
            self.owned_tiles = self.home_supply.copy()
        else:
            self.owned_tiles = []
            self.armies = []
            self.fleets = []

    def add_army(self, tile):
        if tile not in board or not board[tile].land:
            return False
        else:
            self.armies.append(board[tile].set_unit(("a", self.country)))

    def add_fleet(self, tile):
        if tile not in board or (board[tile].land and board[tile].sea_adj == []):
            return False
        else:
            self.fleets.append(board[tile].set_unit(("f", self.country)))

    def remove_unit(self, tile):
        if tile not in board:
            return False
        else:
            t = board[tile]
            if t.unit[1] != self.country:
                return False
            else:
                if t.unit[0] == "a":
                    self.armies.remove(t)
                else:
                    self.fleets.remove(t)
                t.unit = None
                return True

    def remove_all_units(self):
        for tile in self.armies + self.fleets:
            tile.unit = None
        self.armies = []
        self.fleets = []

    def set_units(self, commands):
        # takes a list of string commands eg "a bud" and converts them to units.
        self.remove_all_units()
        for command in commands:
            command = command.split(" ")
            if command[0] == "a":
                self.add_army(command[1])
            elif command[0] == "f":
                self.add_fleet(command[1])
            else:
                # Make an assumption about what type of unit to add DO NOT DO THIS IF FORWARD CONSISTENCY IS REQUIRED.
                # This is used just to ask the AI to disband a unit. I don't feel morally wrong telling them they have an army instead of a fleet sometimes.
                if board[command[0]].land:
                    self.add_army(command[0])
                else:
                    self.add_fleet(command[0])

    def prompt(self, message):
        raise NotImplementedError

    def submitted(self):
        return self.orders == ""

    def system_message(self, message):
        if self.ui:
            socketio.emit("add_press", {"type": "banner", "text": message})


class Game(SimpleNamespace):
    global board
    VALID_TILES = "The codes for provinces used by the system are as follows: nao, nwg, bar, stp, stp_nc, stp_sc, fin, bot, swe, nwy, ska, nth, edi, cly, lvp, iri, yor, hel, den, bal, lvn, mos, war, pru, ber, kie, hol, bel, pic, bre, mao, eng, wal, lon, gas, par, bur, ruh, mun, boh, sil, gal, ukr, sev, rum, bud, vie, tyr, pie, mar, spa, spa_nc, spa_sc, por, wes, naf, lyo, tys, tun, tus, rom, nap, ion, apu, ven, adr, tri, alb, ser, gre, bul, bul_ec, bul_sc, bla, con, aeg, eas, smy, ank, arm, syr"
    # board_state = "Austria:\na bud\nf tri\na vie\nEngland:\nf edi\nf lon\na lvp\nFrance:\nf bre\na mar\na par\nGermany:\na ber\nf kie\na mun\nItaly:\nf nap\na rom\na ven\nRussia:\na mos\nf sev\nf stp_sc\na war\nTurkey:\nf ank\na con\na smy"
    turn = 0
    players = {}  # This is a class property not an object property, but since it doesn't make sense to have more than one game this is fine.
    # supply_control = {"Austria": ["vie","bud","tri"], "England": ["edi","lon","lvp"], "France": ["bre","mar","par"], "Germany": ["ber","kie","mun"], "Italy": ["nap","rom","ven"], "Russia": ["mos","sev","stp","war"], "Turkey": ["ank","con","smy"], "Unoccupied": ["bel","hol","nwy","swe","spa","por","tun","rum","bul","gre","den"]}
    supply_control = {"Austria": {"vie", "bud", "tri", "ser"}, "England": {"edi", "lon", "lvp", "hol"},
                      "France": {"bre", "mar", "par"}, "Germany": {"ber", "kie", "mun", "den"},
                      "Italy": {"nap", "rom", "ven"}, "Russia": {"mos", "sev", "stp", "war", "swe"},
                      "Turkey": {"ank", "con", "smy", "bul"},
                      "Unoccupied": {"bel", "nwy", "spa", "por", "tun", "rum", "gre"}}

    def supply_control_str(self):
        supply = "Control of supply centres is as follows: "
        for country, centres in self.supply_control.items():
            supply += country + ": "
            for centre in centres:
                supply += centre + ", "
        return supply[:-2]

    def board_state(self):
        out = "The current state of the board is:\n"
        for country in self.players.keys():
            out += country + ":\n"
            for army in self.players[country].armies:
                out += "a " + army.abbr + "\n"
            for fleet in self.players[country].fleets:
                out += "f " + fleet.abbr + "\n"
        return out

    def start_turn(self):
        season = "Spring" if self.turn % 3 == 0 else "Autumn" if self.turn % 3 == 1 else "Winter"
        return f"It is turn {self.turn + 1}; {season} {self.turn // 3 + 1901}\n{self.board_state()}\n" + (
            "Units on supply centres at this end of this turn will capture them.\n" if season == "Autumn" else "")


game = Game()


class OpenAIPlayer(Player):
    global board
    global game
    message_queue = None
    history = None
    last_polled = time()

    def __init__(self, country, api_key, model, api_url="", random_voice=True, personality="", ui=False):
        super().__init__(country, ui=ui)
        self.message_queue = []
        self.history = []

        # history_file = open("history/" + country + ".txt", "r")
        # self.history = json.loads(history_file.read())
        # history_file.close()

        self.system_prompt = f"You are playing a game of diplomacy as {country}. {personality} "
        if api_url == "":
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI(api_key=api_key, base_url=api_url)
        self.model = model

        if random_voice:
            if random.random() < 0.7:
                v = random.choice(Voice.AVAILABLE[country])
            else:
                v = random.choice(Voice.AVAILABLE["Misc"])
        else:
            match country:
                case "Austria":
                    v = ("streamElements", "Szabolcs")
                case "France":
                    v = ("streamElements", "fr-CA-Standard-C")
                case "Germany":
                    v = ("streamElements", "de-DE-Wavenet-B")
                case "Italy":
                    v = ('streamElements', 'it-IT-Wavenet-C')
                case "Turkey":
                    v = ("streamElements", "tr-TR-Wavenet-E")
                case "Russia":
                    v = ('streamElements', 'ru-RU-Wavenet-A')
                case "England":
                    v = ("gTTS", "en co.uk")
        self.voice = Voice(v[0], v[1])

    def system_message(self, message):
        super().system_message(message)
        self.history.append({"role": "user", "content": message})

    def dump_history(self):
        history_file = open("history/" + self.country + ".txt", "w")
        history_file.write(json.dumps(self.history))
        history_file.close()

    def prompt(self, text, response_format):
        if text == "":
            return None
        if time() - OpenAIPlayer.last_polled < 4.1:
            sleep(4.1 - (time() - OpenAIPlayer.last_polled))
        OpenAIPlayer.last_polled = time()

        completion = None
        while completion == None:
            try:
                completion = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                                 {"role": "developer", "content": self.system_prompt}] +
                             self.history +
                             [{"role": "user", "content": text}],
                    response_format=response_format,
                )
            except Exception as e:
                print(e)
                sleep(10)
        return completion.choices[0].message.parsed

    def gen_discussion(self):
        if self.orders != []:
            if self.message_queue == []:
                # Don't bother generating a discussion if there's nothing to respond to.
                return 1
            answer = self.prompt("You have submitted your orders for this turn, do you want to respond to the " + str(
                len(self.message_queue)) + " message(s) in the queue.", YesNo)
            if answer.yn == YN.N:
                # print("Does not want to communicate further")
                return 1

        # Generate the response from the AI.
        message_text = ""
        prompt_text = game.start_turn() + game.supply_control_str()
        if len(self.message_queue) > 0:
            prompt_text += "\n"
            for message in self.message_queue:
                message_text += str(message)
                if self.ui:
                    # print(str(message))
                    socketio.emit("update_screen", {"country_image": message.sender + ".svg", "model_image": [
                        random.choice(["ChatGPT_White.svg", "DeepSeek.svg", "Gemini.svg", "Google.svg"])]})
                    socketio.emit("add_press",
                                  {"type": "message", "sender": message.sender,
                                   "recipients": [country.name.title() for country in message.to],
                                   "body": message.body})
                    game.players[message.sender].voice.say(message.body)
                    socketio.emit("update_screen", {"screen": "off"})
                    sleep(2)
            prompt_text += message_text
        else:
            prompt_text += "You have no new messages, what would you like to send?"
        discussion = self.prompt(prompt_text, Discussion)

        # Update and clear message history.
        if self.message_queue != []:
            self.history.append({"role": "user", "content": message_text})
        response = ""
        for message in discussion.messages:
            response += "[Message sent to "
            for country in message.to:
                response += country.value + ", "
            response = response[:-2] + "]| " + message.body + "\n"
        # response += "Readiness: " + str(discussion.turn_readiness)
        self.history.append({"role": "assistant", "content": response})
        self.message_queue = []

        # Process Discusion, send messages to correct places.
        for message in discussion.messages:
            message = MessageWithSender(message, self.country)
            if self.ui:
                socketio.emit("add_press",
                              {"type": "message", "sender": self.country,
                               "recipients": [country.name.title() for country in message.to],
                               "body": message.body})
            for country in message.to:
                game.players[country.value].message_queue.append(message)

        return discussion.turn_readiness

    def gen_orders(self):
        prompt_text = game.start_turn() + game.supply_control_str() + ". " + game.VALID_TILES + ". Please submit your orders for this turn."
        orders = self.prompt(prompt_text, Orders)
        for unused in range(3):
            # print(orders)
            # Give the AI 3 attempts to make a valid set of moves
            errs = []
            current_attempt = []
            history_string = "Submit:\n"
            for o in orders.orders:
                a = convert_order_to_strict(o)
                current_attempt.append(a)
                valid, reason = a.check_validity(self.country)
                if not valid:
                    errs.append(reason)
                history_string += str(a) + ", "

            # print(current_attempt)
            # print(errs)
            self.history.append({"role": "assistant", "content": history_string})
            if len(errs) == 0:
                break
            else:
                prompt_text = game.start_turn() + game.supply_control_str() + ". " + game.VALID_TILES + ". Some of your orders have errors, please reveiw your orders, Errors:" + str(
                    errs)
                orders = self.prompt(prompt_text, Orders)
                self.history = self.history[:-1]

        self.orders = current_attempt
        return current_attempt

    def gen_retreat(self, tile, options):
        prompt_text = "Your " + "unit" + " in " + tile + " has been dislodged please retreat the unit to one of the following options" + str(
            options)
        return self.prompt(prompt_text, Retreat)

    def gen_winter(self, num_units, tiles):
        if "stp sc nc" in tiles:
            tiles.remove("stp sc nc")
            tiles.append("stp")
            tiles.append("stp_nc")
            tiles.append("stp_sc")
        if num_units > 0:
            num_builds = min(len(tiles), num_units)
            prompt_text = game.start_turn() + "Please build new units on " + str(
                num_builds) + " of the following tiles: " + str(tiles) + (
                              ". Reminder you can ONLY build on ONE of the stp tiles, as one unit covers all 3" if "stp" in tiles else "")
            return self.prompt(prompt_text, Build)
        else:
            self.set_units(tiles)
            num_units = -num_units
            prompt_text = game.start_turn() + "You've lost " + str(num_units) + " supply centres. Please select " + str(
                num_units) + " units to disband."
            return self.prompt(prompt_text, Disband)


def adjudicate(orders):
    global board
    global game
    # print("Adjudicating")
    valid_orders = {}
    for key, order_list in orders.items():
        # print(key)
        new_order_list = []
        doneTiles = []
        for order in order_list:
            if type(order) == Order:
                order = convert_order_to_strict(order)
            # print(order, order.check_validity(key))
            if type(order) != InvalidOrder:
                if order.check_validity(key)[0] == False:
                    if board[order.unit.location].unit[1] == key:
                        new_order = StrictOrder(mtype=MoveType.HOLD,
                                                unit=UnitLocation(
                                                    utype=board[order.unit.location].unit[0],
                                                    location=order.unit.location),
                                                target_start=None,
                                                target_end=None)
                        if new_order.unit.location not in doneTiles:
                            doneTiles.append(new_order.unit.location)
                            new_order_list.append(new_order)
                else:
                    if order.unit.location not in doneTiles:
                        doneTiles.append(order.unit.location)
                        new_order_list.append(order)
                        valid_orders[key] = new_order_list

    for key, order_list in valid_orders.items():
        unit_tiles = set()
        for tile in game.players[key].armies:
            unit_tiles.add(tile.abbr)
        for tile in game.players[key].fleets:
            unit_tiles.add(tile.abbr)
        order_tiles = set()
        for order in order_list:
            order_tiles.add(order.unit.location)
        for tile in (unit_tiles - order_tiles):
            valid_orders[key].append(StrictOrder(mtype=MoveType.HOLD,
                                                 unit=UnitLocation(
                                                     utype=board[tile].unit[0],
                                                     location=tile),
                                                 target_start=None,
                                                 target_end=None))

    '''print("\nValids")
    for key, order_list in valid_orders.items():
        print(key)
        for order in order_list:
            print(order, order.check_validity(key))'''
    return valid_orders.values()


OPENAI_KEY = environ["OPENAI_API_KEY"]
GEMINI_KEY = environ["GEMINI_API_KEY"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

game.players = {
    "England": OpenAIPlayer("England", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    "Austria": OpenAIPlayer("Austria", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False,
                            personality=get_personality(1), ui=True),
    "Italy": OpenAIPlayer("Italy", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False, personality=get_personality(1)),
    "Turkey": OpenAIPlayer("Turkey", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False, personality=get_personality(1)),
    "Germany": OpenAIPlayer("Germany", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False, personality=get_personality(1)),
    "Russia": OpenAIPlayer("Russia", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False, personality=get_personality(1)),
    "France": OpenAIPlayer("France", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False, ),
}
# Set up Selenium.
driver = webdriver.Chrome()
driver.get("https://www.backstabbr.com/")
bs = open("../backstabbr.txt")
session_cookie = bs.readline()
bs.close()
driver.add_cookie({"name": "session", "value": session_cookie})
driver.get("https://www.backstabbr.com/sandbox/5114939252277248/")
actions = ActionChains(driver)

'''import pickle

fo = open("history/dill.dat", "rb")
orders = pickle.load(fo)
fo.close()
print(orders)'''


# Selenium Functions
def click_tile(abbr):
    if abbr[3:] == "_nc" or abbr[3:] == "_sc" or abbr[3:] == "_ec":
        abbr = abbr[:-3]
    xoffset = 0
    yoffset = 0
    match abbr:
        case "bar":
            xoffset = 20
            yoffset = -50
        case "bot":
            yoffset = 10
            xoffset = -30
        case "nwy":
            xoffset = -20
        case "lvp":
            xoffset = 10
        case "pru":
            yoffset = 10
        case "mao":
            yoffset = -100
        case "sev":
            yoffset = -50
        case "rum":
            xoffset = 10
    board_tile = board[abbr]
    tile_id = "ter_"
    if board_tile.land:
        tile_id += abbr.title()
    else:
        tile_id += abbr.upper()
    tile = driver.find_element(By.ID, tile_id)
    actions.move_to_element_with_offset(tile, xoffset, yoffset).click().perform()


def submit_orders():
    driver.find_element(By.ID, "submit_orders_button").send_keys(Keys.ENTER)


def screenshot_map():
    # driver.maximize_window()
    x = driver.find_element(By.TAG_NAME, "svg")
    y = x.screenshot_as_png
    fo = open("static/map.png", "wb")  # I know this isn't static anymore because we're changing it but nobody tell
    # flask and we'll be ok.
    fo.write(y)
    fo.close()
    print("refreshing")
    socketio.emit("refresh_map", {})


def get_map_state():
    order_box = driver.find_element(By.ID, "orders-text")
    map_state = ""
    for row in order_box.find_elements(By.XPATH, "//tr"):
        country = row.find_element(By.CLASS_NAME, "country").text
        if country == "":
            continue
        else:
            map_state += country + "\n"
            for order in row.find_elements(By.CLASS_NAME, "orderstring"):
                order_txt = order.text.lower()
                order_txt = order_txt.replace("/", "_")
                map_state += "\t" + order_txt + "\n"
    screenshot_map()
    return map_state


# Use selenium to input the orders into backstabbr, and then retreive the results.
def end_season(orders):
    global game
    global board
    socketio.emit("add_press", {"type": "banner", "text": "Orders are in: Adjudicating..."})
    orders = adjudicate(orders)
    # Input Orders
    start_season = driver.find_element(By.ID, "history_current_season")
    start_season = start_season.text.split(" ")[0]
    for o in orders:
        for order in o:
            # sleep(0.5)
            if order.mtype == MoveType.HOLD:
                click_tile(order.unit.location)
                click_tile(order.unit.location)
            elif order.mtype == MoveType.MOVE:
                click_tile(order.unit.location)
                click_tile(order.target_end)
            else:
                click_tile(order.unit.location)
                click_tile(order.target_start.location)
                if order.mtype == MoveType.SUPPORT:
                    button = driver.find_element(By.ID, "order_button_support")
                else:
                    button = driver.find_element(By.ID, "order_button_convoy")
                button.click()
                click_tile(order.target_end)

    # Submit Orders
    submit_orders()

    sleep(0.5)
    # Grab Results & Take Screenshot
    actions.move_to_element(driver.find_element(By.ID, "history_previous_season")).click().perform()
    results = get_map_state()
    for player in game.players.values():
        player.system_message(results)

    # Grab Current Board State
    actions.move_to_element(driver.find_element(By.ID, "history_next_season")).click().perform()

    season = driver.find_element(By.ID, "history_current_season")
    season = season.text.split(" ")[0]

    if season == start_season:
        # We have not moved forward, At least one unit must retreat
        for danger in driver.find_elements(By.CLASS_NAME, "text-danger"):
            country = danger.find_element(By.XPATH, "ancestor::tr//div[@class='country']").text
            select = danger.find_element(By.XPATH, "following-sibling::select")
            tile = select.get_attribute("territory").lower()
            options = ["DISBAND"]
            for option in select.find_elements(By.TAG_NAME, "option"):
                option = option.get_attribute("value")
                if option not in ["", "DISBAND"]:
                    options.append(option.lower())
            retreat = game.players[country].gen_retreat(tile, options).destination
            select = Select(select)
            if retreat.upper() == "DISBAND":
                select.select_by_value(retreat.upper())
            else:
                select.select_by_value(retreat.title())
        submit_orders()
        season = driver.find_element(By.ID, "history_current_season")
        season = season.text.split(" ")[0]

    if season == "WINTER":
        game.turn += 1
        for row in driver.find_elements(By.CSS_SELECTOR, "#orders-text tr"):
            try:
                country = row.find_element(By.CLASS_NAME, "country").text
            except NoSuchElementException:
                country = ""
            if country == "":
                continue
            else:
                i = 0
                tiles = []
                num_builds = 0
                for line in row.find_element(By.TAG_NAME, "td").text.split("\n"):
                    # print("\t"+str(i)+"\t"+line)
                    if line == "":
                        break
                    else:
                        if i == 0:
                            if line[-7:] == "builds.":
                                num_builds = int(line[6])
                            else:
                                num_builds = - int(line[4])
                        elif i == 1:
                            pass
                        else:
                            if len(line) < 10:
                                # Line length greater than 10 shows "occupied" is in the line and it is impossible to
                                # build on this tile
                                tiles.append(line.lower())
                    i += 1

                if num_builds != 0:
                    change = game.players[country].gen_winter(num_builds, tiles)
                    if num_builds > 0:
                        ulocs = change.builds
                    else:
                        ulocs = change.disbands
                    i = 1
                    for uloc in ulocs:
                        if i > abs(num_builds):
                            break
                        if num_builds > 0:
                            if uloc.location in ["stp_sc", "stp_nc"]:
                                radio_id = uloc.location[:3].title() + "_" + uloc.utype.value.upper() + uloc.location[
                                                                                                        3:]
                            else:
                                radio_id = uloc.location.title() + "_" + uloc.utype.value.upper()
                        else:
                            loc = uloc.location[:3]
                            if board[loc].land:
                                loc = loc.title()
                            else:
                                loc = loc.upper()
                            radio_id = "disband_" + loc

                        try:
                            actions.move_to_element(driver.find_element(By.ID, radio_id)).click().perform()
                        except:
                            pass
                            # The AI generally doesn't have a hard time producing valid winter turns. if so, too bad!
                        i += 1

        submit_orders()
        sleep(1)
        actions.move_to_element(driver.find_element(By.ID, "history_previous_season")).click().perform()
        print(get_map_state())

        # Grab Current Board State
        actions.move_to_element(driver.find_element(By.ID, "history_next_season")).click().perform()

    order_box = driver.find_element(By.ID, "orders-text")
    for row in order_box.find_elements(By.XPATH, "//tr"):
        country = row.find_element(By.CLASS_NAME, "country").text
        if country == "":
            continue
        else:
            print(country)
            units = []
            for order in row.find_elements(By.CLASS_NAME, "orderstring"):
                order_txt = order.text.lower()
                order_txt = order_txt.replace("/", "_")
                units.append(order_txt)
                print("\t" + order_txt)
            game.players[country].set_units(units)
    game.turn += 1


def main():
    sleep(5)
    input("Press Enter to Start")
    screenshot_map()
    socketio.emit("add_press", {"type": "banner", "text": "Spring 1901"})
    gamers = [x for x in game.players.keys()]
    SPEAKING_TURNS = 2  # 20

    for j in range(5):
        submitted = set()
        print(game.start_turn())
        for i in range(SPEAKING_TURNS + 1, 0, -1):
            if len(submitted) == 7:
                break
            # print("Threshold:", i / SPEAKING_TURNS)
            # print(submitted)
            last_moved = gamers[-1]
            while gamers[0] == last_moved:
                gamers = gamers.suffle()

            for x in gamers:
                # print(x)
                # print(game.players[x].message_queue)
                y = game.players[x].gen_discussion()
                if x == "Austria":
                    print(y)
                # print(game.players[x].history)  # [-1]["content"])
                # print(y)
                if y >= i / SPEAKING_TURNS and x not in submitted:
                    print(game.players[x].gen_orders())
                    submitted.add(x)
                    if len(submitted) == 7:
                        break
        orders = {}
        for country in gamers:
            orders[country] = game.players[country].orders
            game.players[country].message_queue = []
            game.players[country].orders = []
        end_season(orders)



main_thread = threading.Thread(target=main)
main_thread.start()
socketio.run(app, allow_unsafe_werkzeug=True)
