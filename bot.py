import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()



#Client code
#=============================================================================================
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#New members joining in the server
@client.event
async def on_member_join(member):
    await client.get_channel(515696069850693646).send(f'Hi {member.name}, thanks for cu-coming!❤️❤️❤️')

#General Messages
#This will handle all message events
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Chat monitor
    if ('fag' in message.content.lower()) or ('faggot' in message.content.lower()) or ('nigger' in message.content.lower()) or ('nigga' in message.content.lower()):
        await message.channel.send('Watch it there buddy 👀')

    if 'i am not a furry' in message.content.lower():
        await message.channel.send('Are you sure?? 🤔')

    if ('cat' in message.content.lower()) or ('hat' in message.content.lower()):
        await message.channel.send('Oh, Yeah!🐈🎩')


client.run(TOKEN)
