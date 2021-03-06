import os

import discord
import json
import urllib.request as request
from random  import randint
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MERRIAM_TOKEN = os.getenv('MERRIAM_DICTIONARY_API')
MERRIAM_THESAURUS_TOKEN = os.getenv('MERRIAM_THESAURUS_API')
OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_API')

bot = commands.Bot(command_prefix='!')

#!def command: used to find the first 4 definitions of a word
@bot.command(name='def', help='Defines a single word given as input. Ex: !define {input}')
async def definitionOf(ctx, word):
    jsonDef = await grab_json_definition(word, "collegiate", MERRIAM_TOKEN)
    for i in jsonDef[0]:
        if(i == 'shortdef'):
            for j in jsonDef[0][i]:
                await ctx.send(j)

#!syn command: used to find the first 4 synonyms of a word
@bot.command(name='syn', help='Gives synonyms for a single word. Ex: !syn {input}')
async def synonymOf(ctx, word):
	limiter = 0
	jsonSyn = await grab_json_definition(word,"thesaurus", MERRIAM_THESAURUS_TOKEN)
	for i in jsonSyn[0]['meta']['syns'][0]:
		await ctx.send(i)
		limiter = limiter + 1
		if (limiter == 4):
			break

#!roll command: given the number (inclusive), it will return a random number from 1 to {input}
@bot.command(name='roll', help='Rolls a dice, given the number of sides that you input. Ex: !roll {# of sides}')
async def diceRoller(ctx,side):
	try:
		if (side == '1'):
			await ctx.send(side)
		elif (int(side)  <= 0):
			await ctx.send('Sorry, no can do jimbo!')
		else:
			value = str(randint(1,int(side)+1))
			await ctx.send(value)
	except ValueError:
		await ctx.send('Sorry, you\'ve entered invalid inputs')

#!weather command: Used to grab the weather (in progress)
@bot.command(name='weather', help='Grabs CURRENT weather info with a zip code')
async def weatherInfo(ctx, zip):
	jsonWeather = await grab_json_weather(zip, OPEN_WEATHER_TOKEN)
	await ctx.send('The current weather for ' + zip + ' looks like ' + jsonWeather['weather'][0]['description'] + '\nThe temperature is ' + str(jsonWeather['main']['temp']) + ' degrees but will feel like ' + str(jsonWeather['main']['feels_like']) + '\n The max today will be ' + str(jsonWeather['main']['temp_max']))


#-------------------------------------------------------------------Helper functions--------------------------------------------------------------

#Used to grab json data from open weather API
async def grab_json_weather(zip, key):
	uri = "https://api.openweathermap.org/data/2.5/weather?zip=" + zip + "&appid=" + key +"&units=imperial"
	jsonURL = request.urlopen(uri)
	source = jsonURL.read()
	jsonData = json.loads(source)
	return jsonData

#used to grab json data from Mirriam webster API
async def grab_json_definition(word, ref, key):
	uri = "https://dictionaryapi.com/api/v3/references/" + ref + "/json/" + word + "?key=" + key
	jsonURL = request.urlopen(uri)
	source = jsonURL.read()
	jsonData = json.loads(source)
	return jsonData



bot.run(TOKEN)
