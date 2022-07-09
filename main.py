import logging

import discord
import os  # default module

bot = discord.Bot()

with open("token.secret", "r") as envfile:
    TOKEN = envfile.read()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="ping", description="Ping the bot, and get WebSocket latency")
async def hello(ctx):

    latency_ms = get_latency_ms(ctx.bot)
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency_ms} ms"
    )
    logging.info(f"/ping: latency is {latency_ms} ms")

    await ctx.respond(embed=embed)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Volunteer Matching Bot, type /help"))


@bot.slash_command(name="view", description="View possible volunteering opportunities")
@discord.option("category", "Enter category of volunteer opportunity you'd like to participate in")
async def view(ctx, category):
    pass

async def


bot.run(TOKEN)  # run the bot with the token
