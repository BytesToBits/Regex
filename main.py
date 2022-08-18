import disnake, argparse, os
from disnake.ext import commands

from core.enums import Bot

bot = commands.InteractionBot(intents=disnake.Intents.default(), test_guilds=Bot.GUILDS)

@bot.event
async def on_ready():
    print(f"[ONLINE] {bot.user} ({bot.user.id})")

COG_TREE = filter(lambda dir: not "__pycache__" in dir[0] ,os.walk("cogs"))

for cog in COG_TREE:
    dir = cog[0] #.replace("\\", ".")
    bot.load_extensions(dir)
    print("Loaded Cogs:", ', '.join(cog[-1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", dest="dev", action="store_true")

    args = parser.parse_args()

    token = Bot.TOKEN if not args.dev else Bot.DEV_TOKEN

    if args.dev: print("DEV MODE ON")

    bot.run(token)