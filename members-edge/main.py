import discord
import os
import dotenv
import time
import baberuth as bruh
import papertrade as ptc
from discord import option
from datetime import datetime
import finmp as fmp
from iso3166 import ISO3166
import log

logger = log.setup_logger(__name__)

# What? You thought I would just hardcode the token?
dotenv.load_dotenv()
TOKEN = str(os.getenv("DISCORD_BOT_TOKEN"))
ver_info = str(os.getenv("VER_INFO"))
burryedge = str(os.getenv("BURRY_EDGE"))  # guild id
theexchange = str(os.getenv("THE_EXCHANGE"))  # guild id
test_chan = str(os.getenv("TEST_CHAN"))  # member-edge-test channel
paper_chan = str(os.getenv("PAPER_CHAN"))  # paper-trade (beta) channel
v4_chan = str(os.getenv("V4_CHAN"))  # vote-4-channel channel
econ_cal_chan = str(os.getenv("ECON_CAL_CHAN"))  # economic-calendar-channel
tifu_chan = str(os.getenv("TIFU_CHAN"))  # BurryEdge "How I Fucked Up" forum channel
scion_cik = str(os.getenv("SCION_CIK"))  # burry_cik

# Note: This is not generally recommended by Discord. It is this way only for the two servers running this release.
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!OHNO"):
        await message.channel.send("👀🍿")

    if message.content.startswith("!ohno"):
        await message.channel.send(
            "Did you hear that? I thought I heard someone whisper. All caps, please."
        )

    if message.content.startswith("!cathie"):
        await message.channel.send(
            "In 1929, 1973, 2000, and 2008, a better short than any company was the guy who would be buying all the way down.\n - *Michael Burry*"
        )

    if message.content.startswith("!advice"):
        await message.channel.send(
            "If you're seeing the economy on the verge of collapse you should do the logical thing and suck a profit from it.\n - *Michael Burry*"
        )

    # Arcane artifact for the little server also testing this bot.
    if message.content.startswith("!DRS"):
        await message.channel.send("📖👑")


@bot.slash_command(name="about", description="Hidden embed about the bot")
async def about(ctx):
    embed = discord.Embed(
        title="Member's Edge",
        description="A bot to grow with the BurryEdge Community",
        color=discord.Colour.dark_gold(),
    )
    embed.add_field(
        name="About Me", value="`/baberuth` is active!. More to come!", inline=False
    )

    embed.add_field(name="Timed Reminders", value="Coming Soon", inline=True)
    embed.add_field(
        name="Paper Competition", value="IN BETA TESTING Q1 2023", inline=True
    )
    embed.add_field(name="Options Flow", value="Limited - Coming Soon", inline=True)

    embed.set_footer(text=ver_info)

    await ctx.respond("Hello! Here's my version info.", embed=embed, ephemeral=True)


@bot.slash_command(
    name="pray", description="The $VET Investor's Prayer", guild_ids=[burryedge]
)
async def about(ctx):
    embed = discord.Embed(
        title="The $VET Investor's Prayer",
        description="A cry for green.",
        color=discord.Colour.dark_green(),
    )
    embed.add_field(
        name="Prayer:",
        value="Dear VET, hallowed be thy name. Your gas will come. May Europe be undone, and our portfolios look like heaven. \nAmen",
        inline=False,
    )

    embed.set_footer(text=ver_info)

    await ctx.respond("Let us pray.", embed=embed)


@bot.slash_command(
    name="plead", description="The $VET Bagholder's Plea", guild_ids=[burryedge]
)
async def about(ctx):
    embed = discord.Embed(
        title="The $VET Bagholder's Plea",
        description="A vigil for green.",
        color=discord.Colour.dark_red(),
    )
    embed.add_field(
        name="Hope:",
        value="Dear VET, hallowed be thy name. Please bring gas. May Europe be cold, and our portfolios look like heaven. \nAmen",
        inline=False,
    )
    embed.set_image(
        url="https://www.cccchelmsford.org/wp-content/uploads/2020/06/vigil.jpg"
    )
    embed.set_footer(text=ver_info)

    await ctx.respond("Let us gather and hope.", embed=embed)


