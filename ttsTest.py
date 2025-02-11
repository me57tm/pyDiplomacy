from gtts import gTTS
import pyttsx3
import requests
from time import sleep
def generateSoundFiles():
    service = "pyttsx3"
    engine = pyttsx3.init()
    xvoices = engine.getProperty('voices')
    engine.setProperty('voice', xvoices[0].id)
    name = "Voice 0"
    engine.save_to_file(f"Hey Doug, I am {name} from {service}. Would you take a DMZ?","audiotests/en_gb_pyttsx3.mp3")
    print("pyttsx 1")
    engine.runAndWait()
    engine.setProperty('voice', xvoices[1].id)
    name = "Voice 1"
    engine.save_to_file(f"Hey Doug, I am {name} from {service}. Would you take a DMZ?","audiotests/en_us_pyttsx3.mp3")
    print("pyttsx 2")
    engine.runAndWait()


    service = "gTTS"
    gLang = {
        "en": ["co.uk","com.au","ca","co.nz","co.in"],
        "de": ["de"],
        "hu": ["hu"],
        "it": ["it"],
        "fr": ["fr","ca"],
        "ru": ["ru"],
        "tr": ["com.tr"]
        }
    for lang, tldList in gLang.items():
        for tld in tldList:
            name = lang[0] + " " + lang[1] + " dot " + tld
            test_text = f"Hey Doug, I am {name} from {service}. Would you take a DMZ?"
            print(name)
            gResult = gTTS(test_text,lang=lang,tld=tld)
            gResult.save("audiotests/"+lang+"_gtts_"+tld.split(".")[-1]+".mp3")

    service = "Stream Elements"
    seNames = {
        "en": ["Heather","Sean","Linda","Emma","Raveena","Salli","Kimberly","Kendra","Joanna","Ivy","Matthew","Justin","Joey","Nicole","Russell","Geraint","Brian","Amy",'en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-C', 'en-US-Wavenet-D', 'en-US-Wavenet-E', 'en-US-Wavenet-F', 'en-GB-Wavenet-A', 'en-GB-Wavenet-B','en-AU-Wavenet-A', 'en-AU-Wavenet-B', 'en-AU-Wavenet-C', 'en-AU-Wavenet-D', 'en-AU-Standard-D'],
        "de": ["Hans","Marlene","Vicki","de-DE-Wavenet-B","de-DE-Wavenet-A"],
        "at": ["Michael","Karsten"],
        "hu": ["Szabolcs","hu-HU-Wavenet-A"],
        "it": ["Carla","Bianca","Giorgio","it-IT-Wavenet-A", "it-IT-Wavenet-C", "it-IT-Wavenet-D"],
        "fr": ["Mathieu","Celine","Chantal","Guillaume",'fr-CA-Standard-A', 'fr-CA-Standard-B', 'fr-CA-Standard-C', 'fr-CA-Standard-D', 'fr-FR-Wavenet-A', 'fr-FR-Wavenet-B',],
        "ru": ["Maxim","Tatyana","ru-RU-Wavenet-A", "ru-RU-Wavenet-B", "ru-RU-Wavenet-C", "ru-RU-Wavenet-D"],
        "tr": ["Filiz","tr-TR-Wavenet-A", "tr-TR-Wavenet-B", "tr-TR-Wavenet-C", "tr-TR-Wavenet-D", "tr-TR-Wavenet-E"]
        }

    for lang, nameList in seNames.items():
        for name in nameList:
            print(name)
            test_text = f"Hey Doug, I am {name} from {service}. Would you take a DMZ?"
            payload = {"voice":name,"text":test_text}
            response = requests.get("https://api.streamelements.com/kappa/v2/speech",params=payload)
            filename = name
            if  filename[:2] == lang:
                filename = filename[3:]
            filename = lang + "_" + filename
            fo = open("audiotests/"+filename+"_se.wav","wb")
            fo.write(response.content)
            fo.close()
            sleep(1)

payload = {"voice":'de-DE-Wavenet-B',"text":"Greetings, dear friends and neighbors! I, Germany, come in peace and goodwill. Let us work together to ensure a prosperous and balanced Europe. I propose open communication and mutual support to prevent any one power from dominating the board. Let’s discuss how we can all thrive together!"}
response = requests.get("https://api.streamelements.com/kappa/v2/speech",params=payload)
fo = open("chaos_de.wav","wb")
fo.write(response.content)
fo.close()
