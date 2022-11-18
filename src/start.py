import json
import disnake
import requests
from datetime import datetime
from disnake.ext import commands

config = open("config.json")
data = json.load(config)


session = requests.Session()


bot = commands.InteractionBot(test_guilds=data["serverId"])

checks = {
    True:"✅",
    False:"❌"
}

@bot.event
async def on_ready():
    print(f'Ready to use | {bot.user}')

currentVersion = {
    0:"LittleBigPlanet",
    1:"LittleBigPlanet 2",
    2:"LittleBigPlanet 3",
    3:"LittleBigPlanet Vita",
    4:"LittleBigPlanet PSP",
    # -1:"Unknown"
}

currentPlatform = {
    0:"PlayStation 3",
    1:"RPCS3",
    2:"Vita",
    3:"PSP",
    4:"UnitTest",
    # -1:"Unknown"
}

slotType = {
    0:"Story Mode",
    1:"Community levels",
    2:"on Moon",
    3:"???",
    4:"???",
    5:"Pod",
    6:"Local",
    7:"DLC"
}

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
            for i in Status["currentRoom"]["playerIds"]:
                name = session.get(f"{data['apiLink']}/user/{i}").json()
                usernames.append(name["username"])

            parse = "\n".join(usernames)
            embed.add_field(name="Online with:", value=parse, inline=True)
            
        embed.set_footer(text=f'Online | {currentVersion[Status["currentVersion"]]} on {currentPlatform[Status["currentPlatform"]]} | {slotType[Status["currentRoom"]["slot"]["slotType"]]}')
    else:
        last = int(Info["lastLogin"]/1000)
        dt_ts = datetime.fromtimestamp(last)
        embed.set_footer(text=f"Offline | {dt_ts}")
    # embed.add_field(name="Language", value="`"+ Info["language"]+"`" , inline=True)
    # embed.add_field(name="Time zone", value="`"+ Info["timeZone"]+"`" , inline=True)
    embed.add_field(name="Email verified", value=f'{checks[Info["emailAddressVerified"]]}' , inline=True)
    embed.add_field(name="Comments enabled", value=f'{checks[Info["commentsEnabled"]]}' , inline=True)

    await inter.response.send_message(embed=embed)

bot.run(data["token"])