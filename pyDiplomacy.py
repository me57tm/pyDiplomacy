# Deepseek, GPT 4o, Gemini, Azure AI Service (phi)????, MEta LLama, Grok? there's also one called claude
from gtts import gTTS
import pyttsx3
import requests
import random
import json
from pygame import mixer
from time import sleep
from os import environ
from openai import OpenAI

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
        return self.name

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


class CoastOnly(Tile):
    parent = None

    def __init__(self, name, parent, unit=None):
        super().__init__(name, False, unit)
        self.parent = parent

    def set_unit(self, unit):
        self.parent.set_unit(unit)
        self.unit = unit


class MultiCoast(Tile):
    nc = None
    sc = None

    def __init__(self, name, nc_name, sc_name, unit=None, unit_location="l"):
        super().__init__(name, True, unit)
        self.adj = []
        self.nc = CoastOnly(name + " " + nc_name, self)
        self.sc = CoastOnly(name + " " + sc_name, self)


class GameController:
    armies = None
    fleets = None
    home_supply = None
    owned_tiles = None

    def __init__(self, a=None):
        self.armies = []
        self.fleets = []
        self.home_supply = []
        self.owned_tiles = []


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


# ----------------------------------------------------------------------------------------------------------------------------

# for tile in board.values():
# print("~"+str(tile) +":\nLand: "+str(tile.land_adj)+"\nSea: "+str(tile.sea_adj)+"\n")

