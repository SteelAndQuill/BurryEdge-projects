import discord
import os
import dotenv

# What? You thought I would just hardcode the token?
dotenv.load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))

# Note: This is not generally recommended by Discord. It is this way only for the two servers running this release.
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

ver_info = "v0.1 - Maintained by @Steelandquill#6141"

@bot.event    
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!OHNO'):
        await message.channel.send('👀🍿')

    # Arcane artifact for the little server also testing this bot.
    if message.content.startswith('!DRS'):
        await message.channel.send('📖👑')

@bot.slash_command(name = "about", description = "Hidden embed about the bot")
async def about(ctx):
    embed = discord.Embed(
        title="Member's Edge",
        description="A bot to grow with the BurryEdge Community",
        color=discord.Colour.dark_red(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="About Me", value="Basic functionality only at the moment. More to come!", inline=False)

    embed.add_field(name="Timed Reminders", value="Coming Soon", inline=True)
    embed.add_field(name="Paper Competition", value="Coming Soon", inline=True)
    embed.add_field(name="Options Flow", value="Limited - Coming Soon", inline=True)
 
    embed.set_footer(text=ver_info)
 
    await ctx.respond("Hello! Here's my version info.", embed=embed, ephemeral=True) # Send the embed with some text

bot.run(TOKEN)