@bot.slash_command(name="mambo", description="...and find out.", guild_ids=[burryedge])
async def mambo(ctx):
    embed = discord.Embed(
        title="",
        description="",
        color=discord.Colour.dark_blue(),
    )
    embed.add_field(name="mambo:", value="I'm ded. I hope they all freeze", inline=True)
    embed.set_thumbnail(
        url="https://static.wikia.nocookie.net/dcanimated/images/b/bb/Deep_Freeze-Title_Card.png"
    )
    embed.set_footer(text=ver_info)

    await ctx.respond("FAFO", embed=embed)  # Send the embed with some text


@bot.slash_command(
    name="sheets", description="show spreadsheet links", guild_ids=[burryedge]
)
async def sheets(ctx):
    embed = discord.Embed(
        title="",
        description="",
        color=discord.Colour.teal(),
    )
    embed.add_field(
        name="@SuperSpy",
        value="Stock Universe v0.7d: [Google Sheet](https://docs.google.com/spreadsheets/d/11cEF1jzciWFMvB5dIlHyifiBttPQqkSEzzyjE8fev3Q)\nStock Tracker v0.7d: [Google Sheet](https://docs.google.com/spreadsheets/d/1umHQqjQ8BWJ8RdqF6TROXRIof1o7Yx5uqzch5Xlo4_c)\nSocial Media Stock Tracker v1.0: [Google Sheet](https://docs.google.com/spreadsheets/d/1uGYxEE-35qLR4JHS_SD8vBm42_B-svWB4afTmnQgDvY/edit#gid=586375650)",
        inline=False,
    )
    embed.add_field(
        name="Guide",
        value="Watch the RK Video to understand how the RK Spreadsheets work.[YouTube](https://www.youtube.com/watch?v=7wjWnMcdnlQ&t=211s)",
        inline=False,
    )
    embed.add_field(name="SuperSpy RK Sheets FAQ", value="Coming soon.", inline=False)
    embed.add_field(
        name="@marco",
        value="Fundamental Sheet: [Google Sheet](https://docs.google.com/spreadsheets/d/1fTbLUElroldIrfFC5It26XDcxH5AviOpTqQp81g-YTI/edit?usp=sharing)",
        inline=False,
    )
    embed.add_field(
        name="@IvoPivo",
        value="Screener: [Google Sheet](https://docs.google.com/spreadsheets/d/1OT-z_QMjmof3SglCtRXb81HnYlROpyIsMhRBbdY07Oc/edit?usp=sharing)",
        inline=False,
    )
    embed.add_field(
        name="@jwohlin2",
        value="Sheet: [Google Sheet](https://docs.google.com/spreadsheets/d/1OiZzESX3dKu0VphCrQP3uOMdzloW5s701fmTAV5Dygk/edit?usp=sharing)\n> *Some modifications I've made include being able to use quarterly data in the analysis, changing the number of periods you want, and having columns BS-CN that RK likes to use occasionally*",
        inline=False,
    )
    embed.add_field(
        name="@onlineonly",
        value="Sheet: [Google Sheet](https://docs.google.com/spreadsheets/d/1rFKqKklDk-PZFcULPtzvquo1muaspDloE3dhGADGHX4/edit?usp=sharing)\n> *Sharing my Metrics workbook, which feeds conditional formatting into the Dashboard in the Tracker....still a work in progress, but want to contribute...*",
        inline=False,
    )
    embed.set_footer(text=ver_info)

    await ctx.respond(
        "Here are all active spreadsheet projects:", embed=embed
    )  # Send the embed with some text


