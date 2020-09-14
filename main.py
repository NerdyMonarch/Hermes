from dotenv import load_dotenv
import os
import pycord
import pygroupme

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
groupme_token = os.getenv('GROUP_ME_TOKEN')

cord = pycord.PyCord(discord_token, groupme_token)
cord.run()