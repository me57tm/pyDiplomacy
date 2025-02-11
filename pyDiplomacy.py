#Deepseek, GPT 4o, Gemini, Azure AI Service (phi)????, MEta LLama, Grok? there's also one called claude

class Tile:
    name = ""
    land_adj = None
    sea_adj = None
    unit = None
    
    def __init__(self,name,land=True,unit=None):
        self.name = name
        self.land = land
        self.unit = unit
        self.land_adj = []
        self.sea_adj = []
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def set_adj(self,land_tiles=[],sea_tiles=[]):
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

    def set_unit(self,unit):
        self.unit = unit

class CoastOnly(Tile):
    parent = None
    def __init__(self,name,parent,unit=None):
        super().__init__(name,False,unit)
        self.parent = parent

    def set_unit(self,unit):
        self.parent.set_unit(unit)
        self.unit = unit
        

class MultiCoast(Tile):
    nc = None
    sc = None
    def __init__(self,name,nc_name,sc_name,unit=None,unit_location="l"):
        super().__init__(name,True,unit)
        self.adj = []
        self.nc = CoastOnly(name + " " + nc_name,self)
        self.sc = CoastOnly(name + " " + sc_name,self)
        
board = {}
board["nao"] = nao = Tile("North Atlantic Ocean",False)
board["nwg"] = nwg = Tile("Norwegian Sea",False)
nwg.set_adj([],nao)
board["bar"] = bar = Tile("Barent's Sea",False)
bar.set_adj([],nwg)
board["stp"] = stp = MultiCoast("Saint Petersburg","North Coast","South Coast")
board["stp_nc"] = stp.nc
stp.nc.set_adj([],bar)
board["stp_sc"] = stp.sc
board["fin"] = fin = Tile("Finland")
fin.set_adj(stp,stp.sc)
board["bot"] = bot = Tile("Golf of Bothnia",False)
bot.set_adj([],[fin,stp.sc])
board["swe"] = swe = Tile("Sweden")
swe.set_adj(fin,[fin,bot])
board["nwy"] = nwy = Tile("Norway")
nwy.set_adj([swe,stp,fin],[swe,nwg,bar,stp.nc])
board["ska"] = ska = Tile("Skaggerak",False)
ska.set_adj([],[swe,nwy])
board["nth"] = nth = Tile("North Sea",False)
nth.set_adj([],[nwg,ska,nwy])
board["edi"] = edi = Tile("Edinburgh")
edi.set_adj([],[nwg,nth])
board["cly"] = cly = Tile("Clyde")
cly.set_adj([edi],[edi,nao,nwg])
board["lvp"] = lvp = Tile("Liverpool")
lvp.set_adj([edi,cly],[nao,cly])
board["iri"] = iri = Tile("Irish Sea",False)
iri.set_adj([],[lvp,nao])
board["yor"] = yor = Tile("Yorkshire")
yor.set_adj([edi,lvp],[nth,edi])
board["hel"] = hel = Tile("Helgoland Bight",False)
hel.set_adj([],[nth])
board["den"] = den = Tile("Denmark")
den.set_adj([swe],[swe,nth,ska,hel])
board["bal"] = bal = Tile("Baltic Sea",False)
bal.set_adj([],[den,swe,bot])
board["lvn"] = lvn = Tile("Livonia")
lvn.set_adj([stp],[bal,bot,stp.sc])
board["mos"] = mos = Tile("Moscow")
mos.set_adj([lvn,stp])
board["war"] = war = Tile("Warsaw")
war.set_adj([mos,lvn])
board["pru"] = pru = Tile("Prussia")
pru.set_adj([lvn,war],[lvn,bal])
board["ber"] = ber = Tile("Berlin")
ber.set_adj([pru],[pru,bal])
board["kie"] = kie = Tile("Kiel")
kie.set_adj([ber,den],[ber,den,bal,hel])
board["hol"] = hol = Tile("The Netherlands")
hol.set_adj([kie],[kie,hel,nth])
board["bel"] = bel = Tile("Belgium")
bel.set_adj([hol],[nth,hol])
board["pic"] = pic = Tile("Picardy")
pic.set_adj([bel],[bel])
board["bre"] = bre = Tile("Brest")
bre.set_adj([pic],[pic])
board["mao"] = mao = Tile("Mid Atlantic Ocean",False)
mao.set_adj([],[nao,iri,bre])
board["eng"] = eng= Tile("English Channel",False)
eng.set_adj([],[mao,iri,bre,pic,bel])
board["wal"] = wal = Tile("Wales")
wal.set_adj([lvp,yor],[iri,eng,lvp])
board["lon"] = lon = Tile("London")
lon.set_adj([wal,yor],[wal,yor,nth,eng])
board["gas"] = gas = Tile("Gascony")
gas.set_adj([bre],[mao,bre])
board["par"] = par = Tile("Paris")
par.set_adj([bre,gas,pic])
board["bur"] = bur = Tile("Burgundy")
bur.set_adj([par,bel,pic,gas])
board["ruh"] = ruh = Tile("Ruhr")
ruh.set_adj([bur,bel,hol,kie])
board["mun"] = mun = Tile("Munich")
mun.set_adj([ruh,bur,ber,kie])
board["boh"] = boh = Tile("Bohemia")
boh.set_adj([mun])
board["sil"] = sil = Tile("Silesia")
sil.set_adj([boh,mun,ber,pru,war])
board["gal"] = gal = Tile("Galacia")
gal.set_adj([war,sil,boh])
board["ukr"] = ukr = Tile("Ukraine")
ukr.set_adj([gal,mos,war])
board["sev"] = sev = Tile("Sevastopol")
sev.set_adj([ukr,mos])
board["rum"] = rum = Tile("Rumania")
rum.set_adj([sev,ukr,gal],[sev])
board["bud"] = bud = Tile("Budapest")
bud.set_adj([rum,gal])
board["vie"] = vie = Tile("Vienna")
vie.set_adj([bud,gal,boh])
board["tyr"] = tyr = Tile("Tyrolia")
tyr.set_adj([vie,boh,mun])
board["pie"] = pie = Tile("Piedmont")
pie.set_adj([tyr])
board["mar"] = mar = Tile("Marseilles")
mar.set_adj([pie,bur,gas],[pie])
board["spa"] = spa = MultiCoast("Spain","North Coast","South Coast")
board["spa_nc"] = spa.nc
board["spa_sc"] = spa.sc
spa.set_adj([mar,gas])
spa.nc.set_adj([],[mao,gas])
spa.sc.set_adj([],[mao,mar])
board["por"] = por = Tile("Portugal")
por.set_adj([spa],[mao,spa.nc,spa.sc])
board["wes"] = wes = Tile("West Mediterranean",False)
wes.set_adj([],[mao,spa.sc])
board["naf"] = naf = Tile("North Africa")
naf.set_adj([],[mao,wes])
board["lyo"] = lyo = Tile("Gulf of Lyon",False)
lyo.set_adj([],[spa.sc,mar,pie,wes])
board["tys"] = tys = Tile("Tyrrhenian Sea",False)
tys.set_adj([],[lyo,wes])
board["tun"] = tun = Tile("Tunis")
tun.set_adj([naf],[naf,wes,tys])
board["tus"] = tus = Tile("Tuscany")
tus.set_adj([pie],[pie,lyo,tys])
board["rom"] = rom = Tile("Rome")
rom.set_adj([tus],[tus,tys])
board["nap"] = nap = Tile("Naples")
nap.set_adj([rom],[rom,tys])
board["ion"] = ion = Tile("Ionian Sea",False)
ion.set_adj([],[nap,tun,tys])
board["apu"] = apu = Tile("Apulia")
apu.set_adj([nap,rom],[ion,nap])
board["ven"] = ven = Tile("Venice")
ven.set_adj([pie,tyr,tus,rom,apu],[apu])
board["adr"] = adr = Tile("Adriatic Sea",False)
adr.set_adj([],[ion,ven,apu])
board["tri"] = tri = Tile("Trieste")
tri.set_adj([bud,vie,tyr,ven],[ven,adr])
board["alb"] = alb = Tile("Albania")
alb.set_adj([tri],[tri,adr,ion])
board["ser"] = ser = Tile("Serbia")
ser.set_adj([tri,bud,alb,rum])
board["gre"] = gre = Tile("Greece")
gre.set_adj([alb,ser],[alb,ion])
board["bul"] = bul = MultiCoast("Bulgaria","East Coast","South Coast")
board["bul_ec"] = bul.nc
board["bul_sc"] = bul.sc
bul.set_adj([ser,gre,rum])
bul.nc.set_adj([],rum)
bul.sc.set_adj([],gre)
board["bla"] = bla = Tile("Black Sea",False)
bla.set_adj([],[sev,rum,bul.nc])
board["con"] = con = Tile("Constantinople")
con.set_adj([bul],[bul.sc,bul.nc,bla])
board["aeg"] = aeg = Tile("Aegean Sea",False)
aeg.set_adj([],[gre,bul.sc,con])
board["eas"] = eas = Tile("East Mediterranean",False)
eas.set_adj([],[aeg,ion])
board["smy"] = smy = Tile("Smyrna")
smy.set_adj([con],[con,aeg,eas])
board["ank"] = ank = Tile("Ankara")
ank.set_adj([con,smy],[con,bla])
board["arm"] = arm = Tile("Armenia")
arm.set_adj([smy,ank,sev],[ank,bla,sev])
board["syr"] = syr = Tile("Syria")
syr.set_adj([arm,smy],[smy,eas])


