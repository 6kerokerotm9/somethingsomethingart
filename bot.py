# bot.py
import discord
import validators
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv("TOKEN")

#used to create initial dm with users
async def direct_message(person, message):
    member = discord.utils.get(message.guild.members, name=person)
    channel = await member.create_dm()
    await channel.send("Send this bot art links that you want to post to other servers by using the command !send <link>")

#recursive function to try and reduce runtime
async def findChannel(channels, index):
    found = -1
    if index >= len(channels):
        return found
    if 'art' in channels[index].name:
        found = index
    else:
        found = await findChannel(channels, index+1)
    return found

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.bot:
        return

    #test thing for ease of use 
    elif message.content == '!quit' or message.content == '!stop' or message.content == '!exit':
        print("quitting out")
        await client.logout()

    elif message.content == '!init' and message.guild != None:
        await direct_message(message.author.name, message)

    elif message.content[:6] == '!send ' and message.guild == None:
        if(validators.url(message.content[6:])):
            for guild in message.author.mutual_guilds:
                index = await findChannel(guild.text_channels, 0) #find indexes of art channels
                if index != -1:
                    await guild.text_channels[index].send("from user " f"{message.author.name}: " + message.content[6:])
                else:
                    await message.channel.send("Server " f"{guild} does not have an art channel. Please contact the dev if you actually see this") 
            await message.channel.send("art sent") 
        else:
            await message.channel.send("Invalid link sent, please check your message and try again.") 

client.run(TOKEN)
