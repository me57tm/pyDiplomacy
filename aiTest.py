from os import environ
from openai import OpenAI
import random

#DEEPSEEK_KEY = environ["DEEPSEEK_API_KEY"]
#client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
OPENAI_KEY = environ["GEMINI_API_KEY"]

client = OpenAI(api_key=OPENAI_KEY,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
'''response = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)'''
AIPrompt = """You are playing a game of diplomacy as France. Along the way you'll have to talk to other players to progress. You must interact with the game through a series of commands.
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
first = "from italy cc austria, germany, france, england, russia, turkey:\nGreetings everyone! As Italy, I aim to establish a balanced relationship with each of you. I would like to discuss potential alliances and strategies to navigate this game effectively. Let's make the most of this turn together! Looking forward to your responses.|"
AIPrompt = AIPrompt.replace("    ","")
start_state = "It is Spring 1901\n---------------------\nThe current board state is as follows...\nAustria,\na bud\nf tri\na vie\nEngland,\nf edi\nf lon\na lvp\nFrance,\nf bre\na mar\na par\nGermany,\na ber\nf kie\na mun\nItaly,\nf nap\na rom\na ven\nRussia\na mos\nf sev\nf stp_sc\na war\nTurkey\nf ank\na con\na smy|\nYou may start issuing commands."

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "developer", "content": "You are an ai who is being tested"},
        {"role": "user", "content": "please send a short test message"}
    ]
)
print(response.choices[0].message.content)
