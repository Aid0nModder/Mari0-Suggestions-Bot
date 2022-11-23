import discord, os
from suggestbot import SuggestBot
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

debug_guilds = [discord.Object(760987756985843733), discord.Object(836936601824788520)]

def main():
	client = SuggestBot(debug_guilds, offline=True)
	client.run(token)
	
if __name__ == '__main__':
	main()