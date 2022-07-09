import logging

import discord

from utils import get_latency_ms

bot = discord.Bot()

with open("token.secret", "r") as envfile:
    TOKEN = envfile.read()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Volunteer Matching Bot, type /help"))


@bot.slash_command(name="ping", description="Ping the bot, and get WebSocket latency")
async def ping(ctx):
    latency_ms = get_latency_ms(ctx.bot)
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency_ms} ms"
    )
    logging.info(f"/ping: latency is {latency_ms} ms")

    await ctx.respond(embed=embed)


@bot.slash_command(name="view", description="View possible volunteering opportunities")
@discord.option("category", description="Enter category of volunteer opportunity you'd like to participate in")
async def view(ctx, category):
    pass


@bot.slash_command(name="volunteer", description="Apply for a volunteering opportunity")
@discord.option("event_id", description="ID of the event you'd like to join. View /view for volunteer opportunities.")
async def volunteer(ctx, event_id):
    pass


@bot.slash_command(name="upload", description="Upload your volunteer slot here for others to volunteer.")
@discord.option("event_id", description="ID of the event you'd like to join. View /view for volunteer opportunities.")
async def upload(ctx):
    pass


bot.run(TOKEN)  # run the bot with the token