@bot.slash_command(
    name="baberuth",
    description="Make a price-by-date prediction",
    guild_ids=[burryedge],
)
@option("ticker", description="Enter the ticker symbol of the common stock")
@option("direction", description="Which way is it going?", choices=["UP", "DOWN"])
@option(
    "target",
    description="Enter your target price as an integer",
    min_value=1,
    max_value=1000000,
)
@option(
    "thesis", description="In a short sentence, why are you making this prediction?"
)
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
    percent_wager = 50  # temp test value
    date_format = "%Y-%m-%d"

    if direction == "UP":
        updown = 1
    else:
        updown = 0

    try:
        checkdate = datetime.strptime(deadline, date_format)
        bruh.baberuth(name, ticker, updown, target, thesis, percent_wager, deadline)
        begin_date = datetime.today().strftime("%Y-%m-%d")
        baberuth_response = (
            "\N{police cars revolving light}"
            + " Calling the swing! "
            + "\N{white right pointing backhand index}"
        )
        embed = discord.Embed(
            title=begin_date,
            description=baberuth_response,
            color=discord.Colour.gold(),
        )
        embed.add_field(name="Batter", value=name, inline=False)
        embed.add_field(name="Stock", value=ticker, inline=True)
        embed.add_field(name="Direction", value=direction, inline=True)
        embed.add_field(name="Target", value=str(target), inline=True)
        embed.add_field(name="By:", value=deadline, inline=False)
        embed.add_field(name="Why:", value=thesis, inline=False)
        embed.set_footer(text=ver_info)
        channel = bot.get_channel(test_chan)
        await channel.send(embed=embed)
        await ctx.respond(
            "Your prediction was registered. See #members-edge-test channel"
        )
    except ValueError:
        baberuth_response = "Error: Incorrect date format, should be YYYY-MM-DD"
        await ctx.respond(baberuth_response)


@bot.slash_command(name="swing", description="Check your thesis", guild_ids=[burryedge])
@option("ticker", description="Enter the ticker symbol of the thesis to verify")
async def swing(
    ctx,
    ticker: str,
):
    name = ctx.author
    reply = bruh.babe_swing(str(name), str(ticker))
    prefix = "Member: " + str(name) + ", Ticker: " + str(ticker) + ", Result: "
    await ctx.respond(prefix + reply)


@bot.slash_command(
    name="propose_channel",
    description="Propose a stock for a channel vote.",
    guild_ids=[burryedge],
)
@option("ticker", description="Enter the ticker symbol of the stock you're proposing")
@option(
    "pitch",
    description="Enter your supporting reasoning - 500 character limit. Make it count.",
)
async def propose_channel(ctx, ticker: str, pitch: str):
    user = ctx.author
    chars = len(pitch)
    if chars > 500:
        error_msg = f"Your pitch was too long. The limit is 500 characters and you entered {chars} characters"
        await ctx.respond(error_msg, ephemeral=True)
    else:
        await ctx.defer()
        # metrics_list = fmp.biz_metrics(ticker)
        # logger.info("Returned metrics:")
        # logger.info(metrics_list)
        # just in case anyone gets creative
        # metrics = metrics_list[0]
        quote_list = fmp.stock_quote(ticker)
        logger.info("Returned quote:")
        logger.info(quote_list)
        # just in case anyone gets creative
        quote = quote_list[0]
        profile_list = fmp.profile(ticker)
        logger.info("Returned profile:")
        logger.info(profile_list)
        profile = profile_list[0]

        name = quote["name"]
        spot = quote["price"]

        yearHigh = quote["yearHigh"]
        yearLow = quote["yearLow"]
        priceAvg50 = quote["priceAvg50"]
        priceAvg200 = quote["priceAvg200"]
        # revPerShare = metrics['revenuePerShareTTM']
        # netPerShare = metrics['netIncomePerShareTTM']
        # fcfPerShare = metrics['freeCashFlowPerShareTTM']
        # debtPerShare = metrics['interestDebtPerShareTTM']

        image_url = profile["image"]
        about_profile = profile["description"]
        mktCap = profile["mktCap"] / 1000000

        embed = discord.Embed(
            title=name,
            description=f"Here's the proposal by {user} for {ticker}.\nData provided by [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
            color=discord.Colour.gold(),
        )
        embed.add_field(name="Pitch", value=pitch, inline=False)
        embed.add_field(name="Current Price", value=f"{spot:.2f}", inline=False)
        embed.add_field(name="Market Cap", value=f"{mktCap:.3f}M", inline=False)
        embed.add_field(
            name="52W Low & High",
            value=f"({yearLow:.2f}, {yearHigh:.2f})",
            inline=False,
        )
        embed.add_field(
            name="50DMA & 200DMA",
            value=f"({priceAvg50:.2f}, {priceAvg200:.2f})",
            inline=False,
        )
        # embed.add_field(name="Revenue Per Share (TTM)", value=f"{revPerShare:.2f}", inline=False)
        # embed.add_field(name="Net Income Per Share (TTM)", value=f"{netPerShare:.2f}", inline=False)
        # embed.add_field(name="FCF Per Share (TTM)", value=f"{fcfPerShare:.2f}", inline=False)
        # embed.add_field(name="Debt + Service Per Share (TTM)", value=f"{debtPerShare:.2f}", inline=False)
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text=ver_info)
        channel = bot.get_channel(v4_chan)
        card = await channel.send(embed=embed)
        await card.add_reaction("👍")
        await card.add_reaction("👎")
        prompt = await channel.send(about_profile)
        await prompt.create_thread(
            name=f"Discussion on {ticker}", auto_archive_duration=1440
        )
        await ctx.followup.send(f"Your proposal has been registered in <#{v4_chan}>")


