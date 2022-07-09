import discord
import os  # default module

bot = discord.Bot()

with open("token.secret", "r") as envfile:
    TOKEN = envfile.read()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


bot.run(TOKEN)  # run the bot with the token
