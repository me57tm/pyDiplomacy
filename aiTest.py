from os import environ
from openai import OpenAI
import random

#DEEPSEEK_KEY = environ["DEEPSEEK_API_KEY"]
#client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
OPENAI_KEY = environ["GEMINI_API_KEY"]

client = OpenAI(api_key=OPENAI_KEY,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
countries = ["England","Austria","Italy","Turkey","Germany","Russia","France"]

personalities = [
    ["chaotic","lawful"],["evil","moral"],["friendly"],["devious"],["trustworthy","untrustworthy"],
    ["secretly in love with the "+random.choice(countries) + " player", "despises the "+random.choice(countries) + " player"],
    ["impatient"],["quirky"],["distracted"],["strange"],["unhinged"]
    ]
traits = ""
for i in range(5):
    choice = random.choice(personalities)
    traits += random.choice(choice) + ", "
    personalities.remove(choice)
print(traits)
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "developer", "content": "Your job is to summarise a list of randomly generated 'Personality traits' into a sentance instructing an llm who will be playing the board game diplomacy how to act. These traits may be somewhat contradictory but make sure to include all of them anyway."},
        {"role": "user", "content": traits}
    ]
)
print(response.choices[0].message.content)