@bot.slash_command(
    name="tifu",
    description="Fill out some info about a hard lesson learned.",
    guild_ids=[burryedge],
)
@option(
    "item_1", description="What was your (wrong) thesis? (Try to keep it to a sentence)"
)
@option("item_2", description="What ended up happening?")
@option("item_3", description="Should you have seen it coming?")
@option("item_4", description="Why didn't you see it coming?")
@option(
    "item_5",
    description="What did you learn from this? (High-level. Discord has character limits",
)
@option(
    "link",
    description="(Optional) Got a link to an article or media enshrining your lesson learned?",
)
async def tifu(
    ctx,
    item_1: str,
    item_2: str,
    item_3: str,
    item_4: str,
    item_5: str,
    link: str = None,
):
    await ctx.defer()
    from_line = ctx.channel_id
    user = ctx.author.id
    auteur = ctx.author
    channel = bot.get_channel(tifu_chan)

    header_1 = "**__What I thought:__**" + "\n" + item_1
    header_2 = "**__What actually ended up happening:__**" + "\n" + item_2
    header_3 = "**__Should I have seen it coming?__**" + "\n" + item_3
    header_4 = "**__Why didn't I?__**" + "\n" + item_4
    header_5 = "**__LESSON LEARNED:__**" + "\n" + item_5
    if link is not None:
        header_link = f"Read more here:\n({link})\n - {auteur}"
    else:
        header_link = f"Thanks for reading.\n - {auteur}"

    payload = [header_1, header_2, header_3, header_4, header_5, header_link]
    for item in payload:
        await channel.send(item)
        time.sleep(0.5)

    if from_line is not tifu_chan:
        await ctx.followup.send(
            f"This command only posts in <#{tifu_chan}. See your post there.>",
            delete_after=30,
        )
    else:
        await ctx.followup.send(f"Invoice: Dues to Mr. Market. Bill to: <@{user}>")


"""1. How were you fucked?
2. Should you have known?
3. Why didn't you know?
4. Any lessons moron?
5. Links - media ect.."""


