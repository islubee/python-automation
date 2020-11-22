import os
import discord
from dotenv import load_dotenv
import requests
from datetime import date

client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
@client.event
async def on_ready():
    # api-endpoint
    URL = "https://knowi.com/api/data/ipE4xJhLBkn8H8jisFisAdHKvepFR5I4bGzRySZ2aaXlJgie"

    # location given here
    entityName = "Raw County level Data"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'entityName':entityName}

    # location given here
    exportFormat = "json"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'exportFormat':exportFormat}

    # location given here
    c9SqlFilter = "select%20*%20where%20County%20like%20Onondaga"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'c9SqlFilter':c9SqlFilter}


    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)

    # extracting data in json format
    data = r.json()
    deaths = data[1]["values"]
    confirmedCases = data[0]["values"]
    today = date.today()
    channel = client.get_channel(778791896793219103)
    embed = discord.Embed(title="COVID STATS", description=str(today)) #,color=Hex code
    embed.add_field(name="Confirmed Cases", value=confirmedCases)
    embed.add_field(name="Total Deaths to date", value=deaths)
    embed.set_footer(text="Stay Safe! Wear a mask!") #if you like to
    print(channel)
    await channel.send(embed=embed)
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
