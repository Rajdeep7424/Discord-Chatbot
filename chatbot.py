import discord
from discord.ext import commands
import aiohttp
import urllib.parse
import wikipedia
import os
from keep_alive import keep_alive  # Import the keep_alive function

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    print("Discord bot is ready.")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content.lower().startswith("?hi"):
            await message.reply(f"Hi, {message.author.display_name}",
                                mention_author=True)
        else:
            await ai_chat(message)


async def ai_chat(message):
    try:
        response = await get_ai_response(message.content)
        if 'wikipedia for' in response.lower():
            query = response.lower().replace("wikipedia for", "").strip()
            results = wikipedia.summary(query, sentences=2)
            await message.reply(content=results, mention_author=True)
        else:
            await message.reply(content=response, mention_author=True)
    except Exception as e:
        await error_embed(f"Bot error, please try again! ({str(e)})", message)


async def get_ai_response(input_text):
    url = f"http://api.brainshop.ai/get?bid=153868&key=rcKonOgrUFmn5usX&uid=1&msg={urllib.parse.quote(input_text)}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if 'cnt' in data:
                    return data['cnt']
                else:
                    return "Sorry, I couldn't understand that."
            else:
                return "Sorry, I couldn't understand that."


async def error_embed(text, message):
    new_embed = discord.Embed(color=discord.Color.red(),
                              description=f"❌ | {text}")
    await message.reply(embed=new_embed, mention_author=True)


keep_alive()  # Start the Flask server
bot.run('token') # enter your bot token
