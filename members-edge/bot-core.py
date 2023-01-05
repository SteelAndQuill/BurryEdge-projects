import discord
import os
import dotenv
import baberuth as bruh
from discord import option
from datetime import datetime

# What? You thought I would just hardcode the token?
dotenv.load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))

# Note: This is not generally recommended by Discord. It is this way only for the two servers running this release.
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

ver_info = "Members' Edge v0.5 - Maintained by @Steelandquill#6141"
burryedge = 853067058380406794 #guild id
test_chan = 1059698556950286367 #member-edge-test channel

@bot.event    
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!OHNO'):
        await message.channel.send('👀🍿')

    if message.content.startswith('!ohno'):
        await message.channel.send("Did you hear that? I thought I heard someone whisper. All caps, please.")

    # Arcane artifact for the little server also testing this bot.
    if message.content.startswith('!DRS'):
        await message.channel.send('📖👑')

@bot.slash_command(name = "about", description = "Hidden embed about the bot")
async def about(ctx):
    embed = discord.Embed(
        title="Member's Edge",
        description="A bot to grow with the BurryEdge Community",
        color=discord.Colour.dark_gold(), 
    )
    embed.add_field(name="About Me", value="Basic functionality only at the moment. More to come!", inline=False)

    embed.add_field(name="Timed Reminders", value="Coming Soon", inline=True)
    embed.add_field(name="Paper Competition", value="v0.1 baberuth", inline=True)
    embed.add_field(name="Options Flow", value="Limited - Coming Soon", inline=True)
 
    embed.set_footer(text=ver_info)
 
    await ctx.respond("Hello! Here's my version info.", embed=embed, ephemeral=True) 

@bot.slash_command(name = "pray", description = "The $VET Investor's Prayer", guild_ids = [burryedge])
async def about(ctx):
    embed = discord.Embed(
        title="The $VET Investor's Prayer",
        description="A cry for green.",
        color=discord.Colour.dark_green(), 
    )
    embed.add_field(name="Prayer:", value="Dear VET, hallowed be thy name. Your gas will come. May Europe be undone, and our portfolios look like heaven. \nAmen", inline=False)
 
    embed.set_footer(text=ver_info)
 
    await ctx.respond("Let us pray.", embed=embed)

@bot.slash_command(name = "plead", description = "The $VET Bagholder's Plea", guild_ids = [burryedge])
async def about(ctx):
    embed = discord.Embed(
        title="The $VET Bagholder's Plea",
        description="A vigil for green.",
        color=discord.Colour.dark_red(), 
    )
    embed.add_field(name="Hope:", value="Dear VET, hallowed be thy name. Please bring gas. May Europe be cold, and our portfolios look like heaven. \nAmen", inline=False)
    embed.set_thumbnail(url="https://www.cccchelmsford.org/wp-content/uploads/2020/06/vigil.jpg")
    embed.set_footer(text=ver_info)
 
    await ctx.respond("Let us gather and hope.", embed=embed)

@bot.slash_command(name = "mambo", description = "...and find out.", guild_ids = [burryedge])
async def mambo(ctx):
    embed = discord.Embed(
        title="",
        description="",
        color=discord.Colour.dark_blue(),
    )
    embed.add_field(name = "mambo:", value="I'm ded. I hope they all freeze", inline=True)
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/dcanimated/images/b/bb/Deep_Freeze-Title_Card.png")
    embed.set_footer(text=ver_info)

    await ctx.respond("FAFO", embed=embed) # Send the embed with some text

@bot.slash_command(name = "baberuth", description = "Make a price-by-date prediction", guild_ids = [burryedge])
@option("ticker", description="Enter the ticker symbol of the common stock")
@option("direction", description="Which way is it going?", choices=["UP","DOWN"])
@option(
    "target",
    description="Enter your target price as an integer",
    min_value=1,
    max_value=1000000
)
@option("thesis", description="In a short sentence, why are you making this prediction?")
@option("deadline", description="Set your deadline in YYYY-MM-DD format")
async def baberuth(
    ctx, 
    ticker: str,
    direction: str,
    target: int,
    thesis: str,
    deadline: str,
):
    name = ctx.author
    percent_wager = 50 #temp test value
    date_format = '%Y-%m-%d'

    if direction == "UP":
        updown = 1
    else:
        updown = 0

    try:
        checkdate = datetime.strptime(deadline, date_format)
        bruh.baberuth(name, ticker, updown, target, thesis, percent_wager, deadline)
        begin_date = datetime.today().strftime('%Y-%m-%d')
        baberuth_response = "\N{police cars revolving light}"+" Calling the swing! "+"\N{white right pointing backhand index}"
        embed = discord.Embed(
        title=begin_date,
        description=baberuth_response,
        color=discord.Colour.gold(),
        )
        embed.add_field(name="Batter", value=name, inline=False)
        embed.add_field(name="Stock", value=ticker, inline=True)
        embed.add_field(name="Direction", value=direction, inline=True)
        embed.add_field(name="Target", value=str(target), inline=True)
        embed.add_field(name="By:", value=deadline, inline=True)
        embed.add_field(name="Why:", value=thesis, inline=True)
        embed.set_footer(text=ver_info)
        channel = bot.get_channel(test_chan)
        await channel.send(embed=embed)
    except ValueError:
        baberuth_response = "Error: Incorrect date format, should be YYYY-MM-DD"
        await ctx.respond(baberuth_response)

bot.run(TOKEN)
