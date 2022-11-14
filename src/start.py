import json
import requests
import disnake
from disnake.ext import commands
from datetime import datetime,timezone

config = open("config.json")
data = json.load(config)


session = requests.Session()
# statistics = session.get("{data['apiLink']}/statistics").json()

bot = commands.InteractionBot(test_guilds=data["serverId"])

checks = {
    True:"✅",
    False:"❌"
}

@bot.event
async def on_ready():
    print(f'Ready to use | {bot.user}')

@bot.slash_command(description="Get user info")
async def user(inter,userid: int):
    Info = session.get(f"{data['apiLink']}/user/{userid}").json()
    Status = session.get(f"{data['apiLink']}/user/{userid}/status").json()

    embed=disnake.Embed(title=Info["username"], description=Info["biography"])
    try:
        embed.set_thumbnail(url=f'{data["link"]}/gameAssets/'+Info["iconHash"])
    except Exception:
        embed.set_thumbnail(url=f'{data["link"]}/gameAssets/e6bb64f5f280ce07fdcf4c63e25fa8296c73ec29')
    if Status["statusType"] != 0:

        if Status["currentRoom"] != None:
            usernames = []
            usernames.append(Info["username"])
            for i in Status["currentRoom"]["playerIds"]:
                if i != Info["username"]:
                    pass
                else:
                    name = session.get(f"{data['apiLink']}/user/{i}").json()
                    # print(name["username"])
                    usernames.append(name["username"])

                parse = "\n".join(usernames)
                embed.add_field(name="Online with:", value=parse, inline=True)
                embed.set_footer(text="Online | Room id: " + str(Status["currentRoom"]["roomId"]))

        embed.set_footer(text="Online")
    else:
        last = int(Info["lastLogin"]/1000)
        dt_ts = datetime.fromtimestamp(last)
        embed.set_footer(text=f"Offline | {dt_ts}")
    embed.add_field(name="Language", value="`"+ Info["language"]+"`" , inline=True)
    embed.add_field(name="Time zone", value="`"+ Info["timeZone"]+"`" , inline=True)
    embed.add_field(name="Email verified", value=f'{checks[Info["emailAddressVerified"]]}' , inline=True)
    embed.add_field(name="Comments enabled", value=f'{checks[Info["commentsEnabled"]]}' , inline=True)


    # info = session.get("{data['apiLink']}/user/310",headers=headers).json()
    await inter.response.send_message(embed=embed)

bot.run(data["token"])