@bot.slash_command(
    name="metrics", description="Quick TTM metrics.", guild_ids=[burryedge, theexchange]
)
@option("ticker", description="Enter the ticker symbol of the stock you want to check")
async def metrics_card(
    ctx,
    ticker: str,
):
    await ctx.defer()
    user = ctx.author
    metrics_list = fmp.biz_metrics(ticker)
    # logger.info("Returned metrics:")
    # logger.info(metrics_list)
    # just in case anyone gets creative
    metrics = metrics_list[0]
    quote_list = fmp.stock_quote(ticker)
    logger.info("Returned quote:")
    logger.info(quote_list)
    # just in case anyone gets creative
    quote = quote_list[0]
    profile_list = fmp.profile(ticker)
    logger.info("Returned profile:")
    logger.info(profile_list)
    profile = profile_list[0]

    name = quote["name"]
    spot = quote["price"]

    yearHigh = quote["yearHigh"]
    yearLow = quote["yearLow"]
    priceAvg50 = quote["priceAvg50"]
    priceAvg200 = quote["priceAvg200"]
    revPerShare = metrics["revenuePerShareTTM"]
    netPerShare = metrics["netIncomePerShareTTM"]
    fcfPerShare = metrics["freeCashFlowPerShareTTM"]
    debtPerShare = metrics["interestDebtPerShareTTM"]

    image_url = profile["image"]
    mktCap = profile["mktCap"] / 1000000

    embed = discord.Embed(
        title=name,
        description=f"Here's the info requested by {user} for {ticker}.\n\nData provided by\n[Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
        color=discord.Colour.gold(),
    )
    embed.add_field(name="Current Price", value=f"{spot:.2f}", inline=False)
    embed.add_field(name="Market Cap", value=f"${mktCap:.3f}M", inline=False)
    embed.add_field(
        name="52W Low & High", value=f"({yearLow:.2f}, {yearHigh:.2f})", inline=False
    )
    embed.add_field(
        name="50DMA & 200DMA",
        value=f"({priceAvg50:.2f}, {priceAvg200:.2f})",
        inline=False,
    )
    embed.add_field(
        name="Revenue Per Share (TTM)", value=f"{revPerShare:.2f}", inline=False
    )
    embed.add_field(
        name="Net Income Per Share (TTM)", value=f"{netPerShare:.2f}", inline=False
    )
    embed.add_field(
        name="FCF Per Share (TTM)", value=f"{fcfPerShare:.2f}", inline=False
    )
    embed.add_field(
        name="Debt + Service Per Share (TTM)", value=f"{debtPerShare:.2f}", inline=False
    )
    embed.set_thumbnail(url=image_url)
    embed.set_footer(text=ver_info)
    await ctx.followup.send(embed=embed)


@bot.slash_command(
    name="company_profile",
    description="Official description of the company.",
    # guild_ids=[burryedge, theexchange],
)
@option("ticker", description="Enter the ticker symbol of the stock you want to check")
async def metrics_card(
    ctx,
    ticker: str,
):
    await ctx.defer()
    quote_list = fmp.stock_quote(ticker)
    logger.info("Returned quote:")
    logger.info(quote_list)
    # just in case anyone gets creative
    quote = quote_list[0]
    profile_list = fmp.profile(ticker)
    logger.info("Returned profile:")
    logger.info(profile_list)
    profile = profile_list[0]

    name = quote["name"]
    spot = quote["price"]

    image_url = profile["image"]
    mktCap = profile["mktCap"] / 1000000
    about_profile = profile["description"]

    embed = discord.Embed(
        title=name,
        description=f"Data provided by\n[Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
        color=discord.Colour.gold(),
    )
    embed.add_field(name="Current Price", value=f"{spot:.2f}", inline=False)
    embed.add_field(name="Market Cap", value=f"${mktCap:.3f}M", inline=False)
    embed.set_thumbnail(url=image_url)
    embed.set_footer(text=ver_info)
    await ctx.followup.send(about_profile, embed=embed)


# ------- Contributor-only commands -----------------


@bot.slash_command(
    name="scion_13f",
    description="See Burry's last known holdings",
    guild_ids=[burryedge],
)
@discord.default_permissions(
    manage_messages=True,
)  # Only members with this permission can use this command.
async def scion_13f(
    ctx,
):
    await ctx.defer()
    dates = fmp.get_13f_dates(scion_cik)
    last = dates[0]
    table = fmp.get_13f_latest(scion_cik, last)
    # link = table.loc["link"][0]
    embed = discord.Embed(
        title="Scion Asset Management",
        description=f"13F reported holdings as of {last}.\nData provided by [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
        color=discord.Colour.gold(),
    )
    for index, row in table.iterrows():
        # do stuff
        stickx = f'{row["tickercusip"]}: {row["titleOfClass"]} class'
        sticky = f'{row["percent"]:.2f}%, {row["shares"]} @ ${row["mark"]:.2f}'
        embed.add_field(name=stickx, value=sticky, inline=False)
    embed.set_footer(text=ver_info)
    await ctx.followup.send(embed=embed)


""""tickercusip": "GEO",
    "nameOfIssuer": "GEO GROUP INC NEW",
    "shares": 2019150,
    "titleOfClass": "COM",
    "value": 15547000,
    "link": "https://www.sec.gov/Archives/edgar/data/1649339/000156761922019784/0001567619-22-019784-index.htm",
"""