#for tile in board.values():
    #print("~"+str(tile) +":\nLand: "+str(tile.land_adj)+"\nSea: "+str(tile.sea_adj)+"\n")
for p in board.keys():
    print(p+", ",end="")


AIPrompt = """You are playing a game of diplomacy as {country}. {personality} Along the way you'll have to talk to other players to progress. You must interact with the game through a series of commands.
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
    """
AIPrompt = AIPrompt.replace("    ","")
start_state = "System:\nTurn one, Spring 1901\n---------------------\nThe current board state is as follows...\nAustria,\na bud\nf tri\na vie\nEngland,\nf edi\nf lon\na lvp\nFrance,\nf bre\na mar\na par\nGermany,\na ber\nf kie\na mun\nItaly,\nf nap\na rom\na ven\nRussia\na mos\nf sev\nf stp_sc\na war\nTurkey\nf ank\na con\na smy|\nYou may start issuing commands."
print("\n"+AIPrompt+"\n"+start_state)
def eg_import_from_backstabbr():
    x = []
    for i in range(50):
        x.append(input())
    boardstate = ""
    for i in x:
        if i == "":
            continue
        i = i.replace("/","_")
        if i[:2] == "A " or i[:2] == "F ":
            boardstate = boardstate + i.lower()
        else:
            boardstate = boardstate + i +  ","
        boardstate = boardstate + "\n"
    print(boardstate)
    return boardstate

