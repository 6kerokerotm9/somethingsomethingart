# bot.py
import discord
import random
import json
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv("TOKEN")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def direct_message(person, message):
    member = discord.utils.get(message.guild.members, name=person)
    channel = await member.create_dm()
    await channel.send("Send this bot art links that you want to post to other servers")

@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.bot:
        return

    elif message.content == '!quit' or message.content == '!stop' or message.content == '!exit':
        print("quitting out")
        await client.logout()

    elif message.content == '!init' and message.guild != None:
        await direct_message(message.author.name, message)

    elif message.content[:6] == '!send ' and message.guild == None:
        for guild in client.guilds:
            if guild.get_member(message.author.id) is not None:
                for i in range(len(guild.text_channels)):
                    try:
                        await guild.text_channels[i].send(message.content[6:])
                        break
                    except:
                        print("no permissions")
        await message.channel.send("message sent") 

client.run(TOKEN)