@bot.slash_command(
    name="cik_lookup",
    description="Find matching CIKs for a fund name. Returns only names who filed 13Fs.",
    guild_ids=[burryedge],
)
@option(
    "name",
    description="Partial or full name of the fund. Avoid partial matches to 'market' or 'invest'.",
)
@discord.default_permissions(
    manage_messages=True,
)  # Only members with this permission can use this command.
async def cik_lookup(
    ctx,
    name: str,
):
    await ctx.defer(ephemeral=True)
    ciklist = fmp.get_13f_firms(name)
    items = len(ciklist)
    if not ciklist:
        await ctx.followup.send("Your search returned no matching results.")
    elif items > 10:
        await ctx.followup.send(
            "Your search returned more than 10 results. Please refine your search."
        )
    else:
        embed = discord.Embed(
            title=f"CIK Search: {name}",
            description=f"{items} matching funds.\nData provided by [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
            color=discord.Colour.dark_gray(),
        )
        for dicto in ciklist:
            embed.add_field(name=str(dicto["cik"]), value=str(dicto["name"]))
        embed.set_footer(text=ver_info)
        await ctx.followup.send("Found matches.", embed=embed)


@bot.slash_command(
    name="thirteen_f",
    description="Get latest 13F for the supplied CIK",
    guild_ids=[burryedge],
)
@option("CIK", description="Fund CIK. Use /cik_lookup if you don't know it.")
@discord.default_permissions(
    manage_messages=True,
)  # Only members with this permission can use this command.
async def thirteen_f(
    ctx,
    cik: str,
):
    await ctx.defer(ephemeral=True)
    dates = fmp.get_13f_dates(cik)

    if not dates:
        await ctx.followup.send(
            f"FMP has no record of 13Fs ever filed for this CIK: {cik}"
        )
    else:
        last = dates[0]
        table = fmp.get_13f_latest(cik, last)
        fundname = fmp.get_cik_name(cik)
        # link = table.loc["link"][0]

        if len(table.index) > 15:
            embed = discord.Embed(
                title=f"{fundname}",
                description=f"Top 15 13F reported holdings as of {last}.\nSee it all at: [13F]({table.iloc[0, table.columns.get_loc('link')]}) \nData provided by [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
                color=discord.Colour.gold(),
            )
            table15 = table.iloc[0:15]
            for index, row in table15.iterrows():
                # do stuff
                stickx = f'{row["tickercusip"]}: {row["titleOfClass"]} class'
                sticky = f'{row["percent"]:.2f}%, {row["shares"]} @ ${row["mark"]:.2f}'
                embed.add_field(name=stickx, value=sticky, inline=False)
            embed.set_footer(text=ver_info)
            await ctx.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{fundname}",
                description=f"All 13F reported holdings as of {last}.\nCheck the filing at: [13F]({table.iloc[0, table.columns.get_loc('link')]}) \nData provided by [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)",
                color=discord.Colour.gold(),
            )
            for index, row in table.iterrows():
                # do stuff
                stickx = f'{row["tickercusip"]}: {row["titleOfClass"]} class'
                sticky = f'{row["percent"]:.2f}%, {row["shares"]} @ ${row["mark"]:.2f}'
                embed.add_field(name=stickx, value=sticky, inline=False)
            embed.set_footer(text=ver_info)
            await ctx.followup.send(embed=embed)


# ------- Admin-only Commands below -----------------