class Voice():
    AVALIBLE = {
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

    def say(self, txt):
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


class Player:
    country = ""
    turn = 0
    gc = None
    submitted = False

    def __init__(self, country):
        self.country = country
        self.gc = GameController()
        match country:
            case "Austria":
                self.gc.armies = [board["vie"], board["bud"]]
                self.gc.fleets = [board["tri"]]
            case "France":
                self.gc.armies = [board["par"], board["mar"]]
                self.gc.fleets = [board["bre"]]
            case "Germany":
                self.gc.armies = [board["ber"], board["mun"]]
                self.gc.fleets = [board["kie"], ]
            case "Italy":
                self.gc.armies = [board["ven"], board["rom"]]
                self.gc.fleets = [board["nap"]]
            case "Turkey":
                self.gc.armies = [board["con"], board["smy"]]
                self.gc.fleets = [board["ank"]]
            case "Russia":
                self.gc.armies = [board["mos"], board["war"]]
                self.gc.fleets = [board["sev"], board["stp_sc"]]
            case "England":
                self.gc.armies = [board["lvp"]]
                self.gc.fleets = [board["lon"], board["edi"]]
            case _:
                raise Exception("Invalid Country")
        self.gc.home_supply = self.gc.armies + self.gc.fleets
        if country == "Russia":
            self.gc.home_supply[3] = board["stp"]
        self.gc.owned_tiles = self.gc.home_supply.copy()

    def start_turn(self):
        season = "Spring" if self.turn % 3 == 0 else "Autumn" if self.turn % 3 == 1 else "Winter"
        sub = "You have not yet submitted your moves for this turn! You need not do it immediately but the turn will not end until everyone has done so!" if not self.submitted else "Your orders for this turn have been submitted. Waiting for other players. You may resubmit orders if you want to change them."
        return f"It is turn {self.turn + 1}; {season} {self.turn // 3 + 1901}\nThe current state of the board is…\n{board_state}. {sub}\n"

    def prompt(self, message):
        raise NotImplementedError


NO_SUBMIT = "SYSTEM: You haven't submitted your moves for this turn! You need not do it immediately as disscussion is important, but the turn will not end until everyone has done so!|"
YES_SUBMIT = "SYSTEM: You have submitted your orders for this turn!|"


class OpenAIPlayer(Player):
    global board
    global board_state
    SYSTEM_PROMPT = """You are playing a game of diplomacy as {country}. {personality} Along the way you'll have to talk to other players to progress. You must interact with the game through a series of commands.
    Commands are issued by typing the name of the command followed by a colon (:) followed by the content of the command followed by a pipe (|). You should place a newline after this key punctuation to help readability.
    The first command is mail, this will send a message to the listed countries allowing you to converse. For example, if you were a Russia player you could issue:
    mail england, germany:
    Greetings! I propose a DMZ in the Baltic Sea to ensure mutual security while I focus on southern expansion. Let’s discuss cooperation in the north.|
    This would signal to those countries you were an ally.
    The next command is submit. Submit is how you apply your orders. Bear in mind once every player has submitted the turn will end, so it is advisable to wait to submit until you have finished discussions.
    Orders should be issued with either a for army or f for fleet then the location of the unit a dash (-) and the target location. we will use s for support h for hold and c for convoy. An army not listed in an order set is assumed to be holding.
    The codes for provinces used by the system are as follows:
    nao, nwg, bar, stp, stp_nc, stp_sc, fin, bot, swe, nwy, ska, nth, edi, cly, lvp, iri, yor, hel, den, bal, lvn, mos, war, pru, ber, kie, hol, bel, pic, bre, mao, eng, wal, lon, gas, par, bur, ruh, mun, boh, sil, gal, ukr, sev, rum, bud, vie, tyr, pie, mar, spa, spa_nc, spa_sc, por, wes, naf, lyo, tys, tun, tus, rom, nap, ion, apu, ven, adr, tri, alb, ser, gre, bul, bul_ec, bul_sc, bla, con, aeg, eas, smy, ank, arm, syr
    An example turn one order for a Germany player would be:
    submit:
    a ber - kie
    f kie - den
    a mun s ven - tyr|
    You may send multiple commands per turn. Please refrain from sending either speial characters in your responses except where required (:|)
    RESPOND ONLY with commands in the provided format. They will be handled automatically and will fail to process if malformed. You are aiming to PLAY the game, do not echo the developer prompt.
    """.replace("    ", "")
    history = None

    def __init__(self, country, api_key, model, api_url="", random_voice=True, personality=""):
        super().__init__(country)

        history_file = open("history/" + country + ".txt", "r")
        self.history = json.loads(history_file.read())
        history_file.close()

        self.system_prompt = OpenAIPlayer.SYSTEM_PROMPT.format_map({"country": country, "personality": personality})
        if api_url == "":
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI(api_key=api_key, base_url=api_url)
        self.model = model

        if random_voice:
            if random.random() < 0.7:
                v = random.choice(Voice.AVALIBLE[country])
            else:
                v = random.choice(Voice.AVALIBLE["Misc"])
        else:
            match country:
                case "Austria":
                    v = ("streamElements", "Szabolcs")
                case "France":
                    v = ("streamElements", "fr-CA-Standard-C")
                case "Germany":
                    v = ("streamElements", "de-DE-Wavenet-B")
                case "Italy":
                    v = ("streamElements", "Giorgio")
                case "Turkey":
                    v = ("streamElements", "tr-TR-Wavenet-E")
                case "Russia":
                    v = ("streamElements", "ru-RU-Wavenet-A")
                case "England":
                    v = ("gTTS", "en co.uk")
        self.voice = Voice(v[0], v[1])

    def dump_history(self):
        history_file = open("history/" + self.country + ".txt", "w")
        history_file.write(json.dumps(self.history))
        history_file.close()

    def prompt(self, message):
        message_list = [{"role": "developer",
                         "content": self.system_prompt + "\n" + self.start_turn()}] + self.history + [
                           {"role": "user", "content": message}]
        response = self.client.chat.completions.create(model=self.model, messages=message_list)  # store=True,
        print(response.choices[0].message.content)
        global NO_SUBMIT, YES_SUBMIT
        self.history += [{"role": "user", "content": message.replace(NO_SUBMIT, "").replace(YES_SUBMIT, "")},
                         {"role": "assistant", "content": response.choices[0].message.content}]
        # self.voice.say(response.choices[0].message.content)
        # self.dump_history()
        return response.choices[0].message.content


def backstab_import():
    x = []
    for i in range(100):
        x.append(input())
        if x[-3:] == ["", "", ""]:
            break
    boardstate = ""
    for i in x:
        if i == "":
            continue
        i = i.replace("/", "_")
        if i[:2] == "A " or i[:2] == "F ":
            boardstate = boardstate + i.lower()
        else:
            boardstate = boardstate + i + ","
        boardstate = boardstate + "\n"
    print(boardstate)
    global board_state
    board_state = boardstate + "|"


def process_message_text(msg, sender, message_queue, orders):
    commands = []
    for i in range(len(msg)):
        while msg[i] != "" and msg[i][0] == "\n":
            msg[i] = msg[i][1:]
        if msg[i] == "":
            continue
        commands.append(msg[i].split(":"))

    for command in commands:
        # print(command)
        if command == [""]:
            continue
        elif command[0][:4] == "mail":
            mailto = command[0][5:].split(", ")
            for countryi in mailto:
                cc = []
                for countryj in mailto:
                    if countryi != countryj:
                        cc.append(countryj)
                message = "From " + sender
                if len(cc) > 0:
                    message += " cc "
                    for countryj in cc:
                        if countryj in message_queue.keys():
                            message += countryj + ", "
                    message = message[:-2]
                message += ":" + command[1] + "|\n"
                try:
                    message_queue[countryi.title()] += message
                except KeyError:
                    message_queue[
                        sender] += "SYSTEM: Your previous message was not sent to " + countryi + \
                                   "as it doesn't exist. Remember you are playing the board game Diplomay!!|"

        elif command[0][:6] == "submit":
            print(command)
            global board
            verbose_orders = ""
            for move in command[1].split("\n"):
                if len(move) > 0:
                    verbose_orders += "\t"
                for action in move.split(" "):
                    if action == "":
                        continue
                    elif action == "a":
                        verbose_orders += "Army "
                    elif action == "f":
                        verbose_orders += "Fleet "
                    elif action == "s":
                        verbose_orders += "supports "
                    elif action == "c":
                        verbose_orders += "convoys "
                    elif action == "h":
                        verbose_orders += "holds"
                    elif action == "-":
                        verbose_orders += "-> "
                    else:
                        verbose_orders += str(board[action]) + " "
                if len(move) > 0:
                    verbose_orders = verbose_orders[:-1] + "\n"
            # print("Orders from: "+sender + "\n"+verbose_orders)
            orders[sender] = verbose_orders
            # testout = command[0] + command[1]
            # print(testout + "\n---")
        else:
            print("malformed command: " + str(command))
            message_queue[sender] += "SYSTEM: One of your previous commands was malformed and has not been processed."


def process_message(player, message_queue, orders):
    global NO_SUBMIT
    sender = player.country
    if message_queue[sender] == "":
        if orders[sender] != "":
            print("Skipping " + sender + "'s turn. They've submitted and have an empty inbox.")
            return
        else:
            message_queue[sender] = NO_SUBMIT
    msg = player.prompt(message_queue[sender]).split("|")
    process_message_text(msg, sender, message_queue, orders)
    message_queue[sender] = ""
    if orders[sender] != "":
        player.sumbitted = True


def turn_finished(orders):
    for order in orders.values():
        if order == "":
            return False
    return True


board_state = "Austria,\na bud\nf tri\na vie\nEngland,\nf edi\nf lon\na lvp\nFrance,\nf bre\na mar\na par\nGermany,\na ber\nf kie\na mun\nItaly,\nf nap\na rom\na ven\nRussia,\na mos\nf sev\nf stp_sc\na war\nTurkey,\nf ank\na con\na smy|"
message_queue = {"Austria": "", "England": "", "France": "", "Germany": "", "Italy": "", "Russia": "", "Turkey": ""}
orders = message_queue.copy()

OPENAI_KEY = environ["OPENAI_API_KEY"]
GEMINI_KEY = environ["GEMINI_API_KEY"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

players = [
    OpenAIPlayer("England", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("Austria", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("Italy", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("Turkey", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("Germany", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("Russia", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
    OpenAIPlayer("France", GEMINI_KEY, "gemini-2.0-flash", GEMINI_URL, False),
]

fo = open("history/_save.txt")
save_file = fo.read().split("|")
fo.close()
if save_file != "":  # TODO work out if player has submitted orders
    for player in players:
        player.turn = int(save_file[0])
    board_state = save_file[1]
    saved_orders = save_file[2:]
    for saved_order in saved_orders:
        saved_order = saved_order.split(",\n")
        saved_order[0] = saved_order[0].replace("\n", "")
        try:
            saved_order[1] = saved_order[1].replace("\t", "")
            orders[saved_order[0]] = saved_order[1]
        except IndexError:
            pass

'''for p in players:
    print(p.country + ",",end="\n")
    for a in p.gc.armies:
        print("a " + a.abbr,end="\n")
    for f in p.gc.fleets:
        print("f " + f.abbr,end="\n")'''

i = 0
while not turn_finished(orders):
    print("------------------------" * 2)
    print(players[i].country + "'s Turn (Queue Length: " + str(len(message_queue[players[i].country])) + ")")
    process_message(players[i], message_queue, orders)
    sleep(4)
    i = (i + 1) % 7
    if i == 0:
        print("~~~~~~~~~~~~~~~~~~~~~" * 2)
        print("Negotiation Round Over!")
        print(orders)
        print(message_queue)
        temp_player = players[6]
        random.shuffle(players)
        if players[0] == temp_player:  # Check that a player doesn't move twice in a row
            players[0] = players[6]
            players[6] = temp_player
        input("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("ORDERS ARE IN")
for player in players:
    print(player.country + ",\n"+orders[player.country])

turn_result = ""
for player in players:
    # TODO: Allow the program to automatically resolve turns so we don't need to do this / import from backstabbr.
    turn_result += player.country + ",\n"
    print(player.country + "'s Orders:")
    for order in orders[player.country].split("\n"):
        turn_result += order
        success = input(order + "\n\t>>>")
        if success == "":
            turn_result += " succeeds\n"
        else:
            turn_result += " fails (" + success + ")\n"

orders = {"Austria": "", "England": "", "France": "", "Germany": "", "Italy": "", "Russia": "", "Turkey": ""}
for player in players:
    player.turn += 1
    message_queue[player.country] += "[The turn has completed! orders were as follows]:" + turn_result + "|"
    player.submitted = False
print(message_queue[players[0].country])
print("Please copy the backstabbr board")
backstab_import()


fo = open("history/_save.txt", "w")
fo.write(str(players[0].turn) + "|" + board_state)
for country, order in orders.items():
    fo.write(country + "," + order + "|")
for player in players:
    player.dump_history()
