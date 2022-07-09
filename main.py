import logging
import discord
import json

from utils import get_latency_ms

bot = discord.Bot()

with open("token.secret", "r") as envfile:
    TOKEN = envfile.read()


def get_categories(ctx):
    return ["Youth", "Elderly", "Disabled"]


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
@discord.option("target", description="Enter target audience of volunteer opportunity you'd like to participate in",
                required=False, autocomplete=get_categories)
async def view(ctx, target):
    with open("data/beneficiary.json", "r") as beneficiaries_raw:
        beneficiaries = json.loads(beneficiaries_raw.read())
        embed = discord.Embed(
            title="Volunteer Opportunities",
            description="Here are some volunteer opportunities for you to try out. Use /volunteer to apply."
        )

        for beneficiary_id in beneficiaries:
            beneficiary = beneficiaries[beneficiary_id]
            if target not in beneficiary["targets"]:
                if target:
                    # Target param is existent
                    continue
            value = f"""{beneficiary["description"]}
**Organisation:** {beneficiary["org"]}
**Target(s)**: {str(beneficiary["targets"]).replace("[", "").replace("]", "").replace("'", "")}
**Contact:** {beneficiary["contact"]}, {beneficiary["contact_discord"]}
**Volunteer ID:**
```
{beneficiary["id"]}
```
"""
            embed.add_field(
                name=beneficiary["summary"],
                value=value
            )
        # embed.add_field(
        #     name="Thanks for your interest!",
        #     value="1"
        # )
    await ctx.respond(embed=embed)


@bot.slash_command(name="volunteer", description="Apply for a volunteering opportunity")
@discord.option("event_id", description="ID of the event you'd like to join. View /view for volunteer opportunities.")
async def volunteer(ctx, event_id):
    userid = str(ctx.user.id)
    event_id_formatted = event_id.strip().lower()

    with open("data/users.json", "r") as users_raw:
        users = json.loads(users_raw.read())
        if not await exit_if_not_registered(ctx, users):
            return
        this_user = users["main_data"][userid]
    with open("data/beneficiary.json", "r+") as beneficiaries_fd:
        beneficiaries = json.loads(beneficiaries_fd.read())
        if event_id_formatted in beneficiaries:
            beneficiary = beneficiaries[event_id_formatted]
            beneficiary["volunteers"].append(userid)
            beneficiaries_fd.seek(0)
            json.dump(beneficiaries, beneficiaries_fd, indent=4)
            beneficiaries_fd.truncate()
        else:
            await ctx.respond("Volunteer ID is invalid.")






async def exit_if_not_registered(ctx, users):
    userid = str(ctx.user.id)
    if userid not in users["ids"]:
        await ctx.respond("You have not registered")
        return False
    else:
        return True


@bot.slash_command(name="register", description="Register for an account")
@discord.option("name")
@discord.option("job")
@discord.option("contact")
@discord.option("interests", description="Comma-separated list of interests [Youth,Elderly,Disabled]")
async def register(ctx: discord.ApplicationContext, name, job, contact, interests: str):
    userid = str(ctx.user.id)
    interests_parsed = interests.split(",")

    with open("data/users.json", "r") as users_raw:
        users = json.loads(users_raw.read())

        if userid in users["ids"]:
            # User alr registered.
            await ctx.respond("You have already registered.")
            return

    with open("data/users.json", "r+") as users_raw:
        volunteer = {
            "name": name,
            "job": job,
            "contact": contact,
            "discord_id": userid,
            "interests": interests_parsed
        }
        users["main_data"][userid] = volunteer
        users["ids"].append(userid)
        logging.info(f"/register: {volunteer}")
        json.dump(users, users_raw, indent=4)
        # users_raw.truncate()
    await ctx.respond("Registered successfully!")


@bot.slash_command(name="upload", description="Upload your volunteer slot here for others to volunteer.")
@discord.option("event_id", description="ID of the event you'd like to join. View /view for volunteer opportunities.")
async def upload(ctx):
    pass


bot.run(TOKEN)  # run the bot with the token