@bot.slash_command(
    name="high_cal",
    description="Admin Only: Yesterday & Today High-Impact Econ Calendar.",
    # guild_ids=[burryedge, theexchange],
)
@option(
    "day",
    description="Which day do you want?",
    choices=["Yesterday", "Today", "Tomorrow"],
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
async def get_high_cal(ctx, day: str):
    await ctx.defer()
    info = fmp.get_econs(day)
    items = len(info)
    channel = bot.get_channel(econ_cal_chan)
    for report in info:
        await channel.send(report)
        time.sleep(0.5)
    if day == "Yesterday":
        await ctx.followup.send(f"**📅Yesterday's Economic Events: {items} items.**\n\n")
    elif day == "Today":
        await ctx.followup.send(f"**📅Today's Economic Events: {items} items.**\n\n")
    elif day == "Tomorrow":
        await ctx.followup.send(f"**🔮Tomorrow's Economic Events: {items} items.**\n\n")
    else:
        await ctx.followup.send(f"**Error**\n\n")


@bot.slash_command(
    name="admin_swing", description="Manually check a thesis", guild_ids=[burryedge]
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
@option("Member", description="Enter the member whose thesis to verify")
@option("ticker", description="Enter the ticker symbol of the thesis to verify")
async def swing(
    ctx,
    name: str,
    ticker: str,
):
    reply = bruh.babe_swing(str(name), str(ticker))
    prefix = "Member: " + name + ", Ticker: " + ticker + ", Result: "
    await ctx.respond(prefix + reply)


@bot.slash_command(
    name="admin_check", description="Check if I'm a gamemaker", guild_ids=[burryedge]
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
async def admin_check(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author}, you are a designated gamemaker.")


@bot.slash_command(
    name="fix",
    description="Admins only: Correct a BabeRuth thesis",
    guild_ids=[burryedge],
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
@option("name", description="Member to fix")
@option("ticker", description="ticker to fix")
@option("target", description="Enter new target price as an integer")
# fix_thesis(name, ticker, target):
async def fix(ctx: discord.ApplicationContext, name: str, ticker: str, target: int):

    bruh.fix_thesis(name, ticker, target)
    await ctx.respond(
        f"Hello {ctx.author}, {ticker} target has been updated to {target} for {name}."
    )


@bot.slash_command(
    name="admin_paper_round",
    description="Admins only: Create and define a paper trading competition round",
    guild_ids=[burryedge],
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
@option("desc", description="Round description")
@option("start_date", description="Start YYYY-MM-DD format")
@option("end_date", description="End YYYY-MM-DD format")
@option("seed", description="All players' starting amount of cash")
@option(
    "max_pct", description="Maximum percent of initial cash that can buy a position"
)
@option("max_cap", description="Max market cap that can be bought")
@option("min_cap", description="Minimum market cap that can be bought")
@option("max_pos", description="Maximum number of positions that can be held")
@option("detail", description="Details about the rules")
# define_round(conn, round_info): #input round_info is tuple(str desc,str begin_date,str end_date)
async def paper_round(
    ctx: discord.ApplicationContext,
    desc: str,
    start_date: str,
    end_date: str,
    seed: int,
    max_pct: int,
    max_cap: int,
    min_cap: int,
    max_pos: int,
    detail: str,
):

    dbresponse = ptc.create_round(
        desc, start_date, end_date, seed, max_pct, max_cap, min_cap, max_pos, detail
    )

    embed = discord.Embed(
        title="Paper Trading Competition",
        description="A new round was created.",
        color=discord.Colour.blurple(),
    )
    embed.add_field(name="Description", value=desc, inline=False)
    embed.add_field(name="Start Date", value=start_date, inline=True)
    embed.add_field(name="End Date", value=end_date, inline=True)
    embed.add_field(name="Ruleset", value=detail, inline=False)
    embed.add_field(name="Starting Cash", value=str(seed), inline=True)
    embed.add_field(name="Maximum Positions", value=str(max_pos), inline=True)
    embed.add_field(name="Database Response", value=dbresponse, inline=False)
    embed.set_footer(text=ver_info)

    channel = bot.get_channel(paper_chan)
    await channel.send(
        f"An admin has created a new paper trading ruleset. Here are the details:",
        embed=embed,
    )
    await ctx.respond(f"Command registered.")


@bot.slash_command(
    name="admin_table_fetch",
    description="Admins only: Display contents of selected table",
    guild_ids=[burryedge],
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
@option(
    "table",
    description="Name of table",
    choices=["players", "positions", "cash", "rounds", "rules", "performance", "links"],
)
async def fetch_table(ctx, table: str):
    await ctx.defer(ephemeral=True)
    message = ptc.show_table(table)
    await ctx.followup.send(message)


@bot.slash_command(
    name="admin_drop_round",
    description="Admin only: Erase rules for a specified round.",
)
@discord.default_permissions(
    manage_guild=True,
)  # Only members with this permission can use this command.
async def admin_drop_round(ctx, round: int):
    await ctx.defer(ephemeral=True)
    message = ptc.delete_round(round)
    await ctx.followup.send(message)


bot.run(TOKEN)
