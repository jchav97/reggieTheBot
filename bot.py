import os

import discord
import json
import urllib.request as request

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MERRIAM_TOKEN = os.getenv('MERRIAM_DICTIONARY_API')

bot = commands.Bot(command_prefix='!')


@bot.command(name='define', help='Defines a single word given as input. Ex: !define {input}')
async def definitionOf(ctx, word):
    jsonDef = await grab_json_definition(word, "collegiate", MERRIAM_TOKEN)
    for i in jsonDef[0]:
        if(i == 'shortdef'):
            for j in jsonDef[0][i]:
                await ctx.send(j)
                #print(j,"\n")
    #print(jsonDef)


async def grab_json_definition(word, ref, key):
    uri = "https://dictionaryapi.com/api/v3/references/" + ref + "/json/" + word + "?key=" + key
    jsonURL = request.urlopen(uri)
    source = jsonURL.read()
    jsonData = json.loads(source)

    return jsonData

bot.run(TOKEN)
