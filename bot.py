import os

import discord
import json
import urllib.request as request

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MERRIAM_TOKEN = os.getenv('MERRIAM_DICTIONARY_API')
MERRIAM_THESAURUS_TOKEN = os.getenv('MERRIAM_THESAURUS_API')

bot = commands.Bot(command_prefix='!')


@bot.command(name='def', help='Defines a single word given as input. Ex: !define {input}')
async def definitionOf(ctx, word):
    jsonDef = await grab_json_definition(word, "collegiate", MERRIAM_TOKEN)
    for i in jsonDef[0]:
        if(i == 'shortdef'):
            for j in jsonDef[0][i]:
                await ctx.send(j)

@bot.command(name='syn', help='Gives synonyms for a single word. Ex: !syn {input}')
async def synonymOf(ctx, word):
	limiter = 0
	jsonSyn = await grab_json_definition(word,"thesaurus", MERRIAM_THESAURUS_TOKEN)
	for i in jsonSyn[0]['meta']['syns'][0]:
		await ctx.send(i)
		limiter = limiter + 1
		if (limiter == 4):
			break

async def grab_json_definition(word, ref, key):
    uri = "https://dictionaryapi.com/api/v3/references/" + ref + "/json/" + word + "?key=" + key
    jsonURL = request.urlopen(uri)
    source = jsonURL.read()
    jsonData = json.loads(source)

    return jsonData

bot.run(TOKEN)
